#!/usr/bin/python

import sys
import bs4
import requests

def get_tab(search_string=None):
    if search_string is None:
        search_string = sys.argv[1]
    url = query_google(search_string.split(" "))
    tab = pull_tab(url)
    print(tab)

def query_google(search_keywords):
    baseQuery = "https://google.com/search?q={}+site:tabs.ultimate-guitar.com"
    queryString = baseQuery.format("+".join(search_keywords))
    print( "Querying Google...")
    result = bs4.BeautifulSoup(requests.get(queryString).text,"html.parser")
    print( "Searching for link...")
    link = result.find("h3",class_="r").find("a").get("href")
    url = link[7:link.find("&")]
    return url

def pull_tab(url):
    print( "Visiting Ultimate Guitar...")
    data = requests.get(url).text
    # print( data)
    result = bs4.BeautifulSoup(data,"html.parser")
    # print(result)
    print( "Extracting tab...")
    tab = result.select_one("pre[class*=js-tab-content]")
    print(tab.text)
    return tab.text


if __name__ == "__main__":
    get_tab()
