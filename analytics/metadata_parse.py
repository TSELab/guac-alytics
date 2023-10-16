import json
import numpy as np
from collections import defaultdict, Counter

# Load data from the 'data.json' file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# Create a dictionary to store JSON output
output_data = {}

# Initialize a dictionary to store MIME-type statistics for each tag
mime_type_stats = defaultdict(lambda: defaultdict(Counter))

# Iterate through the repositories
for repo_name, tags in data.items():
    # Initialize dictionaries for repo metrics
    repo_metrics = {}

    # Extract and process the data for each tag
    for tag_name, files in tags.items():
        line_count_list = [int(file_data["line_count"]) for file_data in files.values()]
        mean_line_count = np.mean(line_count_list)
        median_line_count = np.median(line_count_list)
        std_dev_line_count = np.std(line_count_list, ddof=0)  # Use ddof=0 for population standard deviation

        # Create a dictionary for metrics per tag
        tag_metrics = {
            "mean": mean_line_count,
            "median": median_line_count,
            "std_dev": std_dev_line_count
        }
        repo_metrics[tag_name] = tag_metrics

        # Collect MIME-type data per tag
        mime_counter = Counter(file_data["mime_type"] for file_data in files.values())
        mime_type_stats[repo_name][tag_name] = mime_counter

    # Add the repo metrics to the JSON output
    output_data[repo_name] = repo_metrics

# Output data to JSON
with open("output_data.json", "w") as json_file:
    json.dump(output_data, json_file, indent=2)

# Output MIME-type data to JSON for each tag
with open("mime_type_data.json", "w") as json_file:
    json.dump(mime_type_stats, json_file, indent=2)
