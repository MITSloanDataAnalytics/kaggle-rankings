"""
Script to profiles of all the kaggle competitors!
"""
import requests
import time
from bs4 import BeautifulSoup
import json

root_url = """http://www.kaggle.com/users?page="""
pages = range(1, 3656+1)

users = []
for page in pages:
    print(page)
    r = requests.get(root_url + str(page))
    soup = BeautifulSoup(r.text)
    users_content = soup.find("ul", class_="users-list")
    user_list = users_content.find_all("a", class_="profilelink")
    users += [u.get('href') for u in user_list]
    time.sleep(0.1)

# save!
with open('user_list.json', 'w') as f:
    json.dump(users, f)
