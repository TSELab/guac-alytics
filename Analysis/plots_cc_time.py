import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns
from dateutil import parser

def is_numeric(value):
    return bool(re.match(r'^\d+(\.\d+)?$', value))

def process_cc_value(cc_value):
    if 'A' in cc_value or 'B' in cc_value or 'C' in cc_value:
        match = re.search(r'\((.*?)\)', cc_value)
        if match:
            numeric_part = match.group(1)
            if is_numeric(numeric_part):
                return float(numeric_part)
    elif any(keyword in cc_value for keyword in ['{', 'invalid', 'unknown', '*']):
        return 0
    return 0

def fetch_data_from_md(md_file_path):
    timestamp = []
    cc = []

    with open(md_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line != '+----------------------------------------------------------+------------------------------------------+':
                items = [item.strip() for item in line.split('|') if item.strip()]
                if len(items) >= 4 and items[0] != '-' and items[0] != 'Package':
                    timestamp.append(items[2])
                    cc_value = items[3]
                    cc_value_processed = process_cc_value(cc_value)
                    cc.append(cc_value_processed)
                    
    return timestamp, cc

def build_plots(timestamps, cc):
    modified_timestamps = [ts.rsplit(':', 1)[0] for ts in timestamps]

    # Parse the modified timestamps
    parsed_dates = [parser.parse(ts) for ts in modified_timestamps]

    # Convert parsed dates to a pandas DataFrame
    data = {'Timestamp': parsed_dates}
    timestamps = pd.DataFrame(data)
    # Plot distribution for timestamps
    plt.figure(figsize=(30,25))
    plt.hist(timestamps, bins=30, color='blue', alpha=0.7)
    # plt.scatter(timestamps, [0.02] * len(timestamps), color='red', marker='o', alpha=0.6)  # Dots
    plt.xlabel('Timestamp')
    plt.ylabel('Frequency')
    plt.title('Distribution of Timestamps')
    plt.tight_layout()
    plt.savefig('/data/yellow/guacalytics/python_files/Analysis/timestamps.png')

    # Plot distribution for cyclomatic complexity
    plt.figure(figsize=(25,20))
    plt.hist(cc, bins=20, color='green', alpha=0.7)
    # plt.scatter(cc, [0.02] * len(cc), color='red', marker='o', alpha=0.6)  # Dots
    plt.xlabel('Cyclomatic Complexity')
    plt.ylabel('Frequency')
    plt.title('Distribution of Cyclomatic Complexity')
    plt.tight_layout()
    plt.savefig('/data/yellow/guacalytics/python_files/Analysis/cc.png')

if __name__ == "__main__":
    md_file = '/data/yellow/guacalytics/python_files/Analysis/radon_results.md'
    timestamp, cc = fetch_data_from_md(md_file)
    build_plots(timestamp, cc)
