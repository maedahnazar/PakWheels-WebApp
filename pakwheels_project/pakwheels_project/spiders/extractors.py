import scrapy


class PakWheelsExtractor:
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
        car_detail_elements = response.css('#scroll_car_detail li.ad-data')
        for detail_element in car_detail_elements:
            key = detail_element.css('::text').get()
            value = detail_element.xpath('following-sibling::li[1]//text()').get()
            if key and value:
                car_details[key.strip()] = value.strip()
        return car_details

    def extract_car_features(self, response):
        return response.css('ul.list-unstyled.car-feature-list.nomargin li::text').getall()

    def extract_seller_comments(self, response):
        seller_comments = response.css('#scroll_seller_comments ~ div')
        return seller_comments.css('::text').getall()

    def extract_inspection_report(self, response):
        inspection_report = {}
        inspected_date = response.css('div.carsure-detail-header.clearfix p.generic-gray::text').get()
        overall_rating = response.css('div.carsure-detail-header.clearfix div.right.pull-right.primary-lang::text').get()
        grade = response.xpath('//div[@class="carsure-detail-header clearfix"]/h3[contains(text(), "Grade")]/following-sibling::span/text()').get()

        if inspected_date:
            inspection_report['Inspected Date'] = inspected_date.strip()
        if overall_rating:
            inspection_report['Overall Rating'] = overall_rating.strip()
        if grade:
            inspection_report['Grade'] = grade.strip()

        additional_details = response.css('ul.carsure-bar-outer.carsure-bar-show.list-unstyled.clearfix li')
        for detail in additional_details:
            key = detail.css('p::text').get()
            value = detail.css('div.bar-count.pull-right::text').get()
            if key and value:
                inspection_report[key.strip()] = value.strip()

        return inspection_report
