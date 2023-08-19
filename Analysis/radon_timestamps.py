import subprocess
import os
import git
from prettytable import PrettyTable
from get_licenses import get_license

def run_git_config(repo_path):
    git_config_command = ["git", "config", "--global", "--add", "safe.directory", repo_path]
    subprocess.run(git_config_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    checkout_command = ["git", "reset", "--hard"]
    subprocess.run(checkout_command, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


def run_radon_cc(repo_path):
    try:
        repo = git.Repo(repo_path)  
    
        if repo:
            output = {}
            tags = repo.tags
            original_dir = os.getcwd()

            # Change to the specified directory
            os.chdir(repo_path)
        
        
            if tags and len(tags)>0:
                # Fetch tags from the remote repository
                # repo.remotes.origin.fetch(tags)
                for tag in tags:
                    # print(tag.name)
                    code_stats = {}
                    try:
                    # Checkout the specific tag
                        repo.git.checkout(tag)
                        initial_commit = repo.head.commit
                        time = initial_commit.authored_datetime
                        # print(time)
                    except git.GitCommandError as e:
                        if "The following untracked working tree files would be overwritten by checkout:" in str(e.stderr):
                            print("Untracked files detected. Cleaning and trying again...")
                            repo.git.clean('-df')  # Clean untracked files
                            repo.git.checkout(tag)  # Retry checkout
                        else:
                            # Handle other GitCommandError cases
                            break
                        
                    command = ["radon", "cc", ".", "-a"]
                    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    res = result.stdout.decode('utf-8')
                    res = res.split("\n")
                    res = res[len(res)-2]
                    res = res.split(":")
                    cc = res[len(res)-1]
                    # print(cc)    
                    licenses = get_license(repo_path)
                    if licenses is None:
                        licenses = {tag.name:"No CopyRight File"}
                        
                    # print(licenses)
                    
                    code_stats['timestamp'] = time
                    code_stats['cc'] = cc
                    code_stats['license'] = licenses
                    
                    output[tag.name] = code_stats
                
                os.chdir(original_dir)
                                        
                return output
        
    except git.InvalidGitRepositoryError:
        pass
    return None  

if __name__ == "__main__":

    myTable = PrettyTable([" Package "," Tag ", " Timestamp "," Cyclomatic Complexity "," Licenses "])
    repositories_path = "/data/yellow/guacalytics/raw_data/upstream_clones/clone_repos"
    output_file = '/data/yellow/guacalytics/python_files/Analysis/radon_results.md'
    
    start = 0
    end = 1000 
    # Adjust the value based on the packages and till the last package
    batch_size = 100  # Adjust this value based on available memory
    
    counter = 0
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
            counter += 1
            
            # Get lines of code per version and code churn
            results = run_radon_cc(repo_path)

            if results is not None:
                i = 0
                for tag, stats in results.items():
                    if i % batch_size == 0:
                        data = myTable.get_string()
                        with open(output_file, 'a') as f:
                            f.write(data)
                        myTable.clear_rows()
                    
                    myTable.add_row([repo_name, tag, stats['timestamp'], stats['cc'], stats['license']])
                    i += 1
                
    # Write the remaining data to the output file
    data = myTable.get_string()
    with open(output_file, 'a') as f:
        f.write(data)
