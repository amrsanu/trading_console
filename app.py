from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from script.symbols import Symbols
from script.db import users_collection


app = Flask(__name__)
app.secret_key = 'intraday_trading'  # Replace with your secret key
bcrypt = Bcrypt(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    symbols = Symbols()
    nse_symbols = symbols.symbols()

    selected_stock = None
    if request.method == 'POST':
        selected_stock = request.form['selected_stock']
        # Process the selected stock as needed
        print(f'Selected Stock: {selected_stock}')

    return render_template('index.html', nse_symbols=nse_symbols, selected_stock=selected_stock)


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
