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
    column_searchable_list = ["username", "first_name", "last_name"]

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
        # 合并错误处理逻辑以减少 return 语句
        if not self.can_edit:
            return jsonify(
                {"success": False, "error": "Permission denied", "message": "You do not have permission to edit"}
            ), 403

        try:
            model = self.session.query(self.model).get(user_id)
            if model is None:
                return jsonify({"success": False, "error": "Not Found", "message": "Record not found"}), 404

            json_data = request.get_json()
            if not json_data or "is_admin" not in json_data:
                return jsonify(
                    {"success": False, "error": "Invalid Request", "message": "Invalid or missing JSON data"}
                ), 400

            model.is_admin = bool(json_data["is_admin"])
            self.session.commit()
            return jsonify({"success": True, "message": "管理员状态更新成功", "data": {"is_admin": model.is_admin}})

        except Exception as ex:
            logger.exception("Unexpected error in ajax_update")
            self.session.rollback()
            return jsonify({"success": False, "error": "Server Error", "message": str(ex)}), 500
