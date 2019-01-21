# -*- coding: utf-8 -*-
import re

import scrapy

import baidu_stocks.items

class StockInfoSpider(scrapy.Spider):
    name = 'stock_Info'
    # start_urls = ['http://quote.eastmoney.com/stocklist.html']
    headers={
    'Accept - Encoding': 'gzip, deflate, br',
    'Accept - Language': 'zh - CN, zh;q = 0.9',
    'Connection': 'keep - alive',
    'Referer':'https://gupiao.baidu.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    def start_requests(self):
        urls=['http://quote.eastmoney.com/stocklist.html']  #
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_index)


    def parse_index(self, response):  # 获取股票列表
        hrefs = response.css('a::attr(href)').extract()
        # print(len(hrefs))
        for href in hrefs:
            url_index = re.findall(r's[hz]\d{6}', href)
            if url_index:
                 url = 'https://gupiao.baidu.com/stock/' + url_index[0] + '.html'
                 try:
                    yield scrapy.Request(url=url, callback=self.parse_detail, headers=self.headers)
                 except:
                    self.logger.warning('url 异常：' + url)
                    continue


    def parse_detail(self, response): # 获取单个股票具体信息
        self.logger.info(response.url + 'crawling.......')
        try:
            info = response.css('.stock-bets')
            name = info.css('.bets-name::text').extract_first().strip().split()[0]
            key = info.css('dt::text').extract()
            value = info.css('dd::text').extract()
        except:
            self.logger.warning('raise a error, this page maybe no that name above or expression is not true')
            info_dict = {}
            info_dict.update({'id': re.search('s[hz]\d{6}', response.url).group(0)})
            info_dict.update({'name': name})
            for i in range(len(key)):
                info_dict[key[i]] = value[i].strip()
            # self.logger.info('output successfully:  ')
            yield info_dict

