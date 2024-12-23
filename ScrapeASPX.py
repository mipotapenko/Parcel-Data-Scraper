# Try to scrape aspx without rendering the web page.

from bs4 import BeautifulSoup
import requests
import pickle
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    url = "https://cityofcorning.sdgnys.com/search.aspx"
    # url = "https://cityofcorning.sdgnys.com/propdetail.aspx?swis=460300&printkey=2990110002001000%20%20%20%20"
    index_page = requests.get(url)
    soup = BeautifulSoup(index_page.content, "html.parser")
    view_state = soup.findAll("input", {"type": "hidden", "name": "__VIEWSTATE"})
    event_validation = soup.findAll("input", {"type": "hidden", "name": "__EVENTVALIDATION"})

    print(view_state[0]['value'])
    # print(soup)

