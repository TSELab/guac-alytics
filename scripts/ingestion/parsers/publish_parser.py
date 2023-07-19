from .publish_headerparser import parser
from ..database.publish_db_init import *
from .snapshot_download import *

def parse_packagelist(date, ARCH, db_location, DFSG):
    con = open_db(db_location)
    with open(f'./ingestion/parsers/Packagelist_DUMP/{date}-{ARCH}-{DFSG}_Packages','r') as rf:
        header = ""
        for line in rf:
            if line == "\n":
                parsed_package =  parser.parse_string(header).normalized_dict()
                parsed_package["added_at"] = date
                cur = con.cursor()
                parsed_package["architecture"] = ARCH
                parsed_package["provided_by"] = ""
                insert_package(cur, parsed_package, DFSG)
                provided_by = cur.lastrowid
                for provided_package in parsed_package["provides"]:
                    parsed_package["package"] = provided_package
                    parsed_package["version"] = ""
                    parsed_package["size"] = ""
                    parsed_package["provided_by"] = provided_by
                    insert_package(cur, parsed_package, DFSG)
                con.commit()
                header = ""
            else:
                header += line
    close_db(con)
    return

def parse_dependencylist(date, ARCH, db_location, DFSG):
    con = open_db(db_location)
    with open(f'./ingestion/parsers/Packagelist_DUMP/{date}-{ARCH}-{DFSG}_Packages','r') as rf:
        header = ""
        for line in rf:
            if line == "\n":
                parsed_package =  parser.parse_string(header).normalized_dict()
                for dependency_list in parsed_package["depends"]:
                    for dependency_condition in dependency_list:
                        packages = dependency_condition.split('|') if '|' in dependency_condition else [dependency_condition]

                        for dependency_package_name in packages:
                            if '(' in dependency_package_name:
                                dependency_package_name = dependency_package_name.split('(')[0]
                            
                            cur = con.cursor()
                            insert_dependency(cur, parsed_package["package"], parsed_package["version"], ARCH, dependency_condition, dependency_package_name)
                            con.commit()
                header = ""
            else:
                header += line
    close_db(con)
    return

def populate_DB(date, ARCH, LOCATION):
    init_db(LOCATION)
    for DFSG in ["main", "contrib", "non-free"]:
        parse_packagelist(date, ARCH, LOCATION, DFSG)
        parse_dependencylist(date, ARCH, LOCATION, DFSG)