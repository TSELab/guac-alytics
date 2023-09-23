import csv
import threading
import random
import os

def read_csv_into_set(filename, target_set):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                target_set.add(row[0])

def find_common_entries(file1, file2, file3, output_file):
    list1 = set()
    list2 = set()
    list3 = set()

    thread1 = threading.Thread(target=read_csv_into_set, args=(file1, list1))
    thread2 = threading.Thread(target=read_csv_into_set, args=(file2, list2))
    thread3 = threading.Thread(target=read_csv_into_set, args=(file3, list3))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    common_entries = list1.intersection(list2, list3)
    thousand_entries = random.sample(common_entries, 1000)

    with open(output_file, 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        for entry in thousand_entries:
            writer.writerow([entry])

if __name__ == "__main__":
	current_dir = os.getcwd()
	files = ['publish_names.csv', 'bi_source_names.csv', 'upstream_names.csv']
	output_file = 'common_entries.csv'
	for (i, file) in enumerate(files):
	  files[i] = os.path.join(current_dir, 'data/' + file)

	find_common_entries(files[0], files[1], files[2], output_file)
