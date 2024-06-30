import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from pymongo.server_api import ServerApi


app = Flask(__name__)
app.secret_key = 'intraday_trading'  # Replace with your secret key
bcrypt = Bcrypt(app)

user = urllib.parse.quote_plus("amrsanubtc")
password = urllib.parse.quote_plus("kite@123")
uri = f"mongodb+srv://{user}:{password}@kite-db.jtrmqlf.mongodb.net/?appName=kite-db"

# Replace the URI with your MongoDB deployment's connection string.
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['kite']
users_collection = db['kite-user']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        if users_collection.find_one({'username': username}):
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        users_collection.insert_one(
            {'username': username, 'password': hashed_password})
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have successfully logged out!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
