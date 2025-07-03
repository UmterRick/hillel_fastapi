from elasticsearch.dsl import Document as ElasticDocument, Text

PRODUCT_INDEX = "products_index"

class ProductIndex(ElasticDocument):
    title = Text()
    description = Text()
    short_description = Text()

    class Index:
        name = PRODUCT_INDEX
