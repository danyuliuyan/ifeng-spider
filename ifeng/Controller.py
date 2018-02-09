# -*- coding: utf-8 -*
from ifeng.HtmlParser import HtmlParser
from ifeng.UrlManager import UrlManager
from ifeng.HtmlDownLoader import HtmlDownLoader
from ifeng.DataOutput import DataOutput
from bs4 import BeautifulSoup
import traceback,pymysql
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Controller(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownLoader()
        self.parser = HtmlParser()
        self.output = DataOutput()
        self.options = Options()
        self.options.add_argument('-headless')
        self.driver = webdriver.Firefox(executable_path='geckodriver',firefox_options=self.options)

    # 下一页
    def get_next_page(self,url):
        next_page = ''
        current_html_content = self.downloader.download(url)
        soup = BeautifulSoup(current_html_content,'lxml')
        try:
           m_page_div = soup.find('div',class_='m_page').find_all('span')
           if len(m_page_div)>=2:
               a_link = m_page_div[1]
               link = a_link.find('a').get('href')
               next_page =link

           else:
               single = soup.find('div', class_='m_page').find('span').find('a')
               temp = single.get_text()
               if temp == '下一页 ':
                   next_page = single.get('href')
        except Exception as e:
           next_page = ''
           print(e)
        finally:
            print(next_page)
            return next_page

    # 爬取入口
    def get_news_list(self,root_url):
        # 入口URL
        self.manager.add_new_url(root_url)
        try:
            new_url = self.manager.get_new_url()
            html = self.downloader.download(new_url)
            new_urls = self.parser.parser(new_url,html)
            self.manager.add_new_urls(new_urls)
            print("获取到了%d个链接" % self.manager.new_urls_size())
            self.crawl_data(new_urls)
        except Exception as e:
                traceback.print_exc(e)
        return html
    #二级内容爬取
    def crawl_data(self,urls):
        if urls is not None:
            for url in urls:
                self.driver.get(url)
                html = self.driver.page_source
                soup = BeautifulSoup(html,'lxml')
                data = self.parser.get_data(url,soup)
                print(url+' is OK!')
                self.insert(data)
        self.output.output_html()

    def insert(self,data):
        db = pymysql.connect('localhost','root','zhangyanping','ifeng',charset='utf8')
        cursor = db.cursor()
        if 'content' in data.keys() and 'from' in data.keys() and 'keyword' in data.keys() and 'time' in data.keys():
            sql = r'insert into ifeng_news(url,title,content,keyword,afrom,atime)VALUES("%s","%s","%s","%s","%s","%s")'%\
                   (data['url'],data['title'],data['content'],data['keyword'],data['from'],data['time'])
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                traceback.print_exc(e)
                db.rollback()
            db.close()
if __name__ == '__main__':
      Controller = Controller()
      root_url_list = []
      next_page1 = r'http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml'
      root_url_list.append(next_page1)
      while True:
          next_page = Controller.get_next_page(next_page1)
          next_page1 = next_page
          if next_page1:
              root_url_list.append(next_page1)
          else:
              break
      for root_url in root_url_list:
          Controller.get_news_list(root_url)
