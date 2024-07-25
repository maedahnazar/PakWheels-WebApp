import scrapy
import logging

class PakWheelsSpider(scrapy.Spider):
    name = 'pakwheels'
    allowed_domains = ['pakwheels.com']
    start_urls = ['https://www.pakwheels.com/used-cars/search/-/']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'COOKIES_ENABLED': True,
    }

    def start_requests(self):
        cookies = {
            "countrycurrency": "PKR",
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_root_url, cookies=cookies)

    def parse_root_url(self, response):
        ad_links = response.css('a.car-name.ad-detail-path::attr(href)').getall()
        
        logging.info(f'Found {len(ad_links)} ad links on the page.')

        for link in ad_links:
            yield response.follow(link, self.parse_ad_details)

        # follow pagination links
        next_page = response.css('ul.pagination li a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_root_url)

    def parse_ad_details(self, response):
        title = self.extract_title(response)
        images = self.extract_images_links(response)
        car_details = self.extract_car_details(response)
        car_features = self.extract_car_features(response)
        seller_comments = self.extract_seller_comments(response)
        location = self.extract_location(response)
        price = self.extract_price(response)
        
        yield {
            'title': title,
            'location': location,
            'price': price,
            'images': images,
            'car_details': car_details,
            'car_features': car_features,
            'seller_comments': seller_comments,
            'link': response.url,
        }

    def extract_title(self, response):
        return response.css('h1::text').get()
    
    def extract_location(self, response):
        return response.css('p.detail-sub-heading a::text').get()

    def extract_price(self, response):
        return response.css('div.price-box strong::text').get()

    def extract_images_links(self, response):
        return response.css('li::attr(data-src)').getall()

    def extract_car_details(self, response):
        car_details = {}
        details_list = response.css('ul#scroll_car_detail li')
        
        for i in range(len(details_list) - 1):
            key = details_list[i].css('li.ad-data::text').get()
            if key:
                value = details_list[i + 1].css('li *::text').getall()
                value = ''.join(value).strip()
                car_details[key.strip()] = value if value else 'N/A'
        
        return car_details

    def extract_car_features(self, response):
        return response.css('ul.list-unstyled.car-feature-list.nomargin li::text').getall()

    def extract_seller_comments(self, response):
        comments_div = response.xpath('//h2[@id="scroll_seller_comments"]/following-sibling::div[1]')
        comments = comments_div.xpath('text()').getall()
        comments = [comment.strip() for comment in comments if comment.strip()]
        return comments

    def extract_description(self, response):
        return response.css('div.description-content p::text').getall()

    def extract_features(self, response):
        return response.css('ul.feature-list li::text').getall()

