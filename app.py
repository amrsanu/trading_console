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

_fyers = None
_fyers_data = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    """Home route that handles authentication and data retrieval."""
    global _fyers, _fyers_data
    # Initialize fyers_data dictionary if not already present
    if 'connected' not in session:
        session['connected'] = False

    connected = session['connected']

    if session.get("username"):
        if _fyers is None:
            print("Creating new account...")
            _fyers = Fyers(username=session["username"])

        try:
            if request.method == 'POST' and 'auth_code' in request.form:
                auth_code = request.form['auth_code']
                _fyers.generate_accesstoken(auth_code=auth_code)
                connected = True
                session['connected'] = connected

        except Exception as ex:
            print("Error in authentication:", ex)
        else:
            if _fyers.fyers_model():
                print("Authentication successfull...")
            else:
                connected = False
                session['connected'] = connected

        if not connected:
            _fyers.gen_authcode()

        if connected:
            try:
                response = _fyers.fyers.orderbook()
                if response["code"] == 200:
                    _fyers_data["order_book"] = response["orderBook"]
                else:
                    _fyers_data["order_book"] = []

                response = _fyers.fyers.positions()
                if response["code"] == 200:
                    _fyers_data["positions"] = response["netPositions"]
                    _fyers_data["overall"] = response["overall"]
                else:
                    _fyers_data["positions"], _fyers_data["overall"] = [], []

                # Return dummy data
                _fyers_data["positions"], _fyers_data["overall"] = _fyers.positions()

            except Exception as ex:
                print("Error in retrieving data:", ex)
    else:
        return redirect(url_for('login'))
    print(_fyers_data)
    return render_template('index.html', fyers_data=_fyers_data, connected=connected)


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
