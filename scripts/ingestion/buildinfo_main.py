import time
import headerparser
import os
import re
from calendar import monthrange
from scripts.ingestion.database.buildinfo_db_init import open_db, init_db, close_db, insert_build
import progressbar


from dateutil.parser import parse as du_parse

t_in = time.time()
def parse_build_depends(entry):

    if entry is None:
        return None

    deps = entry.split("\n")[1:]
    package = []
    name=[]
    version=[]
    for dep in deps:
        d = dep.split(" (= ", 2)
        # print(dep)
        name.append(d[0].strip())
        # print(name)
        version.append(d[1].strip("),\n "))
        # print(version)
        package.append(d[0].strip() + '_' + d[1].strip("),\n "))

    result = [(x, y, z) for x, y, z in zip(package, name, version)]
    return result

def create_parser():
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
    result=[[]]
   
    if bin:
        for item1 in bin:
            m=[]
            s1=[]
            s2=[]
            for item2 in md5:
                if item1 in item2:
                    m.append(item2)
            for item2 in sha1:
                if item1 in item2:
                    s1.append(item2)

            for item2 in sha256:
                if item1 in item2:
                    s2.append(item2)
                    
            result.append([item1,m,s1,s2])
            
        output = [sublst for sublst in result if len(sublst)>0]
        # print(output)
        return output
    return None

def populate_db(location, db_location):
    walk = os.walk(location)
    print("reading buildinfos from {}".format(location))
    parser = create_parser()
    con = open_db(db_location)
    bar = progressbar.ProgressBar(redirect_stdout=True)
    
    for dirpath, dirnames, filenames in bar(walk):
        
        for filename in filenames:
            if not filename.endswith(".buildinfo"):
                continue
    
            target = os.path.join(dirpath, filename)
            print("reading {}...".format(target))
                  
            with open (target, 'r') as f:
                data = f.read() 
                data = re.sub(r'.*debian.org>$', '', data)
                result = parser.parse_string(data)
    # filenames = [k for k in os.listdir(location) if '.buildinfo' in k]
    # for file in filenames:
    #     print(file)
    #     with open ('{}/{}'.format(location,file), 'r') as f:
    # with open ('{}'.format(location), 'r') as f:
            
                # data = f.read() 
                # data = re.sub(r'.*debian.org>$', '', data)
                # result = parser.parse_string(data)

                # we short-circuit parsing to avoid further processing source builds
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
                # print('Binary   ',result['Binary'])
                # print('Build-Origin    ',result['Build-Origin'])
                # print('Md5   ',result['Checksums-Md5'])
                # print('Sha1    ',result['Checksums-Sha1'])
                # print('Sha256    ',result['Checksums-Sha256'])
                
                cur = con.cursor()
                insert_build(cur, result, build_time, deps,output) 
                con.commit()
    close_db(con)

    
if __name__ == "__main__":
    location = '/data/yellow/vineet/raw_data/buildinfo_data'
    db_location = '/data/yellow/vineet/database/bi_multi_tables.db'
    init_db(db_location)
    populate_db(location, db_location)
    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')
