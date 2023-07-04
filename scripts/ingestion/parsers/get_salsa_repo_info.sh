#!/bin/bash

# Get all the repo information with attributes at https://docs.gitlab.com/ee/api/groups.html#list-groups

# Output repo information to a file called projects.json 

# Input is https://salsa.debian.org/python-team/packages

curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" "https://salsa.debian.org/api/v4/groups/9360/projects?per_page=10000" | jq 'map({ id: .id, name: .name, ssh_url: .ssh_url_to_repo, http_url: .http_url_to_repo, created_at: .created_at, statistics: .statistics,  star_count: .star_count, forks_count: .forks_count, last_activity_at: .last_activity_at, created_at: .created_at, path: .path, default_branch_protection: .default_branch_protection, open_issues_count: .open_issues_count, visibility: .visibility, archived: .archived, description: .description, topics: .topics, issues_enabled: .issues_enabled, merge_requests_enabled: .merge_requests_enabled, shared_with_groups: .shared_with_groups, request_access_enabled: .request_access_enabled })' > projects.json
