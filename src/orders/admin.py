from sqladmin import ModelView

from src.orders.models.sqlalchemy import (
    BasketLine,
    Basket,
    OrderLine,
    Order,
)


CATALOGUE_CATEGORY = 'Orders'


class BasketLineAdmin(ModelView, model=BasketLine):
    column_list = [BasketLine.id, BasketLine.product_id, BasketLine.basket_id, BasketLine.quantity, BasketLine.price]
    column_searchable_list = [BasketLine.id, BasketLine.product_id, BasketLine.basket_id]
    form_columns = [BasketLine.product_id, BasketLine.basket_id, BasketLine.quantity]
    column_sortable_list = [BasketLine.quantity, BasketLine.price, BasketLine.basket_id]
    icon = 'fa-solid fa-list'
    category = CATALOGUE_CATEGORY


class BasketAdmin(ModelView, model=Basket):
    column_list = [Basket.id, Basket.user_id, Basket.price, Basket.status]
    column_searchable_list = [Basket.id, Basket.user_id]
    form_columns = [Basket.user_id, Basket.status]
    column_sortable_list = [Basket.user_id, Basket.price, Basket.status]
    icon = 'fa-solid fa-shopping-cart'
    page_size = 50
    category = CATALOGUE_CATEGORY


class OrderLineAdmin(ModelView, model=OrderLine):
    column_list = [OrderLine.id, OrderLine.product_id, OrderLine.order_id, OrderLine.quantity, OrderLine.price]
    column_searchable_list = [OrderLine.id, OrderLine.product_id, OrderLine.order_id]
    form_columns = [OrderLine.product_id, OrderLine.order_id, OrderLine.quantity]
    column_sortable_list = [OrderLine.quantity, OrderLine.price, OrderLine.order_id, OrderLine.product_id]
    icon = 'fa-solid fa-stream'
    category = CATALOGUE_CATEGORY


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.number, Order.basket_id, Order.user_id, Order.address_id, Order.total_price, Order.shipping_price, Order.shipping_method, Order.status, Order.additional_info, Order.created_at]
    column_searchable_list = [Order.id, Order.number, Order.basket_id, Order.user_id, Order.address_id, Order.total_price]
    form_columns = [Order.basket_id, Order.user_id, Order.address_id, Order.shipping_method, Order.status, Order.additional_info]
    column_sortable_list = [
        Order.number,
        Order.basket_id,
        Order.user_id,
        Order.address_id,
        Order.total_price,
        Order.shipping_price,
        Order.status,
    ]
    icon = 'fa-solid fa-file-invoice'
    page_size = 50
    category = CATALOGUE_CATEGORY


def register_order_admin_views(admin):
    admin.add_view(BasketLineAdmin)
    admin.add_view(BasketAdmin)
    admin.add_view(OrderLineAdmin)
    admin.add_view(OrderAdmin)
