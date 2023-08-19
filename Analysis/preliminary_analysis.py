import os
import git
import subprocess
import re
from prettytable import PrettyTable
import time
from datetime import datetime
from depends import get_control_file_versions
from loc_churns import get_code_churn,get_lines_of_code_with_cloc

def run_git_config(repo_path):
    git_config_command = ["git", "config", "--global", "--add", "safe.directory", repo_path]
    subprocess.run(git_config_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    checkout_command = ["git", "reset", "--hard"]
    subprocess.run(checkout_command, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

def count_lines_of_code(repo_path):
    try:
        repo = git.Repo(repo_path)  
    
        if repo:
            lines_of_code = {}
            tags = repo.tags
            
            if tags and len(tags)>0:
                # Fetch tags from the remote repository
                # repo.remotes.origin.fetch(tags)
                patch_count = 0
                prev = None
                prev_commit = None
                for tag in tags:
                    try:
                    # Checkout the specific tag
                        repo.git.checkout(tag)
                        
                    except git.GitCommandError as e:
                        if "The following untracked working tree files would be overwritten by checkout:" in str(e.stderr):
                            print("Untracked files detected. Cleaning and trying again...")
                            repo.git.clean('-df')  # Clean untracked files
                            repo.git.checkout(tag)  # Retry checkout
                        else:
                            # Handle other GitCommandError cases
                            break
                    # Get the lines of code and code churn for the current tag
                    code_stats = get_lines_of_code_with_cloc(repo_path)
                    code_churn = get_code_churn(repo, tag, prev_commit)

                    code_stats['version_1'] = prev
                    code_stats['version_2'] = code_churn['version_2']
                    code_stats['lines_added'] = code_churn['lines_added']
                    code_stats['lines_deleted'] = code_churn['lines_deleted']
                    
                    tracked_files = repo.git.ls_files("*.patch").splitlines()
                    patch_count = len(tracked_files)
                    code_stats['patch_count'] = patch_count
                    
                    if "debian" in tag.name:
                        depends_count,build_depends_count = get_control_file_versions(repo_path,tag)
                        code_stats['depends_count'] = depends_count
                        code_stats['build_depends_count'] = build_depends_count

                    else:
                        code_stats['depends_count'] = 0
                        code_stats['build_depends_count'] = 0
                    
                    lines_of_code[tag.name] = code_stats
                    prev = tag.name
                    prev_commit = tag.commit
                    

                return lines_of_code
        
    except git.InvalidGitRepositoryError:
        pass
    return None  

if __name__ == "__main__":
    print(datetime.now())
    t_in = time.time()
    repositories_path = "/data/yellow/guacalytics/raw_data/upstream_clones/clone_repos"

    myTable = PrettyTable(["Package "," Tag "," loc "," Versions Compared "," lines added "," lines deleted "," languages "," build depends "," depends "," patch files "])
    counter = 0
    start = 1
    end = 1000
    for repo_name in os.listdir(repositories_path):
        if counter < start:
            counter += 1
            continue
        if counter > end:
            break
        repo_path = os.path.join(repositories_path, repo_name)
        if os.path.exists(os.path.join(repo_path, ".git")):
            run_git_config(repo_path)
            print(counter," ",repo_name)
            counter+=1

        # Get lines of code per version and code churn
            lines_of_code_per_version = count_lines_of_code(repo_path)

            if lines_of_code_per_version is not None:
                i=0
                for tag, stats in lines_of_code_per_version.items():
                    stats['version_1'] = stats['version_1'] if stats['version_1'] is not None else ''
                    myTable.add_row([repo_name ,tag,stats['total_lines'],stats['version_1']+'-'+stats['version_2'],stats['lines_added'],stats['lines_deleted'],stats['languages'],stats['build_depends_count'],stats['depends_count'],stats['patch_count']])
                    i+=1

    data = myTable.get_string()
    with open('/data/yellow/guacalytics/python_files/Analysis/complexity.md', 'w') as f:
        f.write(data)
            
    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')
