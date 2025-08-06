from sqladmin import ModelView
from src.shop.models.sqlalchemy import Basket, BasketLine, Order, OrderLine


class BasketAdmin(ModelView, model=Basket):
    icon = "fa-solid fa-shopping-basket"
    column_list = [Basket.id, Basket.user_id, Basket.price, Basket.status]
    column_searchable_list = [Basket.user_id]
    category = "Sales"

class BasketLineAdmin(ModelView, model=BasketLine):
    icon = "fa-solid fa-list"
    column_list = [BasketLine.id, BasketLine.product_id, BasketLine.basket_id, BasketLine.quantity, BasketLine.price]
    column_searchable_list = [BasketLine.product_id]
    category = "Sales"

class OrderAdmin(ModelView, model=Order):
    icon = "fa-solid fa-receipt"
    column_list = [Order.id, Order.number, Order.user_id, Order.status, Order.total_price, Order.created_at]
    column_searchable_list = [Order.number, Order.user_id]
    category = "Orders"

class OrderLineAdmin(ModelView, model=OrderLine):
    icon = "fa-solid fa-bars"
    column_list = [OrderLine.id, OrderLine.order_id, OrderLine.product_id, OrderLine.quantity, OrderLine.price]
    column_searchable_list = [OrderLine.order_id, OrderLine.product_id]
    category = "Orders"

def register_products_admin_views(admin):
    admin.add_view(BasketAdmin)
    admin.add_view(BasketLineAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(OrderLineAdmin)
