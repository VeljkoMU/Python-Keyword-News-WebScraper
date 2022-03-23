
from bs4 import BeautifulSoup as bs4
import os
import requests
from urllib.request import urlretrieve


class NewsScraper:
    def __init__(self, conf = "config.txt"):
        self.config_path = conf
        self.links = set()
        self.load_links()

    def load_links(self):
        file = open(self.config_path, "r")
        for link in file:
            link = link.replace("\n","")
            self.links.add(link)
        file.close()

    def add_link(self, link):
        file = open(self.config_path, "a")
        file.write("\n"+link)
        self.links.add(link)
        file.close()

    def read_page(self, link, keyword, getImages=False):
        page_res = requests.get(link).text
        document = bs4(page_res, "html.parser")
        articles = document.find_all("p")
        containsKeyword = False
        results_text = list()
        results_links = document.find_all("a")

        results_links = list(map(lambda x: x["href"] if "href" in x.attrs else "", results_links))
        results_links = list(filter(lambda x: x!="", results_links))

        title = document.title
        
        for a in articles:
            if keyword in a.text:
                containsKeyword = True
                results_text.append(a.text)

                if(getImages):
                    self.getImages(a)

        return (results_text, results_links, title, containsKeyword)

    def getImages(self, div):
        imgs = div.find_all("img")
        for img in imgs:
            src = img["src"]
            if "http" in src:
                urlretrieve(src, f"image: {src}")

    def format_links(self, link, link_base):
        if link_base not in link:
            link = link_base + link[1:]
        if "https" not in link:
            link = "https:" + link
        
        return link

    def run(self, keyword, depthOfSearch=1, includeImages = False):
        resultsListOfLinks = dict()
        pages = list()
        
        for source in self.links:
            _, links, _, _ = self.read_page(source, keyword)
            for i in range(0, len(links)):
                links[i] = self.format_links(links[i], source)
                
            pages.extend(links)

        try:
            alreadyDone = list()
            for page in pages:
                if page in alreadyDone:
                    continue

                results, links, title, found = self.read_page(page, keyword, includeImages)
                print(page)
                if not found:   
                    continue
                
                fname = self.format_filename(title.text)
                with open(f"{fname}.txt", "w", encoding="utf-8") as file:
                    for r in results:
                        file.write(r + "\n\n\n")

                if title not in resultsListOfLinks:
                    resultsListOfLinks[title]= page
                alreadyDone.append(page)

                # depthCounter = 0
                # #alreadyDone.extend(pages)
                # while depthCounter<depthOfSearch:
                #     linksTemp = list()
                #     for link in links:
                #         if link not in alreadyDone:
                #             results, sublinks, title, found = self.read_page(link, keyword, includeImages)
                #             if not found:
                #                 continue

                #             print(link)

                #             with open(f"{title}", "w") as file:
                #                 for r in results:
                #                     file.write(r + "\n\n\n")
                            
                #             resultsListOfLinks[title] = link
                #             alreadyDone.append(link)
                #             linksTemp.extend(sublinks)
                #     links= linksTemp
                #     depthCounter+=1
        except Exception as e:
            print("Error:")
            print(e)
            
        return resultsListOfLinks
    
    def format_filename(self, name):
        invalid = '<>:\"/\|?* '

        for char in invalid:
            name = name.replace(char, "")

        print(name)

        return name
            