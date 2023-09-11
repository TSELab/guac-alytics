from ingestion.parsers.snapshot_download import get_snapshot_bydate
from ingestion.parsers.publish_parser import populate_DB
from ingestion.parsers.graph_generator import generate_graph
import datetime
import argparse

def parse_date_arg(arg):
    try:
        return datetime.date.fromisoformat(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Please use the ISO date format 'YYYY-MM-DD'.")

def date_to_iso_str(date):
    return date.strftime("%Y%m%dT%H%M%S") + "Z"

def process_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("start_date", nargs="?", type=parse_date_arg, default=datetime.date(2016, 12, 31), help="Start date in 'YYYY-MM-DD' format.")
    parser.add_argument("end_date", nargs="?", type=parse_date_arg, default=datetime.date(2022, 12, 31), help="End date in 'YYYY-MM-DD' format.")
    parser.add_argument("--location", default="debian_publish_packages.db", help="Location to store the database.")
    parser.add_argument("--arch", default="amd64", help="Architecture type (default: amd64).")
    return parser.parse_args()

if __name__ == "__main__":
    args = process_command_line_args()

    start, end, LOCATION, ARCH = args.start_date, args.end_date, args.location, args.arch

    while start < end:
        print(start)

        get_snapshot_bydate(date_to_iso_str(start), ARCH)
        populate_DB(date_to_iso_str(start), ARCH, LOCATION)

        # generate_graph(date, ARCH)

        start += datetime.timedelta(days=90)
