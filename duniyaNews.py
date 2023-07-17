import requests
import json
import lxml.html
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from boilerpy3 import extractors
import pysolr


def main():
    solr_client = pysolr.Solr("http://localhost:8983/solr/news_data/", always_commit=False)
    url = "https://urdu.dunyanews.tv"
    response = requests.get(url).text
    # print(response)
    tree = lxml.html.fromstring(response)
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
    ul = "/index.php/ur/"
    inbound_links = []
    for link in links:
        href = link.get('href')
        if href is not None and href.startswith(ul):
            inbound_links.append(url + href)
            # print(inbound_links)
    # print(inbound_links)
    unique_inbound_links = list(set(inbound_links))
    # print(unique_inbound_links)
    sec = "/index.php/ur/"
    inner_inbound_links = []
    for link in unique_inbound_links:
        inner_response = requests.get(link).text
        soup = BeautifulSoup(inner_response, 'html.parser')
        links_all = soup.find_all('a')
        for link1 in links_all:
            href1 = link1.get('href')
            if href1 is not None and href1.startswith(sec):
                # print(href)
                inner_inbound_links.append(url + href1)
    # # # print(inner_inbound_links)
    unique_inner_inbound_links = list(set(inner_inbound_links))
    print(unique_inner_inbound_links)
    for link in unique_inner_inbound_links:
        with open("scrapedLinks.txt", "r") as check:
            if link in check.read():
                print(" ")
            else:
                inner_response = requests.get(link, verify=False)
                extractor = extractors.ArticleExtractor()
                extracted_text = extractor.get_doc(inner_response.text)
                allNews_title = str(extracted_text.title)
                allNews_content = str(extracted_text.content)
                print(allNews_title)
                print(allNews_content)
                print(link)
                x = {
                    "id": str(link),
                    "web_title": str(main_title),
                    "meta_tags": str(meta_tag),
                    "news_title": allNews_title,
                    "news_details": allNews_content,
                    "news_date": '',
                    "domain_name": domain_name,
                    "pdate": ''
                }
                data = json.dumps(x)
                print(data)
                solr_client.add(x)
                solr_client.commit()
                with open("ExtractedNewsDN.txt", "a", encoding="utf-8") as allNewsFile:
                    allNewsFile.write(allNews_title)
                    allNewsFile.write(allNews_content)
                    allNewsFile.close()
                with open("scrapedLinks.txt", "a") as Slinks:
                    Slinks.write(link)
                    Slinks.close()
