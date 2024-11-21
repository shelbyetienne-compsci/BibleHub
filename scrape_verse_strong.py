import csv
import sqlite3
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from strongs.bible_names import bible_books

# Connect to SQLite (creates a database file if it doesn't exist)
conn = sqlite3.connect('verse-strongs-kjv.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS verse_strongs (
    id INTEGER PRIMARY KEY,
    str_num INTEGER
)
''')

csv_file_path = 't_kjv.csv'  #

concords_data = defaultdict(lambda: defaultdict(list))

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    for row in csv_reader:
        verse_id = row[0]  # Verse ID
        book_name = bible_books[int(row[1])]  # Book Name (e.g., "1")
        chapter_number = int(row[2])  # Chapter Number
        verse_number = int(row[3])  # Verse Number

        scrape_url = f"https://biblehub.com/{book_name}/{chapter_number}-{verse_number}.htm"
        r = requests.get(scrape_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        str_list = soup.select('.str a')

        size = str_list.__len__()

        for i in range(size):
            print(i)


print(str_list[0].text.strip())
print(r.content[:100])