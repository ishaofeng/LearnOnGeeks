#! /usr/bin/python
#encoding=utf-8

from __future__ import unicode_literals

from pyquery import PyQuery as pq
import json

baseurl = "http://www.geeksforgeeks.org/"
urls = [
"data-structures",
"fundamentals-of-algorithms",
"c",
"c-plus-plus",
"java",
]

def parserCatagery(url):
    '''
        解析一个题目页面，解析生成的题目结构
    '''
    result = {}

    doc = pq(url=url)

    #分类名称
    title = doc("h2.page-title").html()
    result["title"] = title
    result["sections"] = {}

    #分类解析处理
    for p in doc("div.page-content > p").items():
        sectionname = p("strong").html()
        section = {}

        em = {}
        emname = ""
        for item in p.children().items():
            if item.is_("em"):
                if em:
                    section[emname] = em

                emname = item.text()
                em = {}
            elif item.is_("a"):
                em[item.html()] = item.attr.href

        if section:
            if em:
                section[emname] = em
        else:
            section = em

        result["sections"][sectionname] = section

    return result


if __name__ == "__main__":
    result = [] 
    for url in urls:
        catagery = parserCatagery(baseurl + url)
        result.append(catagery)

    with open("data.json", "w") as f:
        json.dump(result, f, indent=4)

