from ingestion.parsers.snapshot_download import get_snapshot_bydate, date_to_ISO
from ingestion.parsers.publish_parser import populate_DB
from ingestion.parsers.graph_generator import generate_graph
import datetime
from ingestion.database.publish_db_init import *

if __name__ == "__main__":
    LOCATION = 'debian_packages.db'
    ARCH = "amd64"
    date = datetime.date(2016, 12, 31)
    end_date = datetime.date(2022, 12, 31)
    while date < end_date:
        print(date.strftime("%Y-%m-%d"))
        get_snapshot_bydate(date_to_ISO(date.strftime("%Y-%m-%d")), ARCH)
        populate_DB(date_to_ISO(date.strftime("%Y-%m-%d")), ARCH, LOCATION)
        # generate_graph(date, ARCH)
        date += datetime.timedelta(days=90)
    pass