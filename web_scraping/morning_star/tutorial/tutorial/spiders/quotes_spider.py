import scrapy
import re
import json
import os

#Use Scrapy Shell
#scrapy shell 'http://financials.morningstar.com/finan/financials/getKeyStatPart.html?t=XNAS:GOOGL&region=usa&culture=en-US&order=asc'

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        tickers = ['GOOGL']
        ticker_data={}
        for ticker in tickers:
            ticker_data[ticker]={}
            ratio_url='http://financials.morningstar.com/finan/financials/getKeyStatPart.html?&t='+ticker+'&region=usa&culture=en-US'
            metric_url='http://financials.morningstar.com/valuate/current-valuation-list.action?=&t='+ticker
            
            ratios=scrapy.Request(url=ratio_url, callback=self.parse_ratios,cb_kwargs=dict(ticker_name=ticker))
            #ticker_data[ticker]['ratios']=yield scrapy.Request(url=ratio_url, callback=self.parse_ratios) #, cb_kwargs=dict(ticker_name=ticker))         
            #print(ticker_data[ticker]['ratios'])
            #ticker_data[ticker]['metrics']=yield scrapy.Request(url=metric_url, callback=self.parse_metrics) #, cb_kwargs=dict(ticker_name=ticker))
            #print(ticker_data[ticker]['metrics'])
            #yield scrapy.Request(url=ratio_url, callback=self.parse_metrics(ticker))
            #Creating json files to store ratios

            yield ratios

    def parse_ratios(self, response, ticker_name):
        ratios_dict={}
        #Extracting tickers name from the response url
        #ticker_name=ticker_name#re.split("=|&",response.url)[2]
        #Extracting ratios names and values 
        financial_ratios_names=response.xpath("//tbody/tr/th/text()").getall()
        #Creating dictionary with ratios names and values
        for ratio_name in financial_ratios_names:
            name_sq=ratio_name.replace('\'','')
            ratios_dict[name_sq]=response.xpath(f"//th[text()='{name_sq}']/../td[last()]/text()").get()

        data_directory='C:\\Users\\mabalder\\Desktop\\code_projects\\Projects\\jupyterlab\\jupyter_notebooks\\Data\\fundamental_analysis\\ticker_ratios\\'
        json_file=open(data_directory+ticker_name+".json","w")
        #temporal_file=open(os.getcwd()+'\\scrapped_data\\'+ticker_name+".json","w")
        
        json.dump(ratios_dict,json_file) 
          
        yield ratios_dict
        
    def parse_metrics(self, response):
        metrics={}
        #Extracting tickers name from the response url
        #ticker_name=ticker#re.split("=|&",response.url)[2]
        #Extracting ratios names and values 
        #financial_ratios_names=response.xpath("//div[@id='\\\"tab-financial\\\"']//tbody/tr/th/text()").getall()[:24]
        metrics_names=response.xpath("//tbody/tr/th/text()").getall()[:-1]
        #financial_ratios_values= response.xpath("//div[@id='\\\"tab-financial\\\"']//tbody/tr/td[last()]/text()").getall()[:24]
        #Creating dictionary with ratios names and values
        for metric_name in metrics_names:
            name_sq=metric_name.replace('\'','')
            metrics_value=1#response.xpath(f"//th[text()='{name_sq}']/../td[last()]/text()").get()
            metrics[name_sq]=metrics_value
            yield dict(name_sq = metrics_value)
        
        
       
        #Creating json files to store ratios
        #data_directory='C:\\Users\\mabalder\\Desktop\\code_projects\\Projects\\jupyterlab\\jupyter_notebooks\\Data\\fundamental_analysis\\ticker_ratios\\'
        #json_file=open(data_directory+ticker_name+".json","w")
        #temporal_file=open(os.getcwd()+'\\scrapped_data\\'+ticker_name+".json","w")
        #json.dump(ratios,json_file)                    
