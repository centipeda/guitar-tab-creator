#!/usr/bin/python

import sys
import bs4
import requests

def main():
    search_string = sys.argv[1]
    url = query_google(search_string.split(" "))
    tab = pull_tab(url)
    print tab

def query_google(search_keywords):
    baseQuery = "https://google.com/search?q={}+site:tabs.ultimate-guitar.com"
    queryString = baseQuery.format("+".join(search_keywords))
    result = bs4.BeautifulSoup(requests.get(queryString).text,"html.parser")
    link = result.find("h3",class_="r").find("a").get("href")
    url = link[7:link.find("&")]
    return url

def pull_tab(url):
    result = bs4.BeautifulSoup(requests.get(url).text,"html.parser")
    tab = result.find("pre",class_="js-tab-content")
    return tab.string


if __name__ == "__main__":
    main()
