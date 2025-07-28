from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# 初始化資料庫
def init_db():
    if not os.path.exists('wiki.db'):
        conn = sqlite3.connect('wiki.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('wiki.db')
    c = conn.cursor()
    c.execute('SELECT id, title FROM articles')
    rows = c.fetchall()
    conn.close()
    return render_template('index.html', articles=rows)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('wiki.db')
        c = conn.cursor()
        c.execute('INSERT INTO articles (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/article/<int:article_id>')
def article(article_id):
    conn = sqlite3.connect('wiki.db')
    c = conn.cursor()
    c.execute('SELECT title, content FROM articles WHERE id = ?', (article_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return render_template('article.html', title=result[0], content=result[1])
    else:
        return "文章不存在", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
