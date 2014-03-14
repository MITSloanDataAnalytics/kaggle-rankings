"""
blog_miner.py
Reads a list of blogs and mines it for mentions of popular tools
Script 2 of 3 in the pipeline for getting languages used by Kaggle winners.
"""
import time
import json
from bs4 import BeautifulSoup
import requests
import re

# load up a list of blog posts
with open('links.json', 'r') as f:
    links = json.load(f)

# loop through links and mine the text
new_links = []
for i, link in enumerate(links):
    print(i, link['url'])

    # Get the date information
    date_search = re.search(r'\d{4}/\d{2}/\d{2}', link['url'])
    if date_search:
        link['date'] = date_search.group(0).replace('/', '-')
    else:
        link['date'] = None

    # Get the text of the blog post
    r = requests.get(link['url'])
    soup = BeautifulSoup(r.text)
    post = soup.find('div', class_='entry-content')
    link['text'] = post.text
    new_links.append(link)
    time.sleep(.1)


with open('links2.json', 'w') as f:
    json.dump(new_links, f)
