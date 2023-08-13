import requests
from bs4 import BeautifulSoup
import html2text as ht
import os
import urllib3
from config.setting import configDICT
from translate import get_token, url_option, get_translate
import re

urllib3.disable_warnings()
text_maker = ht.HTML2Text()

headers ={
    "Cookie": configDICT["Cookie"],
    "Content-Type": "text/html; charset=utf-8",
    "User-Agent": configDICT["User-Agent"]
}
es_url = "https://www.elastic.co/guide/en/elasticsearch/reference/8.9/"

def url2md(url_name):
    # index.html
    url = es_url + url_name
    htmlpage = requests.get(url, headers=headers).text
    mdtext = text_maker.handle(htmlpage)
    return mdtext

def delete_valid_info(contents):
    results = []
    print(contents)
    contents = contents.split("\n")
    for line in contents:
        if line.startswith("Most Popular") and len(line) < 20:
            break
        results.append(line)

    content = "\n".join(results)
    return content


def re_delete_http(input_string):
    pattern = r'\[(.*?)\]\(.*?\)'
    output_string = re.sub(pattern, r'\1', input_string)
    return output_string


def translate2zh_md(contents):
    trans_contents = []
    related_dict = {}
    sen_contents = contents.split("\n\n")
    transi = 0
    for ind, content in enumerate(sen_contents):
        if content.startswith("[Elastic Docs") or content.startswith("[« ") or content.startswith("[Data in:"):
            sen_contents[int(ind)] = sen_contents[int(ind)].replace(".html", ".md")
            continue
        if content.startswith("    "):  # 代码块不翻译
            continue
        if len(content.split(" ")) < 2:
            continue
        else:
            related_dict[str(ind)] = transi

            if content.startswith("#") and "[edit]" in content:
                content = content.replace("[edit]", "[]")
                pass
            en_content = re_delete_http(content.replace("\n", ""))
            trans_contents.append({"Text": en_content})
            transi += 1

    token = get_token()
    url_option()
    trans_text = get_translate(token, body=trans_contents).json()
    for ind in related_dict.keys():
        sen_contents[int(ind)] = trans_text[int(related_dict[str(ind)])]["translations"][0]["text"].replace("“", "\"").replace("”", "\"").replace("在 GitHub 上编辑此页面", "Edit this page on GitHub").replace("（", "(").replace("）", ")")

    zh_contents = "\n\n".join(sen_contents)
    return zh_contents


if __name__ == "__main__":
    path = os.path.abspath(r"./zh_mds")
    if not os.path.exists(path):
        os.mkdir(path)

    index_url = es_url + "index.html"  # elasticsearch 的网址
    text = requests.get(index_url, headers=headers, verify=False).text
    soup = BeautifulSoup(text, "html.parser")
    toc_class = soup.find("div", {"class": "toc"})
    spans = toc_class.find_all("span")
    for ind, span in enumerate(spans):
        # 获取子目录的链接
        try:
            url_name = span.find("a").attrs.get("href")
        except:
            continue
        name = span.find("a").text
        md_name = str(url_name).replace(".html", ".md")
        with open(os.path.join(path, "index.md"), "a+", encoding="utf-8") as fh:
            line = f"[{name}](./{md_name})"
            fh.write(line + "\n\n")

        print(f"ind:{ind},url_name:{url_name}")
        try:
            # 从url中获取教程后转为html
            md_text = url2md(url_name)
            print(f"=====md_text:{md_text}")
            md_text = delete_valid_info(md_text)
            zh_text = translate2zh_md(md_text)
        except:
            print(f"error span:{span}")


        with open(os.path.join(path, md_name), "w", encoding="utf-8") as fh:
            fh.write(zh_text)