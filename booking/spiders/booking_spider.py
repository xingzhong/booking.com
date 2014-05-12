from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from booking.items import BookingItem


class BookingSpider(BaseSpider):
    name = "Booking"
    allowed_domains = ["booking.com"]
    start_urls = map(lambda o:
    	"http://www.booking.com/searchresults.html?city=-1456928;offset=%s;rows=20"%o, 
    	range(0,1000,20))

    def parse(self, response):
        sel = HtmlXPathSelector(response)
        hotels = sel.select("//div[@class='sr_item_content']")
        items = []
        for hotel in hotels:
        	item = BookingItem()
        	item['name'] = hotel.select("h3/a/text()").extract()[0]
        	item['score'] = float(hotel.select(".//span[@class='average']/text()").extract()[0])
        	item['num'] = int(hotel.select(".//strong[@class='count']/text()").extract()[0])
        	items.append(item)
        return items