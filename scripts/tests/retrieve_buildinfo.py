import os
import csv
import time
import shutil

def create_set(filename):
    target_set = set()

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            target_set.add(row[0])
    return target_set

def retrieve_data(directory, filename):
    starting_dir = os.getcwd()
    sample_dir = "Sample_Data"
    packages = create_set(filename)
    count = 0
    os.makedirs(os.path.join(starting_dir, sample_dir), exist_ok=True)
    #print(os.path.join(starting_dir, sample_dir))
    print(f"Searching through '{directory}' and filling '{sample_dir}':")

    for dirpath, dirnames, filenames in os.walk(starting_dir + directory):
        if count >= 1000:
          print('Sample data allocation successful')
          break
        for filename in filenames:
            if not filename.endswith('buildinfo'):
                continue
            with open(os.path.join(dirpath, filename), 'r') as file:
                source_name = 0
                for line in file:

                  if 'Source: ' in line:
                    line = line.rstrip('\n')
                    source_name = line.split()[1]

                    if source_name and source_name in packages:
                      packages.remove(source_name)
                      count += 1
                      current_dir = os.path.join(dirpath, filename)
                      new_dir = os.path.join(starting_dir, current_dir.replace(starting_dir + directory, sample_dir))
                      #print(current_dir)
                      #print(new_dir)
                      os.makedirs(new_dir, exist_ok=True)
                      shutil.copy(current_dir , new_dir)
                      print(f"count: {count}", end='\r')
                    break
    print("\nData allocation complete")
if __name__ == "__main__":
    location = os.getcwd()
    file = 'common_entries.csv'
    directory = '/buildinfo_data'
    retrieve_data(directory, file)
