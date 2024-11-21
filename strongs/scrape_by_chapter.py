import sqlite3
import sys

from scrape_concordance import scrape_concordance


def scrape_by_chapter(book_number, chapter_number):
    conn = sqlite3.connect('bible-kjv.db')  # Path to your database
    cursor = conn.cursor()

    query = """
    SELECT * FROM verses
    WHERE b = ?
    AND c = ?;
    """
    cursor.execute(query, (book_number, chapter_number))
    verses = cursor.fetchall()
    for id, b, c, v, t in verses:
        scrape_concordance(int(b), int(c), int(v))

    conn.close()


scrape_by_chapter(int(sys.argv[1]), int(sys.argv[2]))