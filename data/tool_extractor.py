"""
This script goes through a list of user ids (sorted by top rank first)
and extracts the tools that each user has listed on their site.  I'll also save some of the text for possible later use.
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import re

# load sorted list of user ids
with open('users.json', 'r') as f:
    user_list = json.load(f)

print(user_list[0])

root_url = """http://www.kaggle.com"""
summary_url = root_url + """/knockout/profiles/"""
# loop through users and extract data.  Let's focus on the top 1k first
# for i, user in enumerate(user_list[:1000]):
#     r = requests.get(root_url + user)
#     soup = BeautifulSoup(r.text)
#     skills_section = soup.find("ul", {"id":"profile2-linkedin-tags"})
#     print(skills_section)
#     skills = skills_section.find_all("span")
#     print([s.text for s in skills])
#     time.sleep(.1)
#     break

users = []
for i, user in enumerate(user_list[:1000]):
    print(i)
    uid = re.search(r'(?<=/)\d+(?=/)', user).group(0)
    r = requests.get(summary_url + uid + "/summary")
    temp_user = json.loads(r.text)
    time.sleep(.05)
    r = requests.get(summary_url + uid)
    temp_add = json.loads(r.text)
    temp_user.update(temp_add)
    users.append(temp_user)
    time.sleep(0.05)

with open('user_data.json', 'w') as f:
    json.dump(users, f)
