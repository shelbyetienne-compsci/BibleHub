import re
import sqlite3

import requests
from bs4 import BeautifulSoup

from bible_names import bible_books


def scrape_concordance(book_number, chapter_number, verse_number):
    conn = sqlite3.connect('concordance.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS concordance (
        str_num INTEGER PRIMARY KEY,
        word TEXT,  -- words
        heb_greek TEXT, -- hebrew or greek
        translit TEXT,  -- english translation of greek or hebrew
        speech TEXT, -- part of speech in English language
        str_words TEXT
    )
    ''')

    scrape_url = f"https://biblehub.com/{bible_books[book_number - 1]}/{chapter_number}-{verse_number}.htm"
    r = requests.get(scrape_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    word_list = soup.select('.word')
    heb_list = soup.select('.heb')
    grk_list = soup.select('.grk')
    translit_list = soup.select('.translit')
    parse_list = soup.select('.parse')
    str_list = soup.select('.str a')
    str2_list = soup.select('.str2')

    size = word_list.__len__()


    for i in range(size):
        print(re.search(r'\d+', str_list[i].text.strip()).group())
        heb_greek = heb_list[i].text.strip() if book_number <= 39 else grk_list[i].text.strip()
        strongs_num = re.search(r'\d+', str_list[i].text.strip())
        cursor.execute('''
                INSERT OR IGNORE INTO concordance (str_num, word, heb_greek, translit, speech, str_words)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
            int(strongs_num.group()),
            word_list[i].text.strip(),
            heb_greek,
            translit_list[i].text.strip(),
            parse_list[i].text.strip(),
            str2_list[i].text.strip()
        ))
        # Update db with last verse scraped
    print(f"{book_number} {chapter_number} {verse_number}")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import sys
    book_number = int(sys.argv[1])  # First argument
    chapter_number = int(sys.argv[2])  # Second argument
    verse_number = int(sys.argv[3])
    scrape_concordance(book_number, chapter_number, verse_number)