import scrapy
from ios.items import IosItem
from scrapy import Request, Selector
from scrapy.http import HtmlResponse


class AppscrapySpider(scrapy.Spider):
    name = "appscrapy"
    allowed_domains = ["apps.apple.com"]
    start_urls = ["http://apps.apple.com/"]

    def start_requests(self):
        # alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','#']
        alphabet = ['A', 'B']
        for letter in alphabet:
            for i in range(1, 3):
                yield Request(url=f'https://apps.apple.com/ie/genre/ios-books/id6018?letter={letter}&page={i}#page', )

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        poisition = ['.first', '', '.last']
        for i in range(3):
            list_items = sel.css(f'#selectedcontent > div.column{poisition[i]} > ul > li')
            for list_item in list_items:
                detail_url = list_item.css('a::attr(herf)').extract_first()
                app_item = IosItem()
                app_item['name'] = list_item.css('a::text').extract_first()
                # yield app_item
                yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': app_item})

    def parse_detail(self, response, **kwargs):
        app_item = kwargs['item']
        sel = Selector(response)

        app_item = IosItem()
        app_item['provider'] = sel.css('span[class="app-privacy__developer-name"]::text').extract_first()
        app_item['link'] = sel.css('h3[class="privacy-type__heading"]::text').extract()
        app_item['rate'] = sel.css('span[class="we-customer-ratings__averages__display"]::text').extract_first()
        app_item['size'] = float(
            sel.css('dd.information-list__item__definition[aria-label*=megabytes]::text').get().split()[0])
        app_item['price'] = sel.css(
            'li[class="inline-list__item inline-list__item--bulleted app-header__list__item--price"]::text').extract_first()
        app_item['age'] = sel.xpath(
            '//dd[contains(@class, "information-list__item__definition") and preceding-sibling::dt[text()="Age Rating"]]//text()').extract_first().strip()

        app_item['inpurchases'] = sel.css(
            'span[class="truncate-single-line truncate-single-line--block"]::text').extract_first()

        linktype = response.xpath(
            '//h3[contains(text(), "Data Linked to You")]/ancestor::div[@class="app-privacy__card"]')
        app_item['linktype'] = linktype.css('.privacy-type__data-category-heading::text').extract()

        notlinkedtype = response.xpath(
            '//h3[contains(text(), "Data Not Linked to You")]/ancestor::div[@class="app-privacy__card"]')
        app_item['notlinkedtype'] = notlinkedtype.css('.privacy-type__data-category-heading::text').extract()

        tracktype = response.xpath(
            '//h3[contains(text(), "Data Used to Track You")]/ancestor::div[@class="app-privacy__card"]')
        app_item['tracktype'] = tracktype.css('.privacy-type__data-category-heading::text').extract()

        yield app_item
