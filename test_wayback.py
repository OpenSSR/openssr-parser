import requests
import wayback3
from ssrn_urls import *

chander_author_id = 275458
chander_paper_id = 562301

chander_url = wayback3.availability(SSRN_AUTHOR_URL % chander_author_id).get('url')
paper_url = wayback3.availability(SSRN_ABSTRACT_URL_LONG % chander_paper_id).get('url')

chander_response = requests.get(chander_url)
paper_response = requests.get(paper_url)

f1 = open("sample-data/wb-author-%d.html" % chander_author_id, "wb")
f1.write(chander_response.content)
f1.close()
f2 = open("sample-data/wb-abstract-%d.html" % chander_paper_id, "wb")
f2.write(paper_response.content)
f2.close()
