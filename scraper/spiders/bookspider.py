import scrapy
from scraper.items import BookItem  
import re

CLEANR = re.compile('<.*?>') 

class BookspiderSpider(scrapy.Spider):
    DOMAIN = "janeausten.fandom.com"
    name = "bookspider"
    allowed_domains = [DOMAIN]
    start_urls = [f"https://{DOMAIN}/wiki/The_Jane_Austen_Wiki"]
    book_count = 0

    def parse(self, response):
        books = response.css('#gallery-0 .lightbox-caption a')
        
        for book in books:
            book_url = f"https://{self.DOMAIN}" + book.attrib['href']
            yield response.follow(book_url, callback=self.parse_book)
    
    def parse_book(self, response):
        self.book_count += 1
        book_item = BookItem()

        
        book_item['id'] = self.book_count
        book_item["title"] = response.css(".mw-page-title-main::text").get()
        book_item["year"] = response.css("aside div[data-source='published'] > div::text").get()
        book_item["characters"] = response.xpath("//div[@class='mw-parser-output']/ul[1]//li/a/@title").extract() + response.xpath("//div[@class='mw-parser-output']/ul[2]//li/a/@title").extract()
        book_item["overview"] = self.parse_plot(response)
        
        yield book_item
    
    def parse_plot(self, response):
        elements = response.css(".mw-parser-output > *")
        plot = []
        
        for i in range(len(elements)):
            if (elements[i].css(".mw-headline::text").get() == 'Plot'):
                
                for j in range(i+1, len(elements)):
                    if (elements[j].css(".mw-headline").get()):
                        break
                    plot.append(re.sub(CLEANR, '', elements[j].get()).strip())

                break
            
        return ' '.join(plot)
    

