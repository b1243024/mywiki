import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("資料庫和 articles 表已建立（如果還沒存在）")
