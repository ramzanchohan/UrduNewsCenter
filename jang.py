import requests
import json
import lxml.html
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from boilerpy3 import extractors
import pysolr
import datetime
import pytz
import re


def main():
    extractor = extractors.ArticleExtractor()
    solr_client = pysolr.Solr("http://localhost:8983/solr/news_data/", always_commit=True)
    url = "https://jang.com.pk/"
    response = requests.get(url).text
    # print(response)
    tree = lxml.html.fromstring(response)
    # print(tree.text)
    meta_tag = tree.xpath('//meta/@content')
    # print(meta_tag)
    soup = BeautifulSoup(response, 'html.parser')
    main_title = soup.find('title').text
    # print(main_title)
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    # print(domain_name)
    links = soup.find_all('a')
    # print(links)
    sec = "https://jang.com.pk/category"
    inbound_links = []
    for link in links:
        href = link.get('href')
        # print(href)
        if href is not None and href.startswith(sec):
            inbound_links.append(href)
    # print(inbound_links)
    unique_inbound_links = list(set(inbound_links))
    # print(unique_inbound_links)
    sec = "https://jang.com.pk/news/"
    inner_inbound_links = []
    for related_links in unique_inbound_links:
        inner_response = requests.get(related_links)
        soup = BeautifulSoup(inner_response.text, 'html.parser')
        links = soup.findAll('a')
        for link in links:
            href = link.get('href')
            # print(href)
            if href is not None and href.startswith(sec):
                inner_inbound_links.append(href)
    unique_inner_inbound_links = list(set(inner_inbound_links))
    # print(unique_inner_inbound_links)
    for dlink in unique_inner_inbound_links:
        with open("scrapedLinks.txt", "r") as check:
            if dlink in check.read():
                print(" ")
            else:
                d_response = requests.get(dlink)
                tree = lxml.html.fromstring(d_response.text)
                date_elem = tree.xpath('//div[@class="detail-time"]')
                date = date_elem[2].text_content()
                extracted_text = extractor.get_doc(d_response.text)
                allNews_title = str(extracted_text.title)
                allNews_content = str(extracted_text.content)
                print(allNews_title)
                print(date)
                print(allNews_content)
                x = {
                    "id": str(dlink),
                    "web_tile": str(main_title),
                    "meta_tags": str(meta_tag),
                    "news_title": allNews_title,
                    "news_details": allNews_content,
                    "news_date": date,
                    "domain_name": domain_name,
                    "pdate": ''
                }
                data = json.dumps(x)
                # print(data)
                solr_client.add(x)
                solr_client.commit()
                with open("scrapedLinks.txt", "a") as Slinks:
                    Slinks.write(dlink)
                    Slinks.close()


