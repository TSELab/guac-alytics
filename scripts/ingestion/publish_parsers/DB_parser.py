import sqlite3

def init_db(location):
    conn = sqlite3.connect(location)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Publish_Packages ("
                   "Package_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "Package varchar,"
                   "Architecture varchar,"
                   "Version varchar,"
                   "Section varchar,"
                   "Size varchar,"
                   "pool_endpoint varchar,"
                   "DFSG varchar,"
                   "Added_at TIMESTAMP,"
                   "MD5sum varchar,"
                   "SHA256 varchar,"
                   "Provided_by varchar,"
                   "Unique (Package, Architecture, Version) ON CONFLICT IGNORE"
                   ")")  
    
    cur.execute("CREATE TABLE IF NOT EXISTS Publish_Dependencies ("
                   "Dependency_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "Package_id INTEGER,"
                   "Dependency_package_id INTEGER,"
                   "Condition varchar,"
                   "FOREIGN KEY (Package_id) REFERENCES Publish_Packages (Package_id)"
                   "ON DELETE CASCADE ON UPDATE CASCADE,"
                   "FOREIGN KEY (Dependency_Package_id) REFERENCES Publish_Packages (Package_id)"
                   "ON DELETE CASCADE ON UPDATE CASCADE"
                   ")")

    conn.commit()
    conn.close()

def open_db(location):
    conn = sqlite3.connect(location)
    return conn

def close_db(conn = None):
    if not conn:
        raise Exception("I need a database handle to close!")
    conn.close()

INSERT_PACKAGE = '''INSERT OR IGNORE INTO Publish_Packages (package, architecture, version, section, size, pool_endpoint, DFSG, added_at, md5sum, sha256, provided_by) VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
INSERT_DEPENDENCY = '''INSERT OR IGNORE INTO Publish_Dependencies (package_id, condition, dependency_package_id) VALUES (?,?,?)'''

def insert_package(cur, package_data, DFSG):
    cur.execute(INSERT_PACKAGE, (package_data['package'], package_data['architecture'], package_data['version'], package_data['section'], package_data['size'], package_data['filename'], DFSG, package_data['added_at'], package_data['md5sum'], package_data['sha256'], package_data['provided_by']))

def insert_dependency(cur, package, version, architecture, dependency_condition, dependency):
    
    package_query = "SELECT Package_id FROM Publish_Packages WHERE Package = ? AND Version = ? AND Architecture = ?"
    dependency_query = "SELECT Package_id FROM Publish_Packages WHERE Package = ? AND Architecture = ?"

    package_id = cur.execute(package_query, (package, version, architecture)).fetchone()
    if package_id:
        dependency_id = cur.execute(dependency_query, (dependency, architecture)).fetchone()
        if dependency_id:
            cur.execute(INSERT_DEPENDENCY, (package_id[0], dependency_condition, dependency_id[0]))
        # else:
        #     print("Dependency not found", dependency)
        # cur.execute(INSERT_DEPENDENCY, (package_id[0], dependency_condition, dependency))
    else:
        print("Package not found:", package, version, architecture)