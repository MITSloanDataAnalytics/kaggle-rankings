"""
keyword_counter.py
Counts the number of times tools appear in kaggle winner interviews.
Script 3 of 3 in the pipeline for getting languages used by Kaggle winners.
"""
import re
import json

tools = ['R', 'Matlab', 'SAS', 'Weka', 'SPSS',
         'Excel', 'C[+][+]', 'Mathematica', 'Stata', 'Java']
python_like = ['Python', '(?:sklearn)|(?:sci[-]kit)|(?:scikit)',
               'pandas', 'scipy', 'numpy']
other_tools = ['SAS', 'C',
               '(?:python)|(?:sklearn)|(?:scikit)|(?:sci[-]kit)|(?:pandas)']
all_tools = tools + python_like + other_tools

# Make a list of all the tutorials ids, which we shouldn't count!
tutorial_ids = [35, 32, 29, 21, 20, 19, 11, 10, ]
print(len(tutorial_ids))

# open the data
with open('links2.json', 'r') as f:
    links = json.load(f)

new_links = []
# loop through all entries and extract keywords
for post in links:
    post['occurences'] = {k: len(re.findall(r'\s' + k + r'\W', post['text'],
                                 flags=re.I)) for k in all_tools}
    # let's add a total column for convenience
    total_refs = sum([v for k, v in post['occurences'].items()
                     if k not in python_like])
    total_ref_classes = len([v for k, v in post['occurences'].items()
                            if v != 0 and k not in python_like])
    post['total_refs'] = total_refs
    post['total_ref_classes'] = total_ref_classes
    if post['id'] in tutorial_ids:
        post['winner'] = False
    else:
        post['winner'] = True
    new_links.append(post)

# save
with open('links3.json', 'w') as f:
    json.dump(new_links, f)

# now loop through all posts, occurences, and make a massive dict
count_dict = {'total': {}, 'once': {},
              'proportion': {}, 'class_proportion': {}}
for post in new_links:
    if post['id'] in tutorial_ids:
        continue  # we only care about #WINNERS!
    else:
        for k, v in post['occurences'].items():
            count_dict['total'][k] = count_dict['total'].get(k, 0) + v
            if post['total_refs'] > 0:
                count_dict['proportion'][k] = count_dict['total'].get(k, 0) / post['total_refs']
            if v > 0:
                count_dict['once'][k] = count_dict['once'].get(k, 0) + 1
                if post['total_ref_classes'] > 0:
                    count_dict['class_proportion'][k] = count_dict['once'].get(k, 0) / post['total_ref_classes']
            else:
                count_dict['once'][k] = count_dict['once'].get(k, 0)

# save
with open('counts.json', 'w') as f:
    json.dump(count_dict, f)

