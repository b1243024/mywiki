from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.config['DEBUG'] = True  # 開啟除錯，讓錯誤顯示在 Render Logs

# ===== 自動建立資料庫和表格 =====
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

# ===== 首頁：列出所有文章 =====
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

# ===== 查看單篇文章 =====
@app.route('/article/<int:article_id>')
def article(article_id):
    try:
        conn = sqlite3.connect('wiki.db')
        c = conn.cursor()
        c.execute('SELECT * FROM articles WHERE id=?', (article_id,))
        article = c.fetchone()
        conn.close()
        if article:
            return render_template('article.html', article=article)
        else:
            return 'Article not found', 404
    except Exception as e:
        print(f'[ARTICLE ERROR] {e}')
        return 'Internal Server Error', 500

# ===== 新增文章 =====
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            conn = sqlite3.connect('wiki.db')
            c = conn.cursor()
            c.execute('INSERT INTO articles (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            print(f'[CREATE ERROR] {e}')
            return 'Internal Server Error', 500
    return render_template('create.html')

# ===== 啟動應用程式 =====
if __name__ == '__main__':
    init_db()  # 確保 wiki.db 存在
    app.run(host='0.0.0.0', port=5000)
