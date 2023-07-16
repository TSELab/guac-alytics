import sqlite3
import os
from bs4 import BeautifulSoup
import requests
import git

# read from source_name in source_table 

conn = sqlite3.connect('/data/yellow/guacalytics/database/bi_multi_tables.db')
cursor = conn.cursor()
query = '''SELECT distinct(source_name) from source_table1'''
cursor.execute(query)
items = cursor.fetchall()
result = []
for item in items:
    value = item[0]
    value = value.split(' ')[0]  # Remove everything after the space
    if value not in result:
        result.append(value)
print(result)
conn.close() 

# in https://packages.debian.org/stable/, we have developer information that links to https://tracker.debian.org/pkg/
# build URL from source_name
# clone all the repos 

repos = []
for res in result: 
    url = "https://tracker.debian.org/pkg/" + res
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.find_all('link', {'href': True, 'rel': 'vcs-git'}):
        repos.append(item['href'])
print(repos)

for repo in repos:
    
# if cannot clone repos (repos with errors), continue

    try: 
        os.mkdir(res)
        print("cloning")
        repo = git.Repo.clone_from(repo, to_path = res)
    except OSError:
        continue
