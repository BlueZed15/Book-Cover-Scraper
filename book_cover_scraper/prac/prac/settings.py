
BOT_NAME = "covers"

SPIDER_MODULES = ["prac.spiders"]
NEWSPIDER_MODULE = "prac.spiders"

FEEDS={
    'books.json':{'format':'json'}
}
CONCURRENT_REQUESTS = 32

ITEM_PIPELINES = {
    "prac.pipelines.PracPipeline": 300,
}
AUTOTHROTTLE_ENABLED = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
