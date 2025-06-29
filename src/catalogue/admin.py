from sqladmin import ModelView

from src.catalogue.models.sqlalchemy import (
    Category,
    Product,
    ProductCategory,
    ProductDiscount,
    ProductImage,
    StockRecord,
    Basket,
    BasketLine,
    Order,
    OrderLine,
)


CATALOGUE_CATEGORY = "Catalogue"


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.title, Product.is_active]
    column_searchable_list = [Product.title, Product.description]
    form_columns = ["title", "description", "short_description", "is_active"]
    column_sortable_list = ["title", "is_active"]
    icon = "fa-solid fa-box"
    category = CATALOGUE_CATEGORY


class ProductCategoryAdmin(ModelView, model=ProductCategory):
    column_list = [ProductCategory.product, ProductCategory.category]
    column_searchable_list = [ProductCategory.product_id, ProductCategory.category_id]
    form_columns = ["product", "category"]
    icon = "fa-solid fa-tags"
    category = CATALOGUE_CATEGORY


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.title, Category.is_active, Category.parent]
    column_searchable_list = [Category.title]
    form_columns = ["title", "description", "image", "is_active", "parent"]
    icon = "fa-solid fa-sitemap"
    category = CATALOGUE_CATEGORY


class ProductImageAdmin(ModelView, model=ProductImage):
    column_list = [ProductImage.product, ProductImage.original, ProductImage.thumbnail]
    column_searchable_list = [ProductImage.caption]
    form_columns = ["product", "original", "thumbnail", "caption"]
    icon = "fa-solid fa-image"
    category = CATALOGUE_CATEGORY


class StockRecordAdmin(ModelView, model=StockRecord):
    column_list = [StockRecord.product, StockRecord.price, StockRecord.quantity]
    column_searchable_list = [StockRecord.price, StockRecord.quantity]
    form_columns = ["product", "price", "quantity", "date_created", "additional_info"]
    icon = "fa-solid fa-warehouse"
    category = CATALOGUE_CATEGORY


class ProductDiscountAdmin(ModelView, model=ProductDiscount):
    column_list = [
        ProductDiscount.product,
        ProductDiscount.discount_percent,
        ProductDiscount.discount_amount,
    ]
    column_searchable_list = [ProductDiscount.valid_from, ProductDiscount.valid_to]
    form_columns = [
        "product",
        "discount_percent",
        "discount_amount",
        "valid_from",
        "valid_to",
    ]
    icon = "fa-solid fa-percent"
    category = CATALOGUE_CATEGORY


class BasketAdmin(ModelView, model=Basket):
    name = "Basket"
    name_plural = "Baskets"
    icon = "fa fa-shopping-basket"
    category = "Shop"

    column_list = [Basket.id, Basket.user_id, Basket.price, Basket.status]
    column_searchable_list = [Basket.user_id]
    column_sortable_list = [Basket.id, Basket.user_id, Basket.price]


class BasketLineAdmin(ModelView, model=BasketLine):
    name = "Basket Line"
    name_plural = "Basket Lines"
    icon = "fa fa-list"
    category = "Shop"

    column_list = [
        BasketLine.id,
        BasketLine.product_id,
        BasketLine.basket_id,
        BasketLine.quantity,
        BasketLine.price,
    ]
    column_searchable_list = [BasketLine.product_id]
    column_sortable_list = [BasketLine.id, BasketLine.quantity, BasketLine.price]


class OrderAdmin(ModelView, model=Order):
    name = "Order"
    name_plural = "Orders"
    icon = "fa fa-box"
    category = "Orders"

    column_list = [
        Order.id,
        Order.number,
        Order.user_id,
        Order.status,
        Order.total_price,
        Order.created_at,
    ]
    column_searchable_list = [Order.number, Order.user_id]
    column_sortable_list = [Order.number, Order.created_at, Order.total_price]


class OrderLineAdmin(ModelView, model=OrderLine):
    name = "Order Line"
    name_plural = "Order Lines"
    icon = "fa fa-receipt"
    category = "Orders"

    column_list = [
        OrderLine.id,
        OrderLine.order_id,
        OrderLine.product_id,
        OrderLine.quantity,
        OrderLine.price,
    ]
    column_searchable_list = [OrderLine.order_id]
    column_sortable_list = [OrderLine.id, OrderLine.price]


def register_products_admin_views(admin):
    admin.add_view(ProductAdmin)
    admin.add_view(ProductCategoryAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductImageAdmin)
    admin.add_view(StockRecordAdmin)
    admin.add_view(ProductDiscountAdmin)
    admin.add_view(BasketAdmin)
    admin.add_view(BasketLineAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(OrderLineAdmin)
