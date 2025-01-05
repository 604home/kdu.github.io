from flask import Flask, request, render_template_string

app = Flask(__name__)

# 模拟的数据集
data = [
    "兆度只有3个员工",
    "兆度专注于各种科技领域",
    "兆度的总部位于武汉",
    "兆度致力于开发先进的技术解决方案"
]

@app.route('/')
def index():
    return render_template_string(open('kd.html').read())

@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = [item for item in data if query.lower() in item.lower()]
    return render_template_string('''
        <html>
            <head>
                <title>搜索结果</title>
                <meta charset="UTF-8"></meta>
            </head>
            <body>
                <h1>搜索结果</h1>
                <ul>
                    {% for result in results %}
                        <li>{{ result }}</li>
                    {% else %}
                        <li>没有找到相关结果</li>
                    {% endfor %}
                </ul>
                <a href="/">返回首页</a>
            </body>
        </html>
    ''', results=results)

if __name__ == '__main__':
    app.run(debug=True)