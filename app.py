import sqlite3
from flask import Flask, request, render_template, redirect, url_for, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
DATABASE = 'path_to_your_database.db'  # 替换为你的数据库文件路径

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM Food")
    foods = cur.fetchall()
    return render_template('index.html', foods=foods)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, hashed_password))
        db.commit()

        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = get_db().cursor()
        cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[2], password):
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
