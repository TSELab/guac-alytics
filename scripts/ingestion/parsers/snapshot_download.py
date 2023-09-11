import requests
import gzip
from os.path import exists

def get_snapshot_bydate(DATE, ARCH):
    for DFSG in ["main", "contrib", "non-free"]:
        if exists(f"./ingestion/parsers/Packagelist_DUMP/{DATE}-{ARCH}-{DFSG}_Packages.dump"):
            continue # don't re-download
        while True:
            url = f"http://snapshot.debian.org/archive/debian/{DATE}/dists/stable/{DFSG}/binary-{ARCH}/Packages.gz"
            resp = requests.get(url)
            if resp.status_code == 200:
                decompressed_file = gzip.decompress(resp.content)
                with open(f"./ingestion/parsers/Packagelist_DUMP/{DATE}-{ARCH}-{DFSG}_Packages.dump", "w") as f:
                    f.write(decompressed_file.decode('utf-8'))
                break
            else:
                print("Error: " + str(resp.status_code), url)
                print("Retrying...")
    return