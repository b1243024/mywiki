
from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)
DB_PATH = 'wiki.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT, content TEXT)')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, title FROM articles')
    articles = c.fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

@app.route('/article/<int:id>')
def article(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT title, content FROM articles WHERE id=?', (id,))
    article = c.fetchone()
    conn.close()
    return render_template('article.html', article=article, id=id)

@app.route('/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO articles (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new_article.html')

if __name__ == '__main__':
    init_db()
    app.run()
