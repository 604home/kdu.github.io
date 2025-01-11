from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 初始化SQLite数据库
def init_db():
    conn = sqlite3.connect('search.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS documents (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     description TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()

# 插入一些示例数据
def insert_sample_data():
    conn = sqlite3.connect('search.db')
    c = conn.cursor()
    sample_data = [
        ('兆度搜索引擎介绍', '这是一个由我们团队开发的简单搜索引擎...'),
        ('如何使用兆度搜索引擎', '使用兆度搜索引擎非常简单，只需在搜索框中输入关键词...'),
        ('兆度搜索引擎的优势', '兆度搜索引擎速度快，准确率高，适合各种用户需求...')
    ]
    c.executemany("INSERT INTO documents (title, description) VALUES (?, ?)", sample_data)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    conn = sqlite3.connect('search.db')
    c = conn.cursor()
    c.execute("SELECT title, description FROM documents WHERE lower(title) LIKE ? OR lower(description) LIKE ?",
              ('%' + query + '%', '%' + query + '%'))
    results = c.fetchall()
    conn.close()

    return jsonify([{'title': row[0], 'description': row[1]} for row in results])

if __name__ == '__main__':
    init_db()
    insert_sample_data()
    app.run(debug=True)