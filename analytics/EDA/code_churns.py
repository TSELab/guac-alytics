import subprocess
import re

def extract_languages(text):
    # Regular expression to match language lines
    language_pattern = r'^\s*(\w+(?:/\w+)?)\s+(\d+)'

    # Find all matches using the regular expression
    matches = re.findall(language_pattern, text, re.MULTILINE)

    # Create a dictionary to store the results
    languages = {}

    # Iterate through the matches and store them in the dictionary
    for match in matches:
        language, file_count = match
        languages[language] = int(file_count)

    return languages

def get_lines_of_code_with_cloc(repo_path):
    process = subprocess.Popen(["cloc", "."], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, _ = process.communicate()
    output = stdout
    lines = output.strip().split("\n")
    # Find the line containing the total lines of code
    sum_line = next((line for line in lines if line.strip().startswith("SUM:")), None)
# Extract the total lines of code value from the Code column
    if sum_line:
        total_lines_of_code = int(sum_line.split()[4])
    else:
        # If "SUM:" line is not found, find the last row with numeric values and extract the last column as total lines of code
        total_lines_of_code = 0
            
    languages = extract_languages(output)

    return {'total_lines': total_lines_of_code, 'languages': languages}

def get_code_churn(repo, tag, prev_commit):
    if prev_commit is None:
        return {'lines_added': 0, 'lines_deleted': 0, 'version_1': None, 'version_2': tag.name}

    commit_range = f"{prev_commit.hexsha}..{tag.commit.hexsha}"
    diff = repo.git.diff(commit_range, '--numstat')

    lines_added = 0
    lines_deleted = 0
    for line in diff.splitlines():
        parts = line.split()
        lines_added += int(parts[0]) if parts[0].isdigit() else 0
        lines_deleted += int(parts[1]) if parts[1].isdigit() else 0

    return {'lines_added': lines_added, 'lines_deleted': lines_deleted, 'version_1': prev_commit, 'version_2': tag.name}

