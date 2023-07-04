#!/bin/bash 

# Register and request access from https://salsa.debian.org/public. Wait to be given access. 
# This script git clone https://salsa.debian.org/python-team/packages
# Create personal access token at https://salsa.debian.org/-/profile/personal_access_tokens
# To clone with http url use http_url_to_repo

for repo in $(curl -s --header "PRIVATE-TOKEN: my_token_here" https://salsa.debian.org/api/v4/groups/9360 | jq -r ".projects[].ssh_url_to_repo"); do git clone $repo; done;
