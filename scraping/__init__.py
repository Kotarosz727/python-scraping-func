import logging
import requests
from bs4 import BeautifulSoup
import json
import codecs

import azure.functions as func


def getNikkeiBusiness(urlName):
    url = requests.get(urlName)
    soup = BeautifulSoup(url.content, "html.parser")
    elems = soup.find_all("span")

    res = []
    data = {'title': '', 'url': ''}

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


def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }
    name = req.params.get('name')

    if name == 'nikkei_business':
        urlName = "https://business.nikkei.com"
        res = getNikkeiBusiness(urlName)

    return func.HttpResponse(json.dumps(res, ensure_ascii=False), headers=headers)
