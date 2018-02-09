# -*- coding: utf-8 -*
from bs4 import BeautifulSoup
import traceback

class HtmlParser(object):

    # 解析器
    def parser(self,page_url,html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'lxml')
        new_urls = self._get_new_urls(soup)
        return new_urls

    # 爬取url
    def _get_new_urls(self,soup):
        new_urls = set()
        news_list = soup.find('div', class_='newsList').find_all('li')
        for link in news_list:
            new_url = link.find('a').get('href')
            new_urls.add(new_url)
        return new_urls
    # 爬取时间和标题
    def get_data(self,page_url,soup):
        data = {}
        try:
          data['url'] = page_url
          h1=soup.find('h1')
          data['title'] =h1.get_text()
          pList = soup.find('div', id='main_content').find_all('p')
          data['content']=''
          for p in pList:
              str = p.get_text()
              data['content']=data['content']+str
              data['keyword'] = '测试中》》》'
              data['time'] = soup.find('span', class_='ss01').get_text()
              data['from'] = soup.find('span', class_='ss03').find('a').get_text()
        except Exception as e:
              data['from'] = soup.find('span', class_='ss03').get_text()
        finally:
          return data

