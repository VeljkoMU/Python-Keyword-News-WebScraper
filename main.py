import sys

from scraper import Scraper


url = sys.argv[1]
keyword = sys.argv[2]

scraper = Scraper(url, keyword)

results = scraper.getLinkedPagesWithKeyword(1)

print(results)