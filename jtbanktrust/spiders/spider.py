import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import JjtbanktrustItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class JjtbanktrustSpider(scrapy.Spider):
	name = 'jtbanktrust'
	start_urls = ['http://jtbanktrust.com/news']

	def parse(self, response):
		post_links = response.xpath('//h1[@class="article-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//time/@datetime').get().split('T')[0]
		title = response.xpath('(//h1)[last()]/text()').get()
		content = response.xpath('//div[@class="field-item even"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=JjtbanktrustItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
