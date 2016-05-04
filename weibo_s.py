# -*- coding: utf-8 -*-

import requests
import json
import re
from lxml import etree
import logging

__author__ = 'lpe234'


class WeiBoSearchSpider(object):

    weibo_s = 'http://s.weibo.com/weibo/'
    request_headers = {
        'Host': 's.weibo.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://s.weibo.com/',
        'Connection': 'keep-alive',
    }

    def __init__(self, search_text):
        self.search_text = search_text
        self.search_href = self.weibo_s + self.search_text
        logging.basicConfig(level=logging.DEBUG)

    def do_request(self, search_href):
        """ 获取url内容 """
        resp = requests.get(search_href, headers=self.request_headers)
        if resp.status_code != 200:
            logging.error('request error: {}'.format(resp.status_code))
            return None
        return resp.content

    def analyse_content(self, content):
        """ 分析网页中的数据 """
        html = etree.HTML(content)
        # 微博搜索页使用JS加载内容
        scripts_nodes = html.xpath('//script/text()')
        weibo_text = None
        for node in scripts_nodes:
            if '"pid":"pl_weibo_direct"' in node:
                weibo_text = node
                break

        # 这块有些啰嗦. 需要看网页html分析才可
        if weibo_text:
            weibo_text = re.findall(r'\((.*)\)', str(weibo_text))
            if weibo_text:
                weibo_data = json.loads(weibo_text[0])
                weibo_html = weibo_data.get('html')
                if weibo_html:
                    weibo_html_ = etree.HTML(weibo_html)
                    weibo_nodes = weibo_html_.xpath('//div[contains(@class, "WB_cardwrap")]')
                    for wnode in weibo_nodes:
                        mid = wnode.xpath('./div[@mid]/@mid')
                        author_title = wnode.xpath('.//div[@class="face"]/a/@title')
                        author_href = wnode.xpath('.//div[@class="face"]/a/@href')
                        author_avatar = wnode.xpath('.//img[@class="W_face_radius"]/@src')
                        content = wnode.xpath('.//p[@class="comment_txt"]//text()')
                        medias = wnode.xpath('.//img/@src')
                        print ''.join(mid), ''.join(author_title), ''.join(author_href), ''.join(author_avatar), \
                            ''.join(content), ', '.join(medias)

    def save_data(self):
        """ 数据保存 """
        pass

    def run(self):
        """ 进行实际获取数据 """
        content = self.do_request(self.search_href)
        self.analyse_content(content)


if __name__ == '__main__':
    wbss = WeiBoSearchSpider('足球')
    wbss.run()

