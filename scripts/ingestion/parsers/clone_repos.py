import sqlite3
import os
from bs4 import BeautifulSoup
import requests
import git
from git import Repo
import logging

# logging repos that cannot be cloned

logging.basicConfig(level = logging.INFO, filename = "loginfo.log", format = '%(asctime)s %(message)s', filemode = 'w')

folder = '/data/yellow/guacalytics/raw_data/upstream_data/revised_data/clone_repos'

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

for res in result: 
    url = "https://tracker.debian.org/pkg/" + res
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.find_all('link', {'href': True, 'rel': 'vcs-git'}):
        try:
            print("cloning")
            repodir = os.path.join(os.path.abspath(folder), res)

            # if repo exists, pull newest data 

            if os.path.isdir(repodir):      
                repo = Repo(repodir) 
                repo.remotes.origin.pull()
            else: 

                # if repo not exists, clone the repos

                repo = Repo.clone_from(item['href'], repodir)

            # Getting the list of directories and check if empty

            dir = os.listdir(repodir)

            if len(dir) == 0:
                logging.error("Empty directory " + res)

        except OSError:
            logging.error("OSError " + res)

        except git.exc.GitCommandError:
            logging.error("GitCommandError " + res)
