import pysolr
import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import lxml.html
#
# link = "https://urdu.dunyanews.tv/index.php/ur/Pakistan/722576"
# response = requests.get(link)
# tree = lxml.html.fromstring(response.text)
# date_elem = tree.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div/div[1]')
# # date_elem = tree.xpath('//div[@class="detail-time"]')
# date = date_elem[0].text_content()
# print(date)
# solr = pysolr.Solr("http://localhost:8983/solr/news_data/", always_commit=True)
# solr.delete(q="domain_name:urdu.dunyanews.tv")
