import sqlite3
import requests
from bs4 import BeautifulSoup
import os
import git
import logging
import subprocess
import shutil
import pickle
import sys
import time
from multiprocessing import Pool
import argparse

username = '' # give your username
TOKEN = ""  # give your own tokens
repo_dir = "./clone_repos"
log_file = "clone_errors.log"
hashes_file = "hashes.pkl"
logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

def load_hashes_from_file():
    try:
        with open(hashes_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def calculate_head_commit(repo_path, package_name):
    try:
        result = subprocess.run(['git', '-C', repo_path, 'rev-parse', 'HEAD'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error calculating head commit: {e}")
    return None

def is_large_repo(repo_path, size_threshold = 200 * 1024 * 1024):
    try:
        result = subprocess.run(['du', '-sb', repo_path], capture_output=True, text=True)
        if result.returncode == 0:
            size_str = result.stdout.split()[0]  # Extract size as a string
            size_bytes = int(size_str)  # Convert to bytes
            return size_bytes > size_threshold
    except subprocess.CalledProcessError as e:
        print(f"Error checking repository size: {e}")
    return False

def symlink_repository(repo_name, repo_path):
    if is_large_repo(repo_path):
        head_commit = calculate_head_commit(repo_path, repo_name)
        if head_commit:
            if head_commit in large_repos:
                shutil.rmtree(repo_path)
                # Found a similar repository, create a symlink
                similar_repo_name = large_repos[head_commit]
                # print(f"Found similar repository: {repo_name} is similar to {similar_repo_name}")
                symlink_path = os.path.join(repo_dir, repo_name)
                target_repo_path = os.path.join(repo_dir, similar_repo_name)
                if not os.path.exists(symlink_path):
                    os.symlink(target_repo_path, symlink_path)
                    print(f"Symlink created for {repo_name} to {similar_repo_name}")
                return True
            else:
                large_repos[head_commit] = repo_name
                with open(hashes_file, 'wb') as f:
                    pickle.dump(large_repos, f)
                print(f"Added {repo_name} to large_repos")
                return False
                

def get_distinct_packages(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    #        WHERE package LIKE '%firefox%'
    cur.execute("""
        SELECT DISTINCT Package
        FROM Publish_Packages
    """)

    distinct_packages = [row[0] for row in cur.fetchall()]

    conn.close()

    return distinct_packages

def get_vcs_url(package_name):
    package_url = f"https://tracker.debian.org/pkg/{package_name}"
    response = requests.get(package_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        vcs_url = soup.find('link', {'rel':"vcs-git"})
        if vcs_url:
            return vcs_url['href']
    return None

def is_repo_cloned(package_name):
    try:
        # Use subprocess to execute the 'ls' command
        path = os.path.join(repo_dir, package_name)
        cmd = f"ls {path}"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # If the return code is 0, the directory exists
        return result.returncode == 0
    except Exception as e:
        # Handle exceptions if the command execution fails
        print(f"Error checking directory existence: {e}")
        return False

def get_commit_count_within_range(repo_path, start_date, end_date, branch):
    cmd = [
        'git',
        '-C', repo_path,
        'rev-list',
        '--count',
        '--since', start_date,
        '--until', end_date,
        branch
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        commit_count = int(result.stdout.strip())
        return commit_count
    else:
        return None

def get_default_branch(repo_path):
    try:
        # Use 'git remote show origin' to get remote information
        result = subprocess.run(['git', '-C', repo_path, 'remote', 'show', 'origin'], capture_output=True, text=True)
        if result.returncode == 0:
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if line.strip().startswith('HEAD branch:'):
                    return line.split(':')[1].strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting default branch: {e}")
    return None

def clone_repository(package_name, vcs_url, start_date, end_date):
    repo_path = os.path.join(repo_dir, package_name)

    if not os.path.exists(repo_path):
        try:
            # Clone the repository without specifying the branch and depth initially
            git.Repo.clone_from(
                f"https://{username}:{TOKEN}@" + vcs_url.split('//')[1],
                repo_path
            )

            default_branch = get_default_branch(repo_path)
            print(f"Default branch for {package_name}: {default_branch}")

            # Process the repository to check for similarity and create submodules/symlinks
            if symlink_repository(package_name, repo_path):
                # shutil.rmtree(repo_path)
                return
            # else:
            #     # Avoid recloning a large repo and clone with full depth
            #     print(f"Cloned repository for {package_name} from {vcs_url} to {repo_path}")
            #     return

            # Calculate the depth needed based on the date range and default branch
            commit_count = get_commit_count_within_range(repo_path, start_date, end_date, default_branch)

            if commit_count is not None:
                shutil.rmtree(repo_path)

                # Reclone the repository using the calculated depth and default branch
                git.Repo.clone_from(
                    f"https://{username}:{TOKEN}@" + vcs_url.split('//')[1],
                    repo_path,
                    depth=commit_count + 1,
                    branch=default_branch
                )

                print(f"Cloned repository for {package_name} from {vcs_url} to {repo_path}")
            else:
                print(f"Unable to determine commit count for {package_name}. Skipping.")
        except git.exc.GitCommandError as e:
            error_message = f"Error cloning {package_name} from {vcs_url}: {str(e)}"
            print(error_message)
            logging.error(error_message)
        except git.exc.NoSuchPathError as e:
            error_message = f"Error cloning {package_name} from {vcs_url}: {str(e)}"
            print(error_message)
            logging.error(error_message)

def clone_packages(packages):
    for package in packages:
        if is_repo_cloned(package):
            continue
        vcs_url = get_vcs_url(package)
        if vcs_url:
            if "salsa.debian.org" in vcs_url:
                clone_repository(package, vcs_url.split(" ")[0], start_date, end_date)
    return

if __name__ == "__main__":
    start_date = "2017-01-01"
    end_date = "2022-12-31"
    
    # Load large repositories from file
    large_repos = load_hashes_from_file()

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="A script that uses a specified number of processes.")

    # Add a mandatory argument for the number of processes
    parser.add_argument("num_processes", type=int, help="Number of processes to use")

    # Parse the command-line arguments
    args = parser.parse_args()

    distinct_packages = get_distinct_packages("/data/cyan/guacalytics/database/bi_multi_tables.db")
    print(f"Total number of repos is {len(distinct_packages)}")

    num_processes = args.num_processes  # Adjust the number of processes as needed

    # Calculate the chunk size and distribute the remainder among processes
    chunk_size, remainder = divmod(len(distinct_packages), num_processes)
    packages_chunks = [distinct_packages[i:i + chunk_size] for i in range(0, len(distinct_packages), chunk_size)]

    packages_chunks[num_processes - 1] += distinct_packages[-chunk_size:]

    
    with Pool(num_processes) as pool:
        pool.map(clone_packages, packages_chunks)

