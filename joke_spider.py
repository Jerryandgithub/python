# coding=utf-8
from User_Agent_list import ua_list
import requests
import re
import time
import os
import chardet


class Joke(object):
    """
    spider for joke web
    """
    def __init__(self, start_page, end_page):
        """initialize nature"""
        # start_url : http://www.mikcai.com/article/list_5_1.html
        self.base_url = "http://www.mikcai.com/article/list_5_" 
        self.extract = re.compile(r'<div class="f18 mb20">(.*?)</div>', re.S)
        self.start_page = start_page
        self.end_page = end_page
        self.screen_str = re.compile(r"&hellip;|<p>|&ldquo;|<br />|&rdquo;|</p>|\s")
    
    def get_html(self, url):
        """
        get html
        """
        headers = {"User-Agent": ua_list()}
        response = requests.get(url, headers=headers)
        response = response.content
        response = response.decode("gbk")
        return response.encode("utf-8")
    
    def clean_html(self, html):
        """clean html"""
        data = self.extract.findall(html)
        index = 0
        for info in data:
            data[index] = self.screen_str.sub("", info)
            index += 1

        return data
    
    def put_data(self, data):
        """
        write in text
        """
        with open("joke.txt", "ab") as f:
            f.write("第" + str(self.start_page) + "页\n\n")
            for info in data:
                f.write(info + "\n")
            f.write("\n\n\n")
        return

    def main(self):
        """control center"""

        # 1.get url_web
        while self.end_page >= self.start_page:
            url = self.base_url + str(self.start_page) + ".html"
            
            # 2.use re for data
            html = self.get_html(url)

            # 3.cleanout data
            data = self.clean_html(html)
            
            # 4.put data
            self.put_data(data)
            
            # 5.stick up for page
            self.start_page += 1
            
            # 6.防止服务器压力过大
            time.sleep(3)

        print "任务完成"


if __name__ == "__main__":
    """
    start spider
    """
    start = int(input("输入开始页"))
    end = int(input("输入结束页"))
    joke = Joke(start, end)
    joke.main()


