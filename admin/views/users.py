# ruff: noqa: RUF012
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort, redirect, request, url_for, jsonify
from flask_wtf import FlaskForm
from flask_admin import expose
import logging

logger = logging.getLogger(__name__)

class UserView(ModelView):
    form_base_class = FlaskForm
    
    # 明确指定要显示的列
    column_list = [
        'id', 
        'username', 
        'first_name', 
        'last_name',
        'language_code',
        'is_admin',
        'is_suspicious',
        'is_block',
        'is_premium',
        'created_at'
    ]
    
    # 可以搜索的列
    column_searchable_list = ['username', 'first_name', 'last_name']
    
    # 可以筛选的列
    column_filters = [
        'is_admin', 
        'is_suspicious', 
        'is_block', 
        'is_premium',
        'created_at'
    ]
    
    # 排除不显示的列
    column_exclude_list = [
        'telegram_id',
        'fs_uniquifier',
        'session_data'
    ]
    
    # 表单中排除的字段
    form_excluded_columns = [
        'telegram_id',
        'fs_uniquifier',
        'session_data',
        'created_at'
    ]

    # 列的友好名称
    column_labels = {
        'id': 'ID',
        'username': '用户名',
        'first_name': '名字',
        'last_name': '姓氏',
        'language_code': '语言代码',
        'is_admin': '管理员',
        'is_suspicious': '可疑',
        'is_block': '封禁',
        'is_premium': '会员',
        'created_at': '创建时间'
    }
    
    # 只读字段
    column_editable_list = [
        'is_admin',
        'is_suspicious',
        'is_block',
        'is_premium'
    ]
    
    can_create = False  # 禁止创建新用户
    can_delete = True   # 允许删除用户
    can_edit = True     # 允许编辑用户
    can_view_details = True  # 允许查看详情
    
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        return bool(current_user.has_role("superuser"))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for("security.login", next=request.url))

    @expose('/ajax/update/<int:id>', methods=['POST'])
    def ajax_update(self, id):
        if not self.can_edit:
            return jsonify({
                'success': False,
                'error': 'Permission denied',
                'message': 'You do not have permission to edit'
            }), 403

        try:
            model = self.session.query(self.model).get(id)
            if model is None:
                return jsonify({
                    'success': False,
                    'error': 'Not Found',
                    'message': 'Record not found'
                }), 404
                
            json_data = request.get_json()
            if json_data is None:
                return jsonify({
                    'success': False,
                    'error': 'Invalid Request',
                    'message': 'No JSON data received'
                }), 400

            if 'is_admin' in json_data:
                try:
                    model.is_admin = bool(json_data['is_admin'])
                    self.session.commit()
                    
                    return jsonify({
                        'success': True,
                        'message': '管理员状态更新成功',
                        'data': {
                            'is_admin': model.is_admin
                        }
                    })
                except Exception as ex:
                    logger.error(f'Failed to update is_admin status: {str(ex)}')
                    self.session.rollback()
                    return jsonify({
                        'success': False,
                        'error': 'Database Error',
                        'message': str(ex)
                    }), 500
            else:
                return jsonify({
                    'success': False,
                    'error': 'Invalid Request',
                    'message': 'Missing is_admin field'
                }), 400

        except Exception as ex:
            logger.error(f'Unexpected error in ajax_update: {str(ex)}')
            return jsonify({
                'success': False,
                'error': 'Server Error',
                'message': str(ex)
            }), 500
