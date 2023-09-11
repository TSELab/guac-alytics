import time
import headerparser
import os
import re
from calendar import monthrange
from ingestion.database.buildinfo_db_init import open_db, init_db, close_db, insert_build
from ingestion.constants import LOC,DB_LOC
import progressbar
from dateutil.parser import parse as du_parse

t_in = time.time()

def parse_build_depends(entry):
    """Parse the Installed-Build-Depends field from a buildinfo file.

    Args:
        entry (str): The Installed-Build-Depends field.

    Returns:
        list: A list of tuples containing package names, versions, and package names with versions.
    """
    if entry is None:
        return None

    deps = entry.split("\n")[1:]
    package = []
    name=[]
    version=[]
    for dep in deps:
        d = dep.split(" (= ", 2)
        name.append(d[0].strip())
        version.append(d[1].strip("),\n "))
        package.append(d[0].strip() + '_' + d[1].strip("),\n "))

    result = [(x, y, z) for x, y, z in zip(package, name, version)]
    return result

def create_parser():
    """Parse the buildinfo page for headers

    Returns:
        list: A list of headers found in the package description
    """
    parser = headerparser.HeaderParser()
    parser.add_field("Format")
    parser.add_field("Source", default=None)
    parser.add_field("Binary", default=None)
    parser.add_field("Architecture", default=None)
    parser.add_field("Version", default=None)
    parser.add_field("Checksums-Sha1", default=None)
    parser.add_field("Checksums-Md5", default=None)
    parser.add_field("Checksums-Sha256", default=None)
    parser.add_field("Build-Origin", default=None)
    parser.add_field("Build-Architecture", default=None)
    parser.add_field("Build-Date", default=None)
    parser.add_field("Build-Path", default=None)
    parser.add_field("Installed-Build-Depends", None)
    parser.add_field("Environment", default=None)
    parser.add_additional()
    return parser

def parse_checksum(bin,md5,sha1,sha256):
    """Parse the Checksums-Md5, Checksums-Sha1, and Checksums-Sha256 fields from a buildinfo file.

    Args:
        bin (list): A list of binary package names.
        md5 (list): A list of Md5 checksums.
        sha1 (list): A list of Sha1 checksums.
        sha256 (list): A list of Sha256 checksums.

    Returns:
        list: A list of lists, where each sublist contains a binary package name, a list of Md5 checksums,
              a list of Sha1 checksums, and a list of Sha256 checksums.
    """
    
    result=[[]]
   
    if bin:
        for item1 in bin:
            md=[]
            sha=[]
            sha2=[]
            for item2 in md5:
                if item1 in item2:
                    md.append(item2)
            for item2 in sha1:
                if item1 in item2:
                    sha.append(item2)

            for item2 in sha256:
                if item1 in item2:
                    sha2.append(item2)
                    
            result.append([item1,md,sha,sha2])
            
        output = [sublst for sublst in result if len(sublst)>0]
        return output
    return None

def populate_db(location, db_location):
    """Populate a database with buildinfo files in a directory.

    Args:
        location (str): The directory containing buildinfo files.
        db_location (str): The path to the database file.
    """
    walk = os.walk(location)
    print("reading buildinfos from {}".format(location))
    parser = create_parser()
    con = open_db(db_location)
    bar = progressbar.ProgressBar(redirect_stdout=True)
    
    for dirpath, dirnames, filenames in bar(walk):
        
        for filename in filenames:
            if not filename.endswith(".buildinfo"):  # Walking through the folders to find all the buildinfo files
                continue
    
            target = os.path.join(dirpath, filename)
            print("reading {}...".format(target))
                  
            with open (target, 'r') as f:
                data = f.read() 
                data = re.sub(r'.*debian.org>$', '', data)
                result = parser.parse_string(data)
                
                # Filling Null values if the header is not present in the data
                if result['Architecture'] == 'source':
                    continue
                if result['Architecture'] == "all source":
                    result['Architecture'] = 'all'

                if 'Installed-Build-Depends' in result:
                    deps = parse_build_depends(result['Installed-Build-Depends'])
                else:
                    deps=None
                    
                if result['Build-Date'] is not None:
                    build_time = du_parse(result['Build-Date']).isoformat()
                else:
                    build_time=None
                
                if 'Binary' in result and result['Binary']:
                    result['Binary'] = result["Binary"].split(" ")
                else:
                    result['Binary'] = None

                if 'Checksums-Md5' in result and result['Checksums-Md5']:
                    result['Checksums-Md5'] = result["Checksums-Md5"].split("\n")[1:]
                    result['Checksums-Md5'] = [elem.strip() for elem in result['Checksums-Md5']]
                else:
                    result['Checksums-Md5'] = None
                    
                if 'Checksums-Sha1' in result and result['Checksums-Sha1']:
                    result['Checksums-Sha1'] = result["Checksums-Sha1"].split("\n")[1:]
                    result['Checksums-Sha1'] = [elem.strip() for elem in result['Checksums-Sha1']]
                else:
                    result['Checksums-Sha1'] = None
                    
                if 'Checksums-Sha256' in result and result['Checksums-Sha256']:
                    result['Checksums-Sha256'] = result["Checksums-Sha256"].split("\n")[1:]
                    result['Checksums-Sha256'] = [elem.strip() for elem in result['Checksums-Sha256']]
                else:
                    result['Checksums-Sha256'] = None
                 
                output=parse_checksum(result['Binary'],result['Checksums-Md5'],result['Checksums-Sha1'],result['Checksums-Sha256'])   
               
                cur = con.cursor()
                
                # to insert records into the table
                insert_build(cur, result, build_time, deps,output) 
                con.commit()
    close_db(con)

    
if __name__ == "__main__":
    init_db(DB_LOC)  # Initializing the database
    populate_db(LOC, DB_LOC)    # Populating the data
    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')
