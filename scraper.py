from ast import keyword
from msilib.schema import Error
from os import system
import os
import time
from urllib.request import urlretrieve
from xml.dom.minidom import Document
from bs4 import BeautifulSoup
import bs4
from flask import request
import requests
from pytube import YouTube
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class Scraper:
    def __init__(self, url, keyword):
        self.url = url
        self.keyword = keyword
        self.pageRes = requests.get(url).text

    def getTextWithKeyword(self):
        document = BeautifulSoup(self.pageRes, "html.parser")
        articles = document.find_all("article")
        divs = document.find_all("div")
        paragraphs = document.find_all("p")


        for article in articles:
            if self.keyword in article.text:
                print(article.text)
                with open(f"results {document.title.text}.txt","a") as file:
                    file.write("\n\n\n")
                    file.write(article.text)

        
        for div in divs:
            if self.keyword in div.text:
                print(div.text)
                with open(f"results {document.title.text}.txt","a") as file:
                    file.write("\n\n\n")
                    file.write(article.text)

        
        for par in paragraphs:
            #print(par.decode_contents())
            if self.keyword in par.text:
                print(par.text)
                with open(f"results {document.title.text}.txt","a") as file:
                    file.write("\n\n\n")
                    file.write(article.text)

    def getLinkedPagesWithKeyword(self, depthOfSearch, currentDepth=0, linksDict = {}, url = ""):
        try:
            if(currentDepth==0):
                document = BeautifulSoup(self.pageRes, "html.parser")
            else:
                page = requests.get(url).text
                document = BeautifulSoup(page, "html.parser")
            links = document.find_all("a", href=True)
            title = document.title
            print(title)
            if title not in linksDict:
                for link in links:
                    if self.keyword in link["href"]:
                        linksDict[title.text] = link["href"]
                        if currentDepth < depthOfSearch:
                            self.getLinkedPagesWithKeyword(depthOfSearch, currentDepth+1, linksDict, link["href"])

            currentDepth = currentDepth + 1


            return linksDict    
        except Exception:
            print("Cannot get from url: "+ url)
            return linksDict

    def getImagesFromPage(self):
        document = BeautifulSoup(self.pageRes, "html.parser")
        imgs = document.find_all("img")
        counter = 0
        for img in imgs:
            src = img["src"]
            print(src)
            if "http" in src:
                urlretrieve(src, f"{counter}.png")
                counter = counter + 1

    def getYTVideosFromSearch(self):
        url = "https://www.youtube.com/results?search_query="+self.keyword
        options = Options()
        browser = webdriver.Chrome(executable_path=r'C:\cmder\bin\chromedriver.exe', options=options)
       
        #print(document)
        print(url)
        browser.get(url)
        time.sleep(2)
        document = BeautifulSoup(browser.page_source, "html.parser")
        videoSrcList = list()

        videoLinks = document.find_all("a",attrs={'class':'pl-video-title-link'})
        print(videoLinks)
      #  for video in videoLinks:
        #     link = video['href']
        #     print("Downloading: " + "https://www.youtube.com" + link)
        #     videoSrcList.append("https://www.youtube.com"+link)
        
        # for src in videoSrcList:
        #     YouTube(src).streams.get_by_resolution("360p").download()

