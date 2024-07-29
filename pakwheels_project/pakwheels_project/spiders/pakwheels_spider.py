import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .extractors import PakWheelsExtractor


class PakWheelsSpider(CrawlSpider):
    name = 'pakwheels'
    allowed_domains = ['pakwheels.com']
    start_urls = ['https://www.pakwheels.com/used-cars/search/-/']

    rules = (
        Rule(
            LinkExtractor(restrict_css='div.col-md-9.search-listing.pull-right a.car-name.ad-detail-path'), 
            callback='parse_ad_details'
        ),
        Rule(LinkExtractor(restrict_css='ul.pagination li a[rel="next"]'), follow=True),
    )

    def parse_ad_details(self, response):
        yield {
            'title': PakWheelsExtractor.extract_title(response),
            'location': PakWheelsExtractor.extract_location(response),
            'price': PakWheelsExtractor.extract_car_price(response),
            'images': PakWheelsExtractor.extract_car_images_links(response),
            'car_details': PakWheelsExtractor.extract_car_details(response),
            'car_features': PakWheelsExtractor.extract_car_features(response),
            'seller_comments': PakWheelsExtractor.extract_car_seller_comments(response),
            'inspection_report': PakWheelsExtractor.extract_inspection_report(response),
            'link': response.url,
        }
