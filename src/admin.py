from src.catalogue.admin import register_products_admin_views
from src.users.admin import register_users_admin_views
from sqladmin import ModelView
from src.catalogue.models.basket import Basket, BasketLine, OrderLine
from sqladmin import ModelView
from src.catalogue.models.order import Order


def register_admin_views(admin):
    register_users_admin_views(admin=admin)
    register_products_admin_views(admin=admin)



class BasketAdmin(ModelView, model=Basket):
    icon = "fa fa-shopping-basket"
    category = "Orders"
    column_list = [Basket.id, Basket.user_id, Basket.price, Basket.status]
    column_searchable_list = [Basket.status]

class BasketLineAdmin(ModelView, model=BasketLine):
    icon = "fa fa-list"
    category = "Orders"
    column_list = [BasketLine.id, BasketLine.product_id, BasketLine.basket_id, BasketLine.quantity, BasketLine.price]

class OrderLineAdmin(ModelView, model=OrderLine):
    icon = "fa fa-list-alt"
    category = "Orders"
    column_list = [OrderLine.id, OrderLine.product_id, OrderLine.order_id, OrderLine.quantity, OrderLine.price]




class OrderAdmin(ModelView, model=Order):
    icon = "fa fa-box"
    category = "Orders"
    column_list = [
        Order.id, Order.number, Order.basket_id, Order.user_id, Order.address_id,
        Order.total_price, Order.shipping_price, Order.shipping_method,
        Order.status, Order.additional_info, Order.created_at
    ]
    column_searchable_list = [Order.number, Order.shipping_method, Order.status]