import json
import sys
from news_sraper import NewsScraper

from scraper import Scraper

scraper = NewsScraper()

scraper.load_links()

keyword = input()

res = scraper.run(keyword)
print(res)

#results = scraper.getLinkedPagesWithKeyword(1)
#scraper.getTextWithKeyword()
#scraper.getImagesFromPage()
#scraper.getYTVideosFromSearch()

#print(json.dumps(results, indent=4))