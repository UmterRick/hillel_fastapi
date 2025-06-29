from sqladmin import Admin
from src.catalogue.admin import register_products_admin_views
from src.users.admin import register_users_admin_views


def register_admin_views(admin):
    register_users_admin_views(admin=admin)
    register_products_admin_views(admin=admin)
