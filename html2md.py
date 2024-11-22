import re

def parse(html_content):
    reg_title = re.compile(r"<title>(.*?)</title>")
    title = reg_title.findall(html_content)[0]
    reg_content = re.compile(r'<div id="topic_content" class="topic-content markdown-body">(.*?)<\/div>',flags=re.S+re.M)
    content = reg_content.findall(html_content)[0]
    print(content)


html = open("example.html","r",encoding="utf-8").read()
parse(html)