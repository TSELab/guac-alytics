import os 
import json 
from pathlib import Path

src = '/Users/jialincheoh/repo-test'


for fname in os.listdir(src):
    # build the path to the folder
    folder_path = os.path.join(src, fname)

    if os.path.isdir(folder_path):
        # we are sure this is a folder; now lets iterate it

        file_path = os.path.join(folder_path, "debian/control")
        with Path(file_path).open() as file:   # be sure to adjust your path
            commands, description = {}, ''
            for line in file:
                if not line.strip(): continue  # if line is blank continue loop
                if ':' in line:
            # use 'maxsplit=1' to split only the first occurance of ':'
                    command, description = list(map(str.strip, line.split(':', maxsplit=1)))
                else:
            # if not ':' in line append line to description
                    description += ' %s' % line.strip()
                commands[command] = description
      
        fp = Path('test.json').open('a')
        fp.write(json.dumps(commands, indent=4))
        fp.close()
        print(fname)
