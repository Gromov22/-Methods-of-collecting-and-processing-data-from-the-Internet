import scrapy
from scrapy.http import HtmlResponse
from mvideo_parsing.items import MvideoParsingItem


class DromSpider(scrapy.Spider):
    name = "drom"
    allowed_domains = ["drom.ru"]
    start_urls = ["https://auto.drom.ru/all/?multiselect[]=2_105_9_1&multiselect[]=2_105_10_all&multiselect["
                  "]=2_105_11_all"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-ftid="component_pagination-item-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        car_link = response.xpath("//a[@data-ftid='bulls-list_bull']/@href").getall()
        for link in car_link:
            yield response.follow(link, callback=self.parse_link)

    def parse_link(self, response: HtmlResponse):
        car_link = response.url
        car_name = response.xpath('//h1/span/text()').getall()
        car_price = response.xpath('//div[@class="css-eazmxc e162wx9x0"]/text()').getall()
        car_price.remove(car_price[1])
        car_price[0] = car_price[0].replace('\xa0', ' ')

        descr_dom = response.xpath('//table[@class="css-xalqz7 eppj3wm0"]')
        for i in descr_dom:
            car_engine = i.xpath('.//tr/td/span/text()')[0].getall()
            car_power = [val.replace('\xa0', '') for val in
                         i.xpath('.//span[@class="css-9g0qum e162wx9x0"]/text()').getall()]
            car_power.pop(2)
            car_transmission = i.xpath('.//tr/td/text()')[0].get()
            car_drive = i.xpath('.//tr/td/text()')[1].get()
            car_body = i.xpath('.//tr/td/text()')[2].get()
            car_color = (
                i.xpath('.//tr/td/text()')[3].get() if i.xpath('.//tr/td/text()')[3].get() != 'левый'
                                                       and i.xpath('.//tr/td/text()')[3].get() != 'правый' else None)
            car_mileage = [val.replace('\xa0', '') for val in i.xpath('.//tr/td/span/text()')[4].getall()]
            car_steering_wheel = (
                i.xpath('.//tr/td/text()')[4].get() if len(i.xpath('.//tr/td/text()').getall())
                                                       >= 5 else i.xpath('.//tr/td/text()')[3].get())
            car_generation = (
                i.xpath('.//tr/td/a/text()')[0].getall() if len(i.xpath('.//tr/td/a/text()').getall())
                                                            > 0 else i.xpath('.//tr/td/text()')[-1].get())
            car_equipment = (
                i.xpath('.//tr/td/a/text()')[1].getall() if len(i.xpath('.//tr/td/a/text()').getall()) > 1 else None)

            yield MvideoParsingItem(
                name=car_name,
                price=car_price,
                engine=car_engine,
                power=car_power,
                transmission=car_transmission,
                drive=car_drive,
                body=car_body,
                color=car_color,
                mileage=car_mileage,
                steering_wheel=car_steering_wheel,
                generation=car_generation,
                equipment=car_equipment,
                link=car_link
            )


