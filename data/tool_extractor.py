"""
tool_extractor.py
Goes through a list of user ids (sorted by top rank first)
and extracts the tools that each user has listed on their site.
I'll also save some of the text for possible later use.
Script 2 of 2 for finding top languages/tools used by kaggle competitors
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import re

# load sorted list of user ids
with open('users.json', 'r') as f:
    user_list = json.load(f)

# check
print(user_list[0])

root_url = """http://www.kaggle.com"""
summary_url = root_url + """/knockout/profiles/"""

users = []
for i, user in enumerate(user_list[:1000]):  # only get top 1000 users
    print(i)  # this is going to take a while and I want to know the progress
    
    uid = re.search(r'(?<=/)\d+(?=/)', user).group(0)
    r = requests.get(summary_url + uid + "/summary")
    temp_user = json.loads(r.text)
    time.sleep(.05)
    
    # other data is available from the regular url
    r = requests.get(summary_url + uid)
    temp_add = json.loads(r.text)
    temp_user.update(temp_add)
    users.append(temp_user)
    time.sleep(0.05)

with open('user_data.json', 'w') as f:
    json.dump(users, f)
