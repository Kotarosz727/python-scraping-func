import logging
import requests
from bs4 import BeautifulSoup
import json
import codecs
import azure.functions as func
import re


def getNikkeiBusiness(urlName):
    content = requests.get(urlName).text
    soup = BeautifulSoup(content, "html.parser")
    elems = soup.find_all("span")
    res = []

    for elem in elems:
        try:
            string = elem.get("class").pop(0)
            if string in "category":
                title = elem.find_next_sibling("h3")
                title = (title.text.replace('\n', ''))
                r = elem.find_previous('a')
                url = urlName + r.get('href')
                data = {'title': '', 'url': ''}
                data['title'] = title
                data['url'] = url
                res.append(data)
        except:
            pass

    return res


def getNikkei(urlName):
    content = requests.get(urlName).text
    soup = BeautifulSoup(content, "html.parser")
    elems = soup.find_all("a", class_="k-card__block-link")
    res = []

    for elem in elems:
        title = (elem.span.text)
        url = (elem.get('href'))
        data = {'title': '', 'url': ''}
        # urlにhttpsが含まれているか否か
        checkUrlHasHttps = re.search('https', url)
        if not checkUrlHasHttps:
            url = urlName + url
        data['title'] = title
        data['url'] = url
        res.append(data)
    return res


def getSankei(urlName):
    content = requests.get(urlName).text
    soup = BeautifulSoup(content, "html.parser")
    elems = soup.find_all("span", class_="title")

    res = []

    for elem in elems:
        title = elem.text
        url = elem.find_parent("a")
        url = url.get('href')
        data = {'title': '', 'url': ''}
        # urlにhttpsが含まれているか否か
        checkUrlHasHttps = re.search('https', url)
        if not checkUrlHasHttps:
            url = urlName + url
        data['title'] = title
        data['url'] = url
        res.append(data)
    return res


def getJapanTimes(urlName):
    content = requests.get(urlName).text
    soup = BeautifulSoup(content, "html.parser")
    elems = soup.find_all("p", class_="article-title")

    res = []

    for elem in elems:
        title = elem.text.strip()
        print(title)
        url = elem.find_parent("a")
        url = url.get('href')
        data = {'title': '', 'url': ''}
        # urlにhttpsが含まれているか否か
        # checkUrlHasHttps = re.search('https', url)
        # if not checkUrlHasHttps:
        #     url = urlName + url
        data['title'] = title
        data['url'] = url
        res.append(data)
    return res


def getAsahi(urlName):
    r = requests.get(urlName)
    r.raise_for_status()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    elems = soup.find_all("a", class_="c-articleModule__link")

    res = []

    for elem in elems:
        title = elem.span.text.strip()
        print(elem)
        url = elem.get('href')
        data = {'title': '', 'url': ''}
        # urlにhttpsが含まれているか否か
        # checkUrlHasHttps = re.search('https', url)
        # if not checkUrlHasHttps:
        #     url = urlName + url
        data['title'] = title
        data['url'] = url
        res.append(data)
    return res


def getBBC(urlName):
    content = requests.get(urlName).text
    soup = BeautifulSoup(content, "html.parser")
    elems = soup.find_all("h3", class_="gs-c-promo-heading__title")

    res = []
    title_array = []

    for elem in elems:
        title = elem.text.strip()
        # 重複があるのでその場合スキップ
        if (title in title_array):
            continue
        title_array.append(title)
        url = elem.find_parent("a")
        url = url.get('href')
        # urlにhttpsが含まれているか否か
        checkUrlHasHttps = re.search('https', url)
        if not checkUrlHasHttps:
            url = urlName + url
        data = {'title': '', 'url': ''}
        data['title'] = title
        data['url'] = url
        res.append(data)
    return res


def getWSJ(urlName):
    content = requests.get(urlName).text
    soup = BeautifulSoup(content, "html.parser")
    elems = soup.find_all("div", class_="WSJTheme--headline--7VCzo7Ay")

    res = []

    for elem in elems:
        title = elem.find_next("a").text
        url = elem.find_next("a").get('href')
        data = {'title': '', 'url': ''}
        # urlにhttpsが含まれているか否か
        # checkUrlHasHttps = re.search('https', url)
        # if not checkUrlHasHttps:
        #     url = urlName + url
        data['title'] = title
        data['url'] = url
        res.append(data)
    return res


def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    name = req.params.get('name')

    if name == 'nikkei_business':
        urlName = "https://business.nikkei.com"
        res = getNikkeiBusiness(urlName)
    elif name == 'nikkei':
        urlName = 'https://www.nikkei.com'
        res = getNikkei(urlName)
    elif name == 'sankei':
        urlName = 'https://www.sankei.com'
        res = getSankei(urlName)
    elif name == 'japanTimes':
        urlName = 'https://www.japantimes.co.jp'
        res = getJapanTimes(urlName)
    elif name == 'asahi':
        urlName = 'https://www.asahi.com'
        res = getAsahi(urlName)
    elif name == 'bbc':
        urlName = 'https://www.bbc.com/news/world'
        res = getBBC(urlName)
    elif name == 'wsj':
        urlName = 'https://www.wsj.com'
        res = getWSJ(urlName)
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )

    return func.HttpResponse(json.dumps(res, ensure_ascii=False), headers=headers)
