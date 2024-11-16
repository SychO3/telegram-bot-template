# ruff: noqa: RUF012
from __future__ import annotations
import logging

from flask import Response, abort, jsonify, redirect, request, url_for
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_wtf import FlaskForm

logger = logging.getLogger(__name__)


class UserView(ModelView):
    form_base_class = FlaskForm

    # 明确指定要显示的列
    column_list = [
        "id",
        "username",
        "first_name",
        "last_name",
        "language_code",
        "is_admin",
        "is_suspicious",
        "is_block",
        "is_premium",
        "created_at",
    ]

    # 可以搜索的列
    column_searchable_list = ["id", "username", "first_name", "last_name"]

    # 可以筛选的列
    column_filters = ["is_admin", "is_suspicious", "is_block", "is_premium", "created_at"]

    # 排除不显示的列
    column_exclude_list = ["telegram_id", "fs_uniquifier", "session_data"]

    # 表单中排除的字段
    form_excluded_columns = ["telegram_id", "fs_uniquifier", "session_data", "created_at"]

    # 列的友好称
    column_labels = {
        "id": "ID",
        "username": "用户名",
        "first_name": "名字",
        "last_name": "姓氏",
        "language_code": "语言代码",
        "is_admin": "管理员",
        "is_suspicious": "可疑",
        "is_block": "封禁",
        "is_premium": "会员",
        "created_at": "创建时间",
    }

    # 只读字段
    column_editable_list = ["is_admin", "is_suspicious", "is_block", "is_premium"]

    can_create = False  # 禁止创建新用户
    can_delete = True  # 允许删除用户
    can_edit = True  # 允许编辑用户
    can_view_details = True  # 允许查看详情

    def is_accessible(self) -> bool:
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        return bool(current_user.has_role("superuser"))

    def _handle_view(self, _name: str, **_kwargs: dict) -> None | redirect:  # type: ignore[misc]
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
                return None
            return redirect(url_for("security.login", next=request.url))
        return None

    @expose("/ajax/update/<int:user_id>", methods=["POST"])
    def ajax_update(self, user_id: int) -> tuple[Response, int] | Response:
        if not self.can_edit:
            return jsonify(
                {"success": False, "error": "Permission denied", "message": "您没有编辑权限"}
            ), 403

        try:
            model = self.session.query(self.model).get(user_id)
            if model is None:
                return jsonify({"success": False, "error": "Not Found", "message": "找不到记录"}), 404

            json_data = request.get_json()
            if not json_data:
                return jsonify(
                    {"success": False, "error": "Invalid Request", "message": "无效的请求数据"}
                ), 400

            # 允许更新的布尔字段列表
            allowed_fields = ["is_admin", "is_suspicious", "is_block", "is_premium"]

            # 检查请求中的字段
            update_field = None
            update_value = None

            for field in allowed_fields:
                if field in json_data:
                    update_field = field
                    update_value = json_data[field]
                    break

            if update_field is None:
                return jsonify(
                    {"success": False, "error": "Invalid Request", "message": "没有有效的更新字段"}
                ), 400

            # 确保值是布尔类型
            update_value = bool(update_value)

            # 更新字段
            setattr(model, update_field, update_value)
            self.session.commit()

            # 返回更新后的实际值
            return jsonify({
                "success": True, 
                "message": "状态更新成功", 
                "data": {
                    "field": update_field,
                    "value": getattr(model, update_field)
                }
            })

        except Exception as ex:
            logger.exception("Unexpected error in ajax_update")
            self.session.rollback()
            return jsonify({"success": False, "error": "Server Error", "message": str(ex)}), 500

    def get_raw_value(self, model, name):
        """直接从数据库获取原始值"""
        try:
            value = getattr(model, name)
            # 直接从数据库获取原始值
            if hasattr(value, "_sa_instance_state"):
                # 如果是 SQLAlchemy 对象，获取其实际值
                return getattr(model.__table__.c, name).type.python_type(value)
            return value
        except Exception as e:
            logger.exception(f"Error getting raw value for {name}")
            return False

    def get_value(self, context, model, name):
        """重写获取值的方法"""
        try:
            if name in ['is_admin', 'is_suspicious', 'is_block', 'is_premium']:
                raw_value = self.get_raw_value(model, name)
                logger.info(f"Raw value for {name}: {raw_value}, type: {type(raw_value)}")
                return bool(raw_value)
            return super(UserView, self).get_value(context, model, name)
        except Exception as e:
            logger.exception(f"Error in get_value for {name}")
            return None

    def _format_bool_value(self, value):
        """格式化布尔值"""
        if value is None:
            return False
        if isinstance(value, int):
            return value != 0
        return bool(value)
