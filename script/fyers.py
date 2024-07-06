"""_summary_
"""
from fyers_apiv3 import fyersModel
import webbrowser
from script.db import users_collection
# Replace these values with your actual API credentials


class Fyers:
    def __init__(self, username):
        """Construct a new instance of the Fyers class"""
        self.user = users_collection.find_one({'username': username})
        self.id = self.user['fyers_id']
        self.client_id = self.user['fyers_client_id']
        self.secret_key = self.user['fyers_client_secret']
        self.redirect_uri = self.user['fyers_redirect_uri']
        self.access_token = self.user['access_token']
        self.response_type = "code"
        self.state = "sample_state"
        self.grant_type = "authorization_code"
        self.appSession = None
        self.fyers = None

    def gen_authcode(self):
        """Generate authorization code
        """
        self.appSession = fyersModel.SessionModel(client_id=self.client_id, redirect_uri=self.redirect_uri,
                                                  response_type=self.response_type, state=self.state, secret_key=self.secret_key, grant_type=self.grant_type)
        generate_token_url = self.appSession.generate_authcode()
        webbrowser.open(generate_token_url, new=1)

    def generate_accesstoken(self, auth_code):
        """Generate authorization token

        Args:
            auth_code (str): authorization code
        """

        self.appSession.set_token(auth_code)
        response = self.appSession.generate_token()

        try:
            self.access_token = response["access_token"]
            users_collection.update_one(
                {"username": self.user["username"]},
                {"$set": {"access_token": self.access_token}},
                upsert=True
            )
        except Exception as e:
            print(e, response)

    def fyers_model(self):
        """Get the model associated with this authentication.
        """
        self.fyers = fyersModel.FyersModel(
            token=self.access_token, is_async=False,
            client_id=self.client_id)
        response = self.fyers.orderbook()
        if response["code"] == 200:
            return True
        else:
            return False

    def order_book(self):
        """Fetches all the orders placed by the user across 
        all platforms and exchanges in the current trading day.

        Returns:
            dict: All the orders placed by the user
        """
        response = self.fyers.orderbook()
        if response["code"] == 200:
            print(response)
            return response["orderBook"]
        else:
            return None

    def positions(self):
        """Fetches all the orders placed by the user across 
        all platforms and exchanges in the current trading day.

        Returns:
            dict: All the orders placed by the user
        """
        response = self.fyers.positions()
        if response["code"] == 200:
            print(response)
            return response["netPositions"], response["overall"]
        else:
            return None
