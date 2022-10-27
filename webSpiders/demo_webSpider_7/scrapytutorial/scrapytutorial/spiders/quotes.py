import scrapy
from scrapytutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # 每个项目唯一的名字，用来区分不同的Spider
    allowed_domains = ['quotes.toscrape.com']  # 允许爬取的域名
    start_urls = ['https://quotes.toscrape.com/']  # 包含Spider在启动时爬取的URL列表（初始请求）

    def parse(self, response):
        """
        负责解析返回的响应、提取数据或进一步生产要处理的请求
        :param response: 请求start_urls里的URL后得到的响应
        :return:
        """
        quotes = response.css('.quote')  # 使用CSS或XPath进行筛选
        for quote in quotes:
            item = QuoteItem()  # 实例化Item（类）
            # 使用::text来获取文本内容（列表），使用extract_first()来获取列表中的第一个元素，使用extract()来获取整个列表
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)  # 由于之后页面结构相同，故回调方法仍可指定为当前parse方法
