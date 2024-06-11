import scrapy
import requests
from prac.items import BookCoverItem
from prac.items import PGBookCoverItem


class AmazonSpider(scrapy.Spider):
    name='amazoncoverimage'
    allowed_domains=['amazon.in']
    start_urls=["https://www.amazon.in/s?k=novels&i=stripbooks&crid=WZ94HF7VRJSQ&qid=1717798357&sprefix=nove%2Cstripbooks%2C486&ref=sr_pg_1"]

    custom_settings = {
        'FEEDS':{'amazon_books':{'format':'json'}},
        'ROBOTSTXT_OBEY' : True
    }

    def parse(self,response):
        #page_url='https://www.amazon.in/s?k=novels&crid=1SH83FIUR9EC3&sprefix=novel%2Caps%2C308&ref=nb_sb_noss_1'
        novels=response.css('h2 a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal::attr(href)').getall()
        for novel in novels:
            novel_url='https://www.amazon.in'+str(novel)
            yield response.follow(novel_url,callback=self.parse_img)

        next_page=response.css('div.a-section.a-text-center.s-pagination-container span a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)')
        next_page_url='https://www.amazon.in'+str(next_page.getall()[0])
        #print('..\n..',next_page_url,'..\n..')
        yield response.follow(next_page_url,callback=self.parse)

    def parse_img(self,response):
        image=response.css('div#imgTagWrapperId.imgTagWrapper img::attr(data-old-hires)')
        book_cover=BookCoverItem()
        book_cover['book_title']=response.css('div h1 span#productTitle ::text').get()
        book_cover['cover_url']=image.getall()[0]

        yield book_cover

class ProjectGutenbergSpider(scrapy.Spider):
    name='pgcoverimage'
    allowed_domains=['mirrorservice.org']
    start_urls=["http://www.mirrorservice.org/sites/ftp.ibiblio.org/pub/docs/books/gutenberg/"]

    custom_settings = {
        'FEEDS': {'project_gutenberg_books': {'format': 'json'}},
        'ROBOTSTXT_OBEY':False,
        'ITEM_PIPELINES':{'prac.pipelines.PG_Pipeline':300}
    }

    def __init__(self):
        self.save_count = 0
        self.book_count = 10

    def parse(self,response):
        main_link="http://www.mirrorservice.org/sites/ftp.ibiblio.org/pub/docs/books/gutenberg/"

        while self.save_count<5:
            directory_list='/'.join(list(str(self.book_count)))[:-2]
            relative_url=main_link+directory_list+'/'+str(self.book_count)+'/'+str(self.book_count)+'-h'
            cover_url=requests.get(relative_url+'/images/cover.jpg')
            book_cover = PGBookCoverItem()
            if cover_url.status_code==200:
                self.save_count+=1
                book_cover['id']=str(self.book_count)
                book_cover['cover_url']=relative_url+'/images/cover.jpg'
            self.book_count+=1

            yield book_cover







