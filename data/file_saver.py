"""
file_saver.py
This script downloads pages from http://blog.kaggle.com/category/dojo/ and saves the html.
Script 1 of 3 in the pipeline for getting languages used by Kaggle winners.
"""
import requests
from bs4 import BeautifulSoup
import json
import time

root_url = "http://blog.kaggle.com/category/dojo/page"
pages = range(1, 10)  # Currently there are 9 pages

elems = []
for page in pages:
    r = requests.get(root_url + "/" + str(page) + "/")
    soup = BeautifulSoup(r.text)
    elems += soup.find_all("h2", class_="entry-title")

# Convert list of dicts
link_dict = []
for i, elem in enumerate(elems):
    link = elem.find("a")
    temp_dict = {
                 'id': i,
                 'url': link.get('href'), 
                 'title': link.get('title'),
                 'link_text': link.get_text()
                }
    link_dict.append(temp_dict)

# Save to json object!
with open('links.json', 'w') as f:
    json.dump(link_dict, f)
