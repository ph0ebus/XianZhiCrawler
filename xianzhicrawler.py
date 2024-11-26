#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ph0ebus
# @Software: PyCharm
import json
import re, time
import tomd
import os
from selenium import webdriver
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start', type=int, help="page num of newest article")
parser.add_argument('end', type=int, help="page num of last article")
args = parser.parse_args()

def convert(regex: str, new: str, src: str):
    return re.sub(regex, new, src, 0, re.MULTILINE)


def format_md(s: str):
    regex = r"\[<"
    t = convert(regex, r"![<", s)
    regex = r"(<pre>)|(</pre>)"
    t = convert(regex, "\n```\n", t)
    regex = r"<li>"
    t = convert(regex, "1. ", t)
    regex = r"</li>"
    t = convert(regex, "", t)
    return t


def replace_link(src: str, title: str):
    regex = r"<img src=\"(.*)\">"
    img_links = re.findall(regex, src, re.MULTILINE)
    base_dir = title + ".assets"
    dir_name = output_dir + "/" + base_dir
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    count = 0
    total = len(img_links)
    headers = {
        "User-Agent": r'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36''',
        "Referer": "https://xz.aliyun.com/"
    }
    for link in img_links:
        print(f"\r\t\033[33m[+] Downloading images ...{count + 1}/{total}\033[0m", end="")
        if not link.startswith("http"):
            count += 1
            continue
        r = requests.get(url=link, headers=headers, verify=False)
        time.sleep(0.1)
        basename = f"image-{count}.png"
        f = open(f"{dir_name}/{basename}", "wb")
        f.write(r.content)
        f.close()

        ref = r'<img src="' + link + r'">'
        src = src.replace(ref, f"image-{count}")
        src = src.replace(link, f"{base_dir}/{basename}")

        count += 1
    return src


def generate_md(article, num):
    print(f"\033[32m[+] Getting: {article}\033[0m")
    driver.get(article)
    time.sleep(1)
    source = driver.page_source
    if '滑动验证页面' in source:
        print(article)
        return 2

    if '页面找不到了(´･ω･`)' in source and '400 - 先知社区' in source:  # 防止无效的404页面
        return 1

    title = driver.title
    title = title[:title.rfind("-")]
    front_template = f'---\ntitle: {title}\n---\n'
    title = title.replace('"', "'").replace("?", "-").replace("<", "-").replace(">", "-").replace("/", "-").replace(
        "\\", "-").replace(":", "-").replace("*", "-").replace("|", "-")
    title = title.strip()
    title = f"{num}-{title}"
    pattern = "(?s)<div id=\"topic_content\" class=\"topic-content markdown-body\">(.*)<div class=\"post-user-action\" style=\"margin-top: 34px;\">"
    pattern = re.compile(pattern)
    match = pattern.findall(source)
    content = match[0]
    content = re.findall(r'(?s)(.*)</div>', content)[0]
    if isinstance(content, str):
        content = content.strip()
    file_name = output_dir + "/" + title + ".md"
    md = tomd.convert(content)
    md = format_md(md)
    md = front_template + md
    md = replace_link(md, title)
    f = open(file_name, "w", encoding="utf-8")
    f.write(md)
    print("\n\033[32m[*] Done\033[0m")
    f.close()
    return 0


chrome_options = webdriver.ChromeOptions()
output_dir = "output"
headers_list = '''Connection: keep-alive
sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9'''.split("\n")

headers_dict = {header.split(":")[0]: ':'.join(header.split(":")[1:]).strip() for header in headers_list}
cookie_list = open("./cookie.txt", encoding="utf-8").read().split(";")  # 切换为自己的cookie
cookie_dict = {cookie.strip().split("=")[0]: ("=".join(cookie.strip().split("=")[1:])) for cookie in cookie_list}
# print(cookie_dict)
for key, value in headers_dict.items():
    chrome_options.add_argument(f"{key}={value}")

from selenium.webdriver.chrome.service import Service

chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--no-sandbox')
s = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get("https://xz.aliyun.com/")

for key, value in cookie_dict.items():
    cookie = {"name": key, "value": value, "domain": ".aliyun.com"}
    # print(cookie)
    driver.add_cookie(cookie_dict=cookie)


print(f"start: {args.start} end: {args.end}")
for num in range(args.start, args.end, -1):
    status_code = generate_md('https://xz.aliyun.com/t/%d' % num, num)
    if status_code == 2:
        break
    elif status_code == 1:
        print("404 not found")
        continue

print("error exit")
time.sleep(10)
