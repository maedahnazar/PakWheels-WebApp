import scrapy


class PakWheelsExtractor:
    def extract_title(response):
        return response.css('h1::text').get()
    
    def extract_location(response):
        return response.css('p.detail-sub-heading a::text').get()

    def extract_car_price(response):
        return response.css('div.price-box strong::text').get()

    def extract_car_images_links(response):
        return response.css('li::attr(data-src)').getall()

    def extract_car_details(response):
        car_details = {}

        for detail_element in response.css('#scroll_car_detail li.ad-data'):
            if key := detail_element.css('::text').get():
                if value := detail_element.xpath('following-sibling::li[1]//text()').get():
                    car_details[key.strip()] = value.strip()

        return car_details

    def extract_car_features(response):
        return response.css('ul.list-unstyled.car-feature-list.nomargin li::text').getall()

    def extract_car_seller_comments(response):
        seller_comments = response.css('#scroll_seller_comments ~ div')
        return seller_comments.css('::text').getall()

    def extract_inspection_report(response):
        car_inspection_report = {}
        
        if inspected_date := response.css('div.carsure-detail-header.clearfix p.generic-gray::text').get():
            car_inspection_report['Inspected Date'] = inspected_date.strip()

        if overall_rating := response.css(
            'div.carsure-detail-header.clearfix div.right.pull-right.primary-lang::text'
        ).get():
            car_inspection_report['Overall Rating'] = overall_rating.strip()

        if grade := response.xpath(
            '//div[@class="carsure-detail-header clearfix"]/h3[contains(text(), "Grade")]'
            '/following-sibling::span/text()'
        ).get():
            car_inspection_report['Grade'] = grade.strip()

        for detail in response.css('ul.carsure-bar-outer.carsure-bar-show.list-unstyled.clearfix li'):
            if key := detail.css('p::text').get():
                if value := detail.css('div.bar-count.pull-right::text').get():
                    car_inspection_report[key.strip()] = value.strip()

        return car_inspection_report
    