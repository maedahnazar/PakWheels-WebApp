import scrapy

class PakWheelsSpider(scrapy.Spider):
    name = 'pakwheels'
    allowed_domains = ['pakwheels.com']
    start_urls = ['https://www.pakwheels.com/used-cars/search/-/']

    def start_requests(self):
        cookies = {
            "countrycurrency": "PKR",
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_root_url, cookies=cookies)

    def parse_root_url(self, response):
        ad_links = response.css('div.col-md-9.search-listing.pull-right a.car-name.ad-detail-path::attr(href)').getall()
        
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
        inspection_report = self.extract_inspection_report(response)
        
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

    def extract_title(self, response):
        return response.css('h1::text').get()
    
    def extract_location(self, response):
        return response.css('p.detail-sub-heading a::text').get()

    def extract_price(self, response):
        return response.css('div.price-box strong::text').get()

    def extract_images_links(self, response):
        return response.css('div.price-box span.price::text').get()

    def extract_car_details(self, response):
        details = {}
        detail_elements = response.css('#scroll_car_detail li.ad-data')
        for detail_element in detail_elements:
            key = detail_element.css('::text').get()
            value = detail_element.xpath('following-sibling::li[1]//text()').get()
            if key and value:
                details[key.strip()] = value.strip()
        return details

    def extract_car_features(self, response):
        return response.css('ul.list-unstyled.car-feature-list.nomargin li::text').getall()

    def extract_seller_comments(self, response):
        comments_div = response.css('#scroll_seller_comments ~ div')
        return comments_div.css('::text').getall()

    def extract_inspection_report(self, response):
        report = {}
        inspected_date = response.css('div.carsure-detail-header.clearfix p.generic-gray::text').get()
        overall_rating = response.css('div.carsure-detail-header.clearfix div.right.pull-right.primary-lang::text').get()
        grade = response.xpath('//div[@class="carsure-detail-header clearfix"]/h3[contains(text(), "Grade")]/following-sibling::span/text()').get()

        if inspected_date:
            report['Inspected Date'] = inspected_date.strip()
        if overall_rating:
            report['Overall Rating'] = overall_rating.strip()
        if grade:
            report['Grade'] = grade.strip()

        additional_details = response.css('ul.carsure-bar-outer.carsure-bar-show.list-unstyled.clearfix li')
        for detail in additional_details:
            key = detail.css('p::text').get()
            value = detail.css('div.bar-count.pull-right::text').get()
            if key and value:
                report[key.strip()] = value.strip()

        return report
