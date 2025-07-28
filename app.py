from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_NAME = 'wiki.db'

# 初始化資料庫
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
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
        print("[INFO] 資料庫已建立")

# 首頁：顯示文章列表
@app.route('/')
def index():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, title FROM articles')
        articles = c.fetchall()
        conn.close()
        return render_template('index.html', articles=articles)
    except Exception as e:
        return f"<h1>首頁錯誤：</h1><p>{e}</p>", 500

# 查看單篇文章
@app.route('/article/<int:article_id>')
def view_article(article_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT title, content FROM articles WHERE id = ?', (article_id,))
        article = c.fetchone()
        conn.close()
        if article:
            return render_template('article.html', title=article[0], content=article[1])
        else:
            return "<h1>找不到文章</h1>", 404
    except Exception as e:
        return f"<h1>查看文章錯誤：</h1><p>{e}</p>", 500

# 新增文章
@app.route('/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('INSERT INTO articles (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            return f"<h1>新增文章錯誤：</h1><p>{e}</p>", 500
    return render_template('new.html')

# 啟動
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
