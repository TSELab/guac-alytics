import os 
import json 
from pathlib import Path

# adjust this path when moving to the tower
src = '/Users/jialincheoh/repo-test'

result = []
for fname in os.listdir(src):

    # build the path to the folder
    folder_path = os.path.join(src, fname)
    
    # making sure this is a folder, now we can iterate it
    if os.path.isdir(folder_path):
 
        file_path = os.path.join(folder_path, "debian/control")

        with Path(file_path).open() as file:
            commands, description = {}, ''
            for line in file:

            	# if line is blank continue loop
                if not line.strip(): 
                	continue  

                # use 'maxsplit=1' to split only the first occurance of ':'
                if ':' in line:
                    command, description = list(map(str.strip, line.split(':', maxsplit=1)))
                else:

                    # if not ':' in line append line to description
                    description += ' %s' % line.strip()
                commands[command] = description
        print(commands)
        result.append(commands)
        fp = Path('upstream.json').open('w')
        fp.write(json.dumps(result, indent=4))
        fp.close()
        print(fname)

