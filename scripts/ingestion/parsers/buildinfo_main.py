import sqlite3
import headerparser
import os
import sys
import re
from calendar import monthrange


from dateutil.parser import parse

conn = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cur = conn.cursor()   

# Parsing dependenies in each file
def parse_build_depends(entry):
    deps = entry.split("\n")[1:]
    package = []
    for dep in deps:
        name, version = dep.split(" (= ", 2)
        package.append(name.strip() + '_' + version.strip("),\n "))
    return package


def populate_db(location):

    # Using parser to parse the headers from buildinfo file
    parser = headerparser.HeaderParser()
    parser.add_field("Format")
    parser.add_field("Source")
    parser.add_field("Binary")
    parser.add_field("Installed-Build-Depends")
    parser.add_additional()  # Get all the other headers present

    print(location)
    filenames = [k for k in os.listdir(location) if '.buildinfo' in k]   # Getting all the buildinfo files on the given day
    
    for file in filenames:
        # print(file)
        with open ('{}/{}'.format(location,file), 'r') as f:
            data = f.read() 
            data = re.sub(r'.*debian.org>$', '', data)
            result = parser.parse_string(data)      # Parsing the data
            
            # Filling Null values if the header is not present in the data
            if 'Installed-Build-Depends' in result:
                deps = parse_build_depends(result['Installed-Build-Depends'])
            else:
                deps=None
            
            if 'Build-Date' in result:
                build_time = parse(result['Build-Date']).isoformat()
            else:
                build_time=None

            if 'Source' not in result:
                result['Source']=None
            if 'Version' not in result:
                result['Version']=None
            if 'Architecture' not in result:
                result['Architecture']=None
          
            #insert records into the table
            cur.execute('''INSERT OR REPLACE INTO buildinfo_data (source,version, arch, time, deps) VALUES (?,?,?,?,?)''',(result['Source'], result['Version'], result['Architecture'], build_time, str(deps)))
            conn.commit()
        

    
if __name__ == "__main__":

    if len(sys.argv) < 1:
        print("No path given. What do you want me to insert?")
        sys.exit(1)

    for year in range(2017,2023):
        for mon in range(1,13):
            x=monthrange(year,mon)
            for day in range(1,x[1]+1):
                populate_db('/data/yellow/vineet/raw_data/buildinfo_data/{:4d}/{:02d}/{:02d}'.format(year, mon, day))
    
    print("done")

print("closing handle")
conn.close() #close the connection
