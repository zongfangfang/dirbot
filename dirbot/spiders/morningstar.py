from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy
from dirbot.items import Website


class DmozSpider(Spider):
    name = "morningstar"
    allowed_domains = ["cn.morningstar.com"]
    start_urls = [
        "http://cn.morningstar.com/fundselect/default.aspx?star=5",
    ]

    def parse(self, response):
        for href in response.xpath('//table[@id="ctl00_cphMain_gridResult"]/tr/td[3]/a/@href').extract():
            url = response.urljoin(href)#"http://cn.morningstar.com",
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sites=response.xpath('//table[@id="ctl00_cphMain_gridResult"]/tr/td[3]')
        # sites = response.css('#site-list-content > div.site-item > div.title-and-desc')
        items = []

        for site in sites:
            item = Website()
            item['name'] = site.xpath(
                'a/text()').extract()
            item['url'] = site.xpath(
                'a/@href').extract()
            item['description'] = site.css(
                'a/@target').extract()
            items.append(item)

        return items
