# -*- coding: utf-8 -*-
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re
import time
from PIL import Image
from ArticleSpider.env import zhihu_account

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookie.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
header = {
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    'User-Agent': agent,
}


def is_login():
    #通过个人中心页面返回的状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True
    pass

def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def get_captcha():
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg", "wb") as f:
        f.write(t.content)
        f.close()

    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n>")
    return captcha


def zhihu_login(account_password):
    account = account_password[0]
    password = account_password[1]

    #知乎登录
    if re.match("^(13[0-9]|14[5|7]|15[0-9]|18[0-9])\d{8}$", account):
        print("手机号码登录:")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha(),
        }
    elif re.match("^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", account):
        print("邮箱登录:")
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "_xsrf": get_xsrf(),
            "email": account,
            "password": password,
            "captcha": get_captcha(),
        }

    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()


if is_login():
    # get_index()
    print('登录成功')
else:
    print('尚未登录，登录中...')
    zhihu_login(zhihu_account())
