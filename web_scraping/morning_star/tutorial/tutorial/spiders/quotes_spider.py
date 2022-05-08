from textwrap import indent
import scrapy
import re
import json
import os

#Use Scrapy Shell
#scrapy shell 'http://financials.morningstar.com/finan/financials/getKeyStatPart.html?t=XNAS:GOOGL&region=usa&culture=en-US&order=asc'

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    data_directory='C:\\Users\\mabalder\\Desktop\\code_projects\\Projects\\jupyterlab\\jupyter_notebooks\\Data\\fundamental_analysis\\ticker_ratios\\'
    tickers_symbols = ['V','TMUS','GOOGL','VOO']        

    def start_requests(self):
        
        for symbol in self.tickers_symbols:
            ratio_url='http://financials.morningstar.com/finan/financials/getKeyStatPart.html?&t='+symbol+'&region=usa&culture=en-US'
            metric_url='http://financials.morningstar.com/valuate/current-valuation-list.action?=&t='+symbol
            
            item=dict()
            item['ticker']=symbol
            yield scrapy.Request(url=ratio_url, callback=self.parse_ratios,meta={'item':item,'metricURL':metric_url})


    def parse_ratios(self, response):
        general_dict=response.meta['item']
        metric_url=response.meta['metricURL']
        ratios_dict={} 
        financial_ratios_names=response.xpath("//tbody/tr/th/text()").getall()
        #Creating dictionary with ratios names and values
        for ratio_name in financial_ratios_names:
            name_sq=ratio_name.replace('\'','')
            ratios_dict[name_sq]=response.xpath(f"//th[text()='{name_sq}']/../td[last()]/text()").get()
        general_dict['ratios']=ratios_dict

        yield scrapy.Request(url=metric_url, callback=self.parse_metrics,meta={'item':general_dict})
        
    def parse_metrics(self, response):
        general_dict=response.meta['item']
        metrics_dict={}
        metrics_names=response.xpath("//tbody/tr/th/text()").getall()[:-1]
        for metric_name in metrics_names:
            name_sq=metric_name.replace('\'','')
            metrics_value=response.xpath(f"//th[text()='{name_sq}']/../td[4]/text()").get()
            metrics_dict[name_sq]=metrics_value
        general_dict['metrics']=metrics_dict

        with open(self.data_directory+general_dict['ticker']+'.json', 'w') as fp:
                json.dump(general_dict, fp,indent=4)
        return general_dict
        