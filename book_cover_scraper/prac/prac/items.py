import scrapy


class PracItem(scrapy.Item):
    pass

class BookCoverItem(scrapy.Item):
    book_title=scrapy.Field()
    cover_url=scrapy.Field()

class PGBookCoverItem(scrapy.Item):
    id=scrapy.Field()
    cover_url=scrapy.Field()