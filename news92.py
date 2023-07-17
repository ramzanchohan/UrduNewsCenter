import requests
import lxml.html
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from boilerpy3 import extractors
import pysolr


def main():
    url = "https://urdu.92newshd.tv"
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
    print(domain_name)

    soup = BeautifulSoup(response, 'html.parser')

    links = soup.find_all('a')
    # print(links)
    sec = "/category/"
    inbound_links = []
    for link in links:
        href = link.get('href')
        if href is not None and href.startswith(sec):
            inbound_links.append(url + href)
    # print(inbound_links)
    unique_inbound_links = list(set(inbound_links))

    url2 = "https://urdu.92newshd.tv"
    inner_links = []
    dir = "/about/"
    for link in unique_inbound_links:
        core_response = requests.get(link)
        soup = BeautifulSoup(core_response.content, 'html.parser')
        links = soup.findAll('a')
        # print(links)

        for core_link in links:
            href = core_link.get('href')
            if href is not None and href.startswith(dir):
                inner_links.append(url2 + href)
    # print(inner_links)

    unique_core_links = list(set(inner_links))
    # print(unique_core_links)
    extractor = extractors.ArticleExtractor()
    for link in unique_core_links:
        with open("scrapedLinks.txt", "r") as check:
            if link in check.read():
                print(" ")
            else:
                innner_response = requests.get(link, verify=False)
                tree = lxml.html.fromstring(innner_response.text)
                date = tree.xpath('//*[@id="main-container"]/div[1]/div/div/article/div/div[2]/a')
                date_time = date[0].text_content()
                extracted_text = extractor.get_doc(innner_response.text)
                allNews_title = str(extracted_text.title)
                allNews_content = str(extracted_text.content)
                print(allNews_title)
                print(allNews_content)
                print(date_time)
                solr_client = pysolr.Solr("http://localhost:8983/solr/news_data/", always_commit=True)
                x = {
                    "id": str(link),
                    "web_tile": str(main_title),
                    "meta_tags": str(meta_tag),
                    "news_title": allNews_title,
                    "news_details": allNews_content,
                    "news_date": date_time,
                    "domain_name": domain_name,
                    "pdate": ''
                }
                data = json.dumps(x)
                print(data)
                solr_client.add(x)
                solr_client.commit()
                with open("scrapedLinks.txt", "a") as Slinks:
                    Slinks.write(link)
                    Slinks.close()
