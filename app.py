from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from script.symbols import Symbols
from script.db import users_collection
from script.fyers import Fyers
from fyres_data.instrument_types import InstrumentType
from fyres_data.orders import OrderStatus, OrderType, OrderSlides
app = Flask(__name__)
app.secret_key = 'intraday_trading'  # Replace with your secret key
bcrypt = Bcrypt(app)

fyers_data = {}
fyers_data["connected"] = False

@app.route('/', methods=['GET', 'POST'])
def home():
    """_summary_

    Returns:
        _type_: _description_
    """
    if session.get("username", None):
        fyers = Fyers(username=session["username"])

        if fyers.fyers_model():
            fyers_data["connected"] = True
            print("Connected")

        if not fyers_data["connected"]:
            fyers.gen_authcode()
            try:
                if request.method == 'POST' and request.form.get('auth_code'):
                    auth_code = request.form['auth_code']
                    fyers.generate_accesstoken(auth_code=auth_code)
                    flash(
                        f"Generated authorization code...{fyers.access_token}")
                    fyers_data["connected"] = True

            except Exception as ex:
                print(ex)

        if fyers_data["connected"]:
            fyers_data["order_book"] = fyers.order_book()
            fyers_data["positions"], fyers_data["overall"] = fyers.positions()

    return render_template('index.html', fyers_data=fyers_data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """_summary_

    Returns:
        _type_: _description_
    """
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
