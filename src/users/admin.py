from sqladmin import ModelView

from src.users.models.sqlalchemy import User, UserAddress


USERS_CATEGORY = "Users"


class UserAdmin(ModelView, model=User):
    category = USERS_CATEGORY
    column_list = [
        User.id,
        User.email,
        User.first_name,
        User.last_name,
        User.is_active,
        User.is_admin,
        User.date_joined,
    ]
    column_details_list = [
        User.id,
        User.email,
        User.phone_number,
        User.first_name,
        User.last_name,
        User.is_active,
        User.is_admin,
        User.date_joined,
        User.last_login,
    ]
    column_searchable_list = [User.email, User.first_name, User.last_name]
    column_sortable_list = [User.id, User.email, User.date_joined]


class UserAddressAdmin(ModelView, model=UserAddress):
    category = USERS_CATEGORY
    column_list = [
        UserAddress.id,
        UserAddress.user_id,
        UserAddress.title,
        UserAddress.city,
        UserAddress.street,
    ]
    column_details_list = [
        UserAddress.id,
        UserAddress.user_id,
        UserAddress.title,
        UserAddress.city,
        UserAddress.street,
        UserAddress.house,
        UserAddress.apartment,
        UserAddress.post_code,
        UserAddress.additional_info,
    ]
    column_searchable_list = [UserAddress.city, UserAddress.street, UserAddress.title]


def register_users_admin_views(admin):
    admin.add_view(UserAdmin)
    admin.add_view(UserAddressAdmin)
