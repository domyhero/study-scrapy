# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from ArticleSpider.env import zhihu_account
from PIL import Image


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    headers = {
        'Host': "www.zhihu.com",
        'Referer': "https://www.zhihu.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/', headers=self.headers, callback=self.login)]

    def login(self, response):
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            account, password = zhihu_account()

            post_data = {
                "_xsrf": xsrf,
                "email": account,
                "password": password,
                "captcha": "",
            }

            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(
                captcha_url, headers=self.headers, meta={"post_data": post_data}, callback=self.login_after_captcha
            )

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get('post_data', {})
        post_url = "https://www.zhihu.com/login/email"
        post_data['captcha'] = captcha

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login,
        )]

    def check_login(self, response):
        #验证服务器的返回数据判断是否成功
        result_json = json.loads(response.body)
        pass
