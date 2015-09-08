# Spider to parse the booking.com
# use the offset parameter trick in its url format

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from booking.items import BookingRooms
from scrapy import Request
import re


class BookingSpider(BaseSpider):
    name = "Booking"
    allowed_domains = ["booking.com"]

    start_urls = ['http://www.booking.com/destination.html']

    def parse(self, response):
        regions = response.xpath('//div[@class="flatListContainer"]/h4/text()')
        countries = response.xpath('//div[@class="flatList"]')
        for region, cs in zip(regions, countries):
            region_name = region.extract()
            for c in cs.xpath('a'):
                country_name = c.xpath('text()').extract()[0]
                country_link = c.xpath('@href').extract()[0]
                url = response.urljoin(country_link)
                req = Request(url, callback=self.parse_city)
                req.meta['region'] = region_name
                req.meta['country'] = country_name
                yield req

    def parse_city(self, response):
        region_name = response.meta['region']
        country_name = response.meta['country']
        for city in response.xpath('//a[contains(@href, "/city/")]'):
            city_name = city.xpath('text()').extract()[0]
            city_link = city.xpath('@href').extract()[0]
            url = response.urljoin(city_link)
            req = Request(url, callback=self.parse_hotel)
            req.meta['region'] = region_name
            req.meta['country'] = country_name
            req.meta['city'] = city_name
            yield req

    def parse_hotel(self, response):
        region_name = response.meta['region']
        country_name = response.meta['country']
        city_name = response.meta['city']
        for hotel in response.xpath('//a[contains(@href, "/hotel/")]'):
            hotel_name = hotel.xpath('text()').extract()[0]
            hotel_link = hotel.xpath('@href').extract()[0]
            url = response.urljoin(hotel_link)
            req = Request(url, callback=self.parse_item)
            req.meta['region'] = region_name
            req.meta['country'] = country_name
            req.meta['city'] = city_name
            req.meta['hotel'] = hotel_name
            yield req

    def parse_item(self, response):
        item = BookingRooms()
        item['region'] = response.meta['region']
        item['country'] = response.meta['country']
        item['city'] = response.meta['city']
        item['hotel'] = response.meta['hotel']
        item['raw'] = response.xpath('//p[contains(@class, "summary")]/text()').extract()[0].replace('\n', ' ')
        try:
            item['numRoom'] = int(re.findall(r'\d+', item['raw'])[0])
        except:
            item['numRoom'] = -1
        item['link'] = response.url
        yield item


