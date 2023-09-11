import os
import re

def extractDependencies(control_content,keyName):
    parsed_output = []
    lines = control_content.strip().split('\n')
    flag = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(keyName):
            dependencies = line.split(":")
            if dependencies[1] is not "":
                dependencies = dependencies[1].split(",")
                if dependencies[len(dependencies)-1] == "":
                    parsed_output.extend(dependencies[:len(dependencies)-1])
                else:
                    parsed_output.extend(dependencies)
            flag =1
            continue
        if re.search(".*\${.*}.*",line):
            continue
        if ":" in line:
            flag =0
            continue
        if flag==1:
            dependencies = line.split(",")
            if dependencies[len(dependencies)-1] == "":
                    parsed_output.extend(dependencies[:len(dependencies)-1])
            else:
                parsed_output.extend(dependencies)
    return len(parsed_output)


def get_control_file_versions(repo_path,tag):
    control_files = {}
    depends_count = 0
    build_depends_count = 0

    control_file = os.path.join(repo_path, 'debian', 'control')
    if os.path.exists(control_file):
        control_files[tag.name] = control_file 
        
        try:
            with open(control_file, 'r', encoding='utf-8') as f:
                control_content = f.read()
                depends_count = extractDependencies(control_content,"Depends:")
                build_depends_count = extractDependencies(control_content,"Build-Depends:")
        except UnicodeDecodeError:
            pass

    return depends_count,build_depends_count
