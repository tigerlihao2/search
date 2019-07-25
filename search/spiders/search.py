# -*- coding: utf-8 -*-
import scrapy
import re
from search.items import SearchItem


class SearchSpider(scrapy.Spider):
	name = 'search'
	
	def __init__(self):
		self.count = 0
	
	start_urls = [
		'https://yandex.ru/news/',
#		'https://mail.ru',
#		'https://spbdnevnik.ru/news/2019-07-24/',
#		'https://news.yandex.ru/yandsearch?text=поклонская&rpt=nnews2&grhow=clutop',
		]



	def parse(self, response):
		self.count += 1		
		print("\n第%d个网页, 网址%s"%(self.count, response.url))
		
		# 检查本页的内容，是否含有关键词。
		ls = response.xpath('//text()').extract()
		mark = 0
		for s in ls:
			if 'кита' in s.lower():
				mark = 1
				break
		
		# 如果mark == 1，则说明本页上有关键词。
		if mark == 1:
			item = SearchItem()
			item['site'] = response.url
			yield item
		
		# 如果第一级url超过5个，就不再找了，只找下级的url。
		if self.count < 3 :
			next_pages = response.xpath('//a/@href').extract()
			if len(next_pages) > 0 :
				for link in next_pages:
					# 如果是http开头，则直接使用该链接，是外网链接。
					if re.match('http',link):
						yield scrapy.Request(link, callback=self.parse)
					# 如果不是http开头，则需要补充前缀，是本站链接。
					else:
						yield scrapy.Request('https://yandex.ru'+link, callback=self.parse)


