import json
import numpy as np
import matplotlib.pyplot as plt

# Load the JSON file containing directories, files, line counts, and MIME types
with open('errorfree.json', 'r') as json_file:
    data = json.load(json_file)

# Lists to store line counts and MIME types
line_counts = []
mime_types = []
# Dictionary to store the count of each MIME type
mime_type_counts = {}
# Function to recursively process nested JSON data
def process_data(data):
    for key, value in data.items():

        if "line_count" in list(value.keys()):
            # If the value is a dictionary, it represents a directory
# If the value is a list with two elements, it represents a file
            line_count = int(data[key]["line_count"])
            mime_type = data[key]["mime_type"]
            line_counts.append(line_count)
            mime_types.append(mime_type)
            if mime_type in mime_type_counts:
                mime_type_counts[mime_type] += 1
            else:
                mime_type_counts[mime_type] = 1
        else:
            process_data(value)

# Start processing the JSON data
process_data(data)

# Calculate the bell curve distribution for line counts
mean = np.mean(line_counts)
std_dev = np.std(line_counts)
min_count = min(line_counts)
max_count = max(line_counts)

# Generate histogram data for MIME types
unique_mime_types = list(mime_type_counts.keys())
counts = [mime_type_counts[mime_type] for mime_type in unique_mime_types]

# Create the bell curve distribution for line counts
plt.subplot(2, 1, 1)
plt.hist(line_counts, bins=20, density=True, alpha=0.6, color='b')
plt.title('Bell Curve Distribution of Line Counts')
plt.xlabel('Line Count')
plt.ylabel('Probability')
plt.grid(True)

# Overlay the bell curve on top
x = np.linspace(min_count, max_count, 100)
pdf = 1.0 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-(x - mean)**2 / (2 * std_dev**2))
plt.plot(x, pdf, color='r', linestyle='--', linewidth=2)

plt.xlim(left=min_count, right=20000)

# Create a histogram for MIME types
plt.subplot(2, 1, 2)
plt.bar(unique_mime_types, counts, alpha=0.6, color='g')
plt.title('Histogram of MIME Types')
plt.xlabel('MIME Type')
plt.xticks(rotation=90)
plt.ylabel('Count')
plt.grid(True)

for i, count in enumerate(counts):
    plt.text(i, count, str(count), ha='center', va='bottom')

plt.tight_layout()
plt.show()
