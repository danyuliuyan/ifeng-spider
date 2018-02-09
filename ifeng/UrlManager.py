# -*- coding: utf-8 -*-
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    # 判断是否还有未爬取的URL
    def has_new_url(self):
        return self.new_urls_size() != 0

    # 获取未爬取的URL数量
    def new_urls_size(self):
        return len(self.new_urls)

    # 获取一个未爬取的URL
    def get_new_url(self):
        new_url=self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    # 将新的URL添加到未爬取的URL集合中
    def add_new_url(self,url):
        if url is None:
            return
        else:
            if url not in self.new_urls and url not in self.old_urls:
                self.new_urls.add(url)

    # 添加一个未爬取的url集合
    def add_new_urls(self,urls):
        if urls is None:
            return
        else:
            for url in urls:
                self.new_urls.add(url)

    # 获取已经爬取的URL集合的大小
    def old_urls_size(self):
        return len(self.old_urls)