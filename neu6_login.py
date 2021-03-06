# -*- coding: utf-8 -*-
# author: Chan

import requests
from bs4 import BeautifulSoup

url_start = 'http://bt.neu6.edu.cn/member.php?mod=logging&action=login&referer=http%3A%2F%2Fbt.neu6.edu.cn%2Fforum.php'
url_login = 'http://bt.neu6.edu.cn/'
url_main = 'http://bt.neu6.edu.cn/forum.php'
url_test = 'http://bt.neu6.edu.cn/home.php?mod=spacecp'


class neu6():
    def __init__(self, username, password):
        headers = {
            "Accept": "text/html, application/xhtml+xml, application/xml",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN, zh",
            "Cache-Control": "max-age = 0",
            "Connection": "keep-alive",
            "Host": "bt.neu6.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0Win64x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.username = username
        self.password = password

        r = self.session.get(url_start)
        soup = BeautifulSoup(r.content, 'html.parser')
        self.formhash = soup.find("input", {"name": "formhash"})["value"]
        # print (self.formhash)
        self.action = soup.find("form")["action"]
        # print(self.action)

    def login(self):
        try:
            formdata = {
                "formhash": self.formhash,
                "referer": url_main,
                "username": self.username,
                "password": self.password,
                "questionid": "0",
                "answer": ""
            }
            self.session.post(url_login+self.action+'&inajax=1', data=formdata)
            r1 = self.session.get(url_main)
        except:
            print("登录失败")

    def info(self):
        try:
            r2 = self.session.get(url_main)
            soup = BeautifulSoup(r2.content, 'html.parser')
            name = soup.find_all("strong", {"class": "vwmy"})[0].get_text()
            points = soup.find_all("a", {"class": "showmenu"})[
                0].get_text().strip()
            level = soup.find_all("a", {"class": "xi2"})[
                0].get_text().strip()
            print("用户名:", name)
            print(points)
            print("用户组:", level)
        except:
            print("获取信息失败")


def main():
    neu = neu6('username', 'passowrd')
    neu.login()
    neu.info()


if __name__ == '__main__':
    main()
