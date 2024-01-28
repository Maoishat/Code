from flask import Flask, render_template

app = Flask(__name__)

# 运行代码后访问 http://127.0.0.1:5000/login
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()

