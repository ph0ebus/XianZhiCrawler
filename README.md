# XianZhiCrawler

![Language](https://img.shields.io/badge/language-python-blue.svg)

> [!IMPORTANT]
> 本项目的目的仅是给需要离线打比赛的CTFer提供一个离线文档检索、使用的方便途径，仅供学习交流使用，请勿用于非法用途

如果对您有用的话，求个star呜呜，孩子没见过star

# Introduction

先知社区半自动爬虫，需要偶尔手动过滑块验证获取Cookie（太菜了不会写自动过滑块

# Usage

```
$ python .\xianzhicrawler.py -h
usage: xianzhicrawler.py [-h] start end

positional arguments:
  start       page num of newest article
  end         page num of last article

options:
  -h, --help  show this help message and exit
```

默认是从索引值大的文章到索引值小的文章依次遍历的（从新到旧），例如下列命令就是下载 https://xz.aliyun.com/t/16318 到 https://xz.aliyun.com/t/16000 的所有有效文章。如有需要可以自行修改代码。

```
$ python .\xianzhicrawler.py 16318 16000
```

# update log

20241126

优化了cookies放置的位置，更方便的替换新的有效cookie；优化了argparse的逻辑，避免使用`-h`时会执行一段无用的代码

20241122

输出方式更新为markdown，避免输出pdf导致的代码折叠问题，解析为markdown部分借鉴了 https://github.com/Zh0um1/xzSpider 这个项目，并根据遇到的bug做了一定优化处理

# Demo

[![demo](https://i.ytimg.com/vi/prxfSq_cxVg/maxresdefault.jpg)](https://youtu.be/prxfSq_cxVg?si=1HfRxytnUvMXrDVI "demo")