import csv
import sqlite3
from collections import defaultdict

# Connect to SQLite (creates a database file if it doesn't exist)
conn = sqlite3.connect('bible-kjv.db')
cursor = conn.cursor()

# Create tables for books, chapters, and verses
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY,
    b TEXT,  -- Book
    c INTEGER,  -- Chapter number
    v INTEGER,  -- Verse number (used as 0 for the chapter itself)
    t TEXT  -- Chapter text (optional, could be null)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS verses (
    id INTEGER PRIMARY KEY,
    b TEXT,  -- Book
    c INTEGER,  -- Chapter number
    v INTEGER,  -- Verse number
    t TEXT  -- Verse text
)
''')
csv_file_path = 't_kjv.csv'  #
chapters_data = defaultdict(lambda: defaultdict(list))
# Open and parse the CSV file
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    # Use defaultdict to organize data by book and chapter


    for row in csv_reader:
        verse_id = row[0]  # Verse ID
        book_name = int(row[1])  # Book Name (e.g., "1")
        chapter_number = int(row[2])  # Chapter Number
        verse_number = int(row[3])  # Verse Number
        verse_text = row[4]  # Verse Text

        # Organize verses by book and chapter
        chapters_data[book_name][chapter_number].append({
            'verse_id': verse_id,
            'verse_number': verse_number,
            'verse_text': verse_text
        })

# Insert the books, chapters, and verses into the database
for book_name, chapters in chapters_data.items():
    # Insert book
    cursor.execute('INSERT OR IGNORE INTO books (name) VALUES (?)', (book_name,))
    cursor.execute('SELECT id FROM books WHERE name = ?', (book_name,))
    book_id = cursor.fetchone()[0]

    for chapter_number, verses in chapters.items():
        # Insert chapter (here we set `v = 0` because it's a chapter and not a specific verse)
        cursor.execute('''
        INSERT INTO chapters (b, c, v, t) 
        VALUES (?, ?, ?, ?)
        ''', (book_name, chapter_number, 0, f"Chapter {chapter_number} of {book_name}"))
        cursor.execute('SELECT id FROM chapters WHERE b = ? AND c = ? AND v = 0', (book_name, chapter_number))
        chapter_id = cursor.fetchone()[0]

        for verse in verses:
            # Insert verse
            cursor.execute('''
            INSERT INTO verses (b, c, v, t) 
            VALUES (?, ?, ?, ?)
            ''', (book_name, chapter_number, verse['verse_number'], verse['verse_text']))

# Commit changes and close connection
conn.commit()
conn.close()

print("CSV data has been imported into SQLite, organized by chapters and verses")
