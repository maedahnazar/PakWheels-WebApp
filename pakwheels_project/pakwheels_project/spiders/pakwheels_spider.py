import scrapy

from .extractors import PakWheelsExtractor


class PakWheelsSpider(scrapy.Spider):
    name = 'pakwheels'
    allowed_domains = ['pakwheels.com']
    start_urls = ['https://www.pakwheels.com/used-cars/search/-/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_root_url,
                cookies={"countrycurrency": "PKR"}
            )

    def parse_root_url(self, response):
        ad_links = response.css('div.col-md-9.search-listing.pull-right a.car-name.ad-detail-path::attr(href)').getall()
        
        for link in ad_links:
            yield response.follow(link, self.parse_ad_details)

        next_page = response.css('ul.pagination li a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_root_url)

    def parse_ad_details(self, response):
        extractor = PakWheelsExtractor()
        title = extractor.extract_title(response)
        images = extractor.extract_images_links(response)
        location = extractor.extract_location(response)
        price = extractor.extract_price(response)
        car_details = extractor.extract_car_details(response)
        car_features = extractor.extract_car_features(response)
        seller_comments = extractor.extract_seller_comments(response)
        inspection_report = extractor.extract_inspection_report(response)
        
        yield {
            'title': title,
            'location': location,
            'price': price,
            'images': images,
            'car_details': car_details,
            'car_features': car_features,
            'seller_comments': seller_comments,
            'inspection_report': inspection_report,
            'link': response.url,
        }
