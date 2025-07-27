from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.config['DEBUG'] = True

# ===== 建立資料庫和資料表 =====
def init_db():
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
    print('資料表已建立')

# ===== 🔥 馬上執行建表（Render 會執行這行）=====
init_db()

# ===== 首頁 =====
@app.route('/')
def index():
    try:
        conn = sqlite3.connect('wiki.db')
        c = conn.cursor()
        c.execute('SELECT * FROM articles')
        articles = c.fetchall()
        conn.close()
        return render_template('index.html', articles=articles)
    except Exception as e:
        print(f'[INDEX ERROR] {e}')
        return 'Internal Server Error', 500

# 其他 routes（省略，與上次相同）

# ===== 啟動 Flask（本地測試時才用）=====
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
