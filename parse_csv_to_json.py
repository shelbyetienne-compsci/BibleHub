import csv
import json
from collections import defaultdict

csv_file_path = 't_kjv.csv'  # Path to your CSV file
json_file_path = 'kjv.json'  # Path where JSON will be saved

# Dictionary to store the data grouped by book and chapter
bible_data = defaultdict(lambda: defaultdict(list))

# Open the CSV file
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header row if there's one

    for row in csv_reader:
        id_field = row[0]
        b_field = int(row[1])  # Book number (can be used to determine the book name)
        c_field = int(row[2])  # Chapter number
        v_field = int(row[3])  # Verse number
        t_field = row[4]  # The text field

        # Use book number as key (e.g., Genesis is 1)
        book_number = b_field

        # Create the verse data as a dictionary
        verse_data = {
            "id": int(id_field),
            "b": b_field,
            "c": c_field,
            "v": v_field,
            "t": t_field
        }

        # Append the verse to the appropriate book and chapter
        bible_data[book_number][str(c_field)].append(verse_data)

# Save the data as JSON
with open(json_file_path, mode='w') as json_file:
    json.dump(bible_data, json_file, indent=4)

print(f"CSV data has been successfully grouped by chapters and saved to {json_file_path}")
