import scrapy

from .constants import CAR_INSPECTED_DATE, CAR_OVERALL_RATING, CAR_GRADE


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
            if (
                (key := detail_element.css('::text').get()) and
                (value := detail_element.xpath('following-sibling::li[1]//text()').get())
            ):
                car_details[key.strip()] = value.strip()

        return car_details

    def extract_car_features(response):
        return response.css('ul.list-unstyled.car-feature-list.nomargin li::text').getall()

    def extract_car_seller_comments(response):
        seller_comments = response.css('#scroll_seller_comments ~ div ::text').getall()
        return seller_comments

    def extract_inspection_report(response):
        car_inspection_report = {}
        
        if car_inspected_date := response.css('div.carsure-detail-header.clearfix p.generic-gray::text').get():
            car_inspection_report[CAR_INSPECTED_DATE] = car_inspected_date.strip()

        if overall_rating := response.css(
            'div.carsure-detail-header.clearfix div.right.pull-right.primary-lang::text'
        ).get():
            car_inspection_report[CAR_OVERALL_RATING] = overall_rating.strip()

        if grade := response.css('div.right.mt0::text').get():
            car_inspection_report[CAR_GRADE] = grade.strip()

        for detail in response.css('ul.carsure-bar-outer.carsure-bar-show.list-unstyled.clearfix li'):
            if (
                (key := detail.css('p::text').get()) and 
                (value := detail.css('div.bar-count.pull-right::text').get())
            ):
                car_inspection_report[key.strip()] = value.strip()

        return car_inspection_report
