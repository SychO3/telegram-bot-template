# ruff: noqa: RUF012
from __future__ import annotations
import logging
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

from flask import Flask, abort, flash, redirect, request, url_for
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.consts import ICON_TYPE_FONT_AWESOME
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel, gettext
from flask_caching import Cache
from flask_login import current_user
from flask_security.core import RoleMixin, Security, UserMixin
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import inspect
from sqlalchemy.orm import Mapped, relationship
from wtforms import Form, PasswordField

from admin.views.users import UserView as AppUserView
from bot.database.models import UserModel as AppUserModel

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


# Create Flask application
def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    # 配置日志
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    db = SQLAlchemy(app)
    Cache(app)
    Babel(app)

    # 添加 CSRF 保护
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Define models
    roles_admins = db.Table(
        "roles_admins",
        db.Column("admin_id", db.Integer(), db.ForeignKey("admin.id")),
        db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
    )

    class RoleModel(db.Model, RoleMixin):
        __tablename__ = "role"

        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(80), unique=True)
        description = db.Column(db.String(255))

        def __str__(self) -> str:
            return self.name

    class AdminModel(db.Model, UserMixin):
        __tablename__ = "admin"

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(255))
        last_name = db.Column(db.String(255))
        email = db.Column(db.String(255), unique=True, nullable=False)
        password = db.Column(db.String(255), nullable=False)
        active = db.Column(db.Boolean())
        confirmed_at = db.Column(db.DateTime(), default=datetime.utcnow)
        fs_uniquifier = db.Column(db.String(255), unique=True)
        roles: Mapped[list[RoleModel]] = relationship(
            "RoleModel", secondary=roles_admins, backref=db.backref("admins", lazy="dynamic")
        )

        def __str__(self) -> str:
            return self.email

    # Setup Flask-Security
    admin_datastore = SQLAlchemyUserDatastore(db, AdminModel, RoleModel)
    security = Security(app, admin_datastore)

    # Create customized model view class
    class RoleView(ModelView):
        form_base_class = FlaskForm

        can_delete = False
        can_edit = False
        can_create = False
        can_view_details = False
        edit_modal = True
        create_modal = True
        can_export = False
        details_modal = True

        def is_accessible(self) -> bool:
            if not current_user.is_active or not current_user.is_authenticated:
                return False

            return bool(current_user.has_role("superuser"))

        def _handle_view(self, _name: str, **_kwargs: dict) -> Response | None:
            """Override builtin _handle_view in order to redirect users when a view is not accessible."""
            if not self.is_accessible():
                if current_user.is_authenticated:
                    # permission denied
                    abort(403)
                else:
                    # login
                    return redirect(url_for("security.login", next=request.url))
            return None

        def is_visible(self) -> bool:
            return False

    class AdminView(RoleView):
        can_view_details = True
        can_delete = True
        can_edit = True
        can_export = True
        can_create = True
        export_types = ["csv", "xlsx", "json", "yaml"]

        column_editable_list = ["email", "first_name", "last_name"]
        column_searchable_list = column_editable_list
        column_exclude_list = ["password", "fs_uniquifier"]
        column_list = ["email", "first_name", "last_name", "active", "roles"]
        column_details_exclude_list = column_exclude_list
        column_filters = column_editable_list
        form_excluded_columns = ["confirmed_at", "fs_uniquifier"]
        form_overrides = {"password": PasswordField}

        def on_model_change(
            self,
            form: Form,
            model: Any,
        ) -> None:
            """
            Handle model changes before commit.

            Args:
                form: The form containing the data
                model: The model being changed
            """
            if hasattr(form, "password") and form.password.data:  # type: ignore[attr-defined]
                model.password = hash_password(form.password.data)  # type: ignore[attr-defined]

        def get_edit_form(self) -> Form:
            """
            Get the form for editing.

            Returns:
                Form: The configured edit form
            """
            form = super().get_edit_form()
            if hasattr(form, "password"):
                form.password.validators = []
            return form

        def get_create_form(self) -> Form:
            """
            Get the form for creating new records.

            Returns:
                Form: The configured create form
            """
            return super().get_create_form()

        def delete_model(self, model: Any) -> bool:
            """
            Delete model.

            Args:
                model: The model to delete

            Returns:
                bool: True if deletion was successful, False otherwise
            """
            try:
                self.session.delete(model)
                self.session.commit()
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext("Failed to delete record. %(error)s", error=str(ex)), "error")
                    logger.exception("Failed to delete record.")
                self.session.rollback()
                return False
            else:
                return True

        def on_model_delete(self, model: Any) -> None:
            """
            Perform some actions before a model is deleted.

            Args:
                model: The model being deleted
            """

    # Flask views
    def get_orders_count() -> int:
        return 0

    def get_user_count() -> int:
        return db.session.query(AppUserModel).count()

    def get_new_user_count(days_before: int = 1) -> int:
        period_start = datetime.now(timezone.utc) - timedelta(days=days_before)
        return db.session.query(AppUserModel).filter(AppUserModel.created_at >= period_start).count()

    class CustomAdminIndexView(AdminIndexView):
        @expose("/")
        def index(self) -> str:
            days_before: int = 1
            period_start = datetime.now(timezone.utc) - timedelta(days=days_before)
            order_count = get_orders_count()
            user_count = get_user_count()
            new_user_count = get_new_user_count(days_before)
            new_user_count = get_new_user_count(days_before)

            return self.render(
                "admin/index.html",
                order_count=order_count,
                user_count=user_count,
                new_user_count=new_user_count,
                period_start=period_start,
                default_email=app.config.get("DEFAULT_ADMIN_EMAIL"),
                default_password=app.config.get("DEFAULT_ADMIN_PASSWORD"),
            )

    @app.route("/")
    def index() -> Response:
        return redirect(url_for("admin.index"))

    # Initializing the admin panel
    admin = Admin(
        app,
        name="机器人管理后台",
        base_template="my_master.html",
        index_view=CustomAdminIndexView(
            name="Home",
            url="/admin",
            menu_icon_type=ICON_TYPE_FONT_AWESOME,
            menu_icon_value="fa-home",
        ),
        template_mode="bootstrap5",
    )

    admin.add_view(
        AppUserView(
            AppUserModel,
            db.session,
            menu_icon_type=ICON_TYPE_FONT_AWESOME,
            menu_icon_value="fa-users",
            name="Users",
            endpoint="users",
        ),
    )

    admin.add_view(
        AdminView(
            AdminModel,
            db.session,
            menu_icon_type=ICON_TYPE_FONT_AWESOME,
            menu_icon_value="fa-black-tie",
            name="Admins",
            endpoint="admins",
        )
    )

    admin.add_view(
        RoleView(
            RoleModel,
            db.session,
            menu_icon_type=ICON_TYPE_FONT_AWESOME,
            menu_icon_value="fa-tags",
            name="Roles",
            endpoint="roles",
        )
    )

    # define a context processor for merging flask-admin's template context into the flask-security views.
    @security.context_processor
    def security_context_processor() -> dict[str, Any]:
        return {
            "admin_base_template": admin.base_template,
            "admin_view": admin.index_view,
            "h": helpers,
            "get_url": url_for,
        }

    def init_db() -> None:
        inspector = inspect(db.engine)
        if inspector.has_table("admin") and inspector.has_table("role"):
            return

        db.create_all()

        admin_role = RoleModel(name="user", description="does not have access to other administrators")
        super_admin_role = RoleModel(name="superuser", description="has access to manage all administrators")
        db.session.add(admin_role)
        db.session.add(super_admin_role)
        db.session.commit()

        admin_datastore.create_user(
            first_name="Admin",
            email=app.config.get("DEFAULT_ADMIN_EMAIL"),
            password=hash_password(str(app.config.get("DEFAULT_ADMIN_PASSWORD"))),
            roles=[admin_role, super_admin_role],
        )

        db.session.commit()

        return

    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run()
