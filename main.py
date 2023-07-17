import requests
import json
import lxml.html
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from boilerpy3 import extractors
import pysolr
import datetime
import pytz


def main():
    url = "https://www.urdunews.com"
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
    soup = BeautifulSoup(response, 'html.parser')
    #
    # # Find the date element and extract its text content
    # date_elem = soup.find('div', {'class': 'article-item-date'})
    # date = date_elem.text.strip()
    #
    # print(date)
    # finding inner links (sections)
    links = soup.find_all('a')
    # print(links)
    sec = "/sections/"
    inbound_links = []
    for link in links:
        href = link.get('href')
        if href is not None and href.startswith(sec):
            inbound_links.append(url + href)
    # print(inbound_links)
    unique_inbound_links = list(set(inbound_links))

    # soup = BeautifulSoup(inner_response.text, 'html.parser')
    # # # print(inner_links)
    sec = "/node/"
    inner_inbound_links = []
    for link in unique_inbound_links:
        response = requests.get(link, verify=False).text
        soup = BeautifulSoup(response, 'html.parser')
        links = soup.findAll('a')
        for inner_link in links:
            href = inner_link.get('href')
            if href is not None and href.startswith(sec):
                inner_inbound_links.append(url + href)

    unique_inner_inbound = list(set(inner_inbound_links))

    # print(unique_inner_inbound)
    solr_client = pysolr.Solr("http://localhost:8983/solr/news_data/", always_commit=True)
    extractor = extractors.ArticleExtractor()
    for link in unique_inner_inbound:

        # with open("scrapedLinks.txt", "r") as check:
        #     if link in check.read():
        #         print(" ")
            # else:
        inner_response = requests.get(link)
        tree = lxml.html.fromstring(inner_response.text)
        date = tree.xpath('//meta[@property="og:updated_time"]/@content')[0]
        date_obj = datetime.datetime.fromisoformat(date)
        utc_date = date_obj.astimezone(pytz.utc)
        utc_date_str = utc_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        print(utc_date_str)
        extractor = extractors.ArticleExtractor()
        extracted_text = extractor.get_doc(inner_response.text)
        allNews_title = str(extracted_text.title)
        allNews_content = str(extracted_text.content)
        print(allNews_title)
        print(allNews_content)
        print("normal date" + date)
        print("utc date" + utc_date_str)
        x = {
                    "id": str(link),
                    "web_tile": str(main_title),
                    "meta_tags": str(meta_tag),
                    "news_title": allNews_title,
                    "news_details": allNews_content,
                    "news_date": date,
                    "domain_name": domain_name,
                    "pdate": utc_date_str
                }
        data = json.dumps(x)
        print(data)
        solr_client.add(x)
        solr_client.commit()
        with open("ExtractedNews.txt", "a", encoding="utf-8") as allNewsFile:
                allNewsFile.write(allNews_title)
                allNewsFile.write(allNews_content)
                allNewsFile.close()
        with open("scrapedLinks.txt", "a") as Slinks:
                Slinks.write(link)
                Slinks.close()        
main()