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


def convert(regex: str, new: str, src: str):
    # print("regex: ", regex)
    # print("new: ", new)
    # print("src: ", src)
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
        # re_link = convert(r"\.", "\\.", link)
        # re_link = convert(r"\-", "\\-", re_link)
        ref = r'<img src="' + link + r'">'
        src = src.replace(ref, f"image-{count}")
        src = src.replace(link, f"{base_dir}/{basename}")
        # print("re_link: ",re_link)
        # ref = r'<img src=\"' + re_link + r'\">'
        # src = convert(ref, f"image-{count}", src)
        # src = convert(re_link, f"{base_dir}/{basename}", src)
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
cookie_list = "_c_WBKFRo=GWapfH2U4VUvfwONiRto0bcrXXlNYsqgkHxE9iQI; _nb_ioWEgULi=; acw_tc=1a0c39d417322411578572458e0035d3925ef328a5ab9bbe8f096fb5b6ff58; acw_sc__v3=673fe7117cec4c83f9aa588fa80aee30719f7477; tfstk=fgUDrX1P4oofVPxoZgufblj3zUI8GIgsqRLtBVHN4YkWBCFNc1bgMWmtbtgYS8VIFj-Z3mRyGz2HWEBfc58iWVWdpwQLGS3s79LbCsKthfNrQLGhnuFj5VWRpwQLGSwEN8LDsV5ozfhHbVoqb35o9fgwuc824LkSUAuZ7RPPZfMrQb650xaazzWYusKXDHKLrjWsLSDoNbaoimDFRYYaMzcmmvP4kQM3Ebz8rDnJ6T0zOueqZ2bDdjqztqlg56-iIc4jrfq5nne3hfPrq-C9fbqg_ygj-C74ZqDmYzofS6wUZ5rKqzCFRq0q3l3b6BXYZr2YGzV9_3umkum3o27B3AE8tPcg5O_uK5PQb04Mngok4HJQMFGP6z-6fmlSZvKXRm1C2uvs3_fkY1iqNjMdZ_x6fmlSZvClZH7s0bGjp; ssxmod_itna=iqIxR7eCqmq7q0LxYKBW1QnMmDG2q4AKrdD/I3xnqD=GFDK40oYyxDC4=lQeZUa7R5xd+YB0n=5qiOeoKNI+K8DeDHxY=DU10beDxoq0rD74irDDxD3DbbdDSDWKD9D048yRvLKGWDbxNDmqdDILNDxDLBiTjDxYQDGwPjD7Q4HuqD0qeiK0hXCDiDY4LDwwRyYinoID=DjwiD/bm7ZD=YppFNUTWaOcNTeqGyeKGuIkryAeDHFdNSlq4=QrqYngIrihGoUhhxlBAfI0uCWRD5W04PSYpkniCL608DGbmf4O4xD=; ssxmod_itna2=iqIxR7eCqmq7q0LxYKBW1QnMmDG2q4AKrG93vQWDBurnq7PwExBWFGFCG2LOF2=oKtK0CDWm4zt+g74i4lexMH08xwfxoNqKxfWvHCD0hH6wB++LdS1ZjOD3H7eDSU97GHvIM86CTZFtfPazBD9tTYRFLxqGleP8x9aaxKc+=Kuw=Fp8TY9m07BajEyCTGIv0GEkrc5Ns3EO+xFjsxE=K4FE=9Y8m39aromCXPH8BITH/83RT7BRptnvglOQ7K=aDZOwqj=Q2WPyr4nRs4ZjqtvhfcpSX=FoDQI5LD08DYI54D==".split(
    ";")  # 切换为自己的cookie
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

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start', type=int, help="page num of newest article")
parser.add_argument('end', type=int, help="page num of last article")
args = parser.parse_args()
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
