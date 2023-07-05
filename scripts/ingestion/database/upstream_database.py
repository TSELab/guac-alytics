import sqlite3
import json
from datetime import datetime

# Read the JSON file
with open('/data/yellow/guacalytics/raw_data/upstream_data/projects.json') as file:
    data = json.load(file)

# Connect to the database
conn = sqlite3.connect('/data/yellow/guacalytics/database/bi_multi_tables.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''CREATE TABLE IF NOT EXISTS upstream_data (
                    sno INTEGER PRIMARY KEY,
                    id INTEGER,
                    name VARCHAR,
                    ssh_url VARCHAR,
                    http_url VARCHAR,
                    created_at VARCHAR,
                    statistics VARCHAR,
                    star_count INTEGER,
                    forks_count INTEGER,
                    last_activity_at VARCHAR,
                    path VARCHAR,
                    default_branch_protection VARCHAR,
                    open_issues_count VARCHAR,
                    visibility VARCHAR,
                    archived TEXT,
                    description VARCHAR,
                    topics VARCHAR,
                    issues_enabled TEXT,
                    merge_requests_enabled TEXT,
                    shared_with_groups VARCHAR,
                    request_access_enabled TEXT
                )''')

# Insert the data into the table
for item in data:
    id = item['id']
    name = item['name']
    ssh_url = item['ssh_url']
    http_url = item['http_url']
    created_at = datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y %H:%M:%S')
    statistics = item['statistics']
    star_count = item['star_count']
    forks_count = item['forks_count']
    last_activity_at = datetime.strptime(item['last_activity_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y %H:%M:%S')
    path = item['path']
    default_branch_protection = item['default_branch_protection']
    open_issues_count = item['open_issues_count']
    visibility = item['visibility']
    archived = item['archived']
    description = item['description']
    topics = json.dumps(item['topics'])
    issues_enabled = item['issues_enabled']
    merge_requests_enabled = item['merge_requests_enabled']
    shared_with_groups = json.dumps(item['shared_with_groups'])
    request_access_enabled = item['request_access_enabled']

    request_access_enabled = 'True' if request_access_enabled == 1 else 'False'
    merge_requests_enabled = 'True' if merge_requests_enabled == 1 else 'False'
    issues_enabled = 'True' if issues_enabled == 1 else 'False'
    archived = 'True' if archived == 1 else 'False'

    # Insert the data into the table
    cursor.execute('''INSERT OR IGNORE INTO upstream_data VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                   (id, name, ssh_url, http_url, created_at, statistics, star_count, forks_count, last_activity_at,
                    path, default_branch_protection, open_issues_count, visibility, archived, description, topics,
                    issues_enabled, merge_requests_enabled, shared_with_groups, request_access_enabled))


# Commit the changes and close the connection
conn.commit()
conn.close()
