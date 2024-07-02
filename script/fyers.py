"""_summary_
"""
from fyers_apiv3 import fyersModel
import webbrowser
from db import users_collection
# Replace these values with your actual API credentials


class Fyers:
    def __init__(self, username):
        """Construct a new instance of the Fyers class"""
        self.user = users_collection.find_one({'username': username})
        self.id = self.user['fyers_id']
        self.client_id = self.user['fyers_client_id']
        self.secret_key = self.user['fyers_client_secret']
        self.redirect_uri = self.user['fyers_redirect_uri']
        self.response_type = "code"
        self.state = "sample_state"
        self.grant_type = "authorization_code"
        self.appSession = None
        self.access_token = None
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
        auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTk4NDcwODcsImV4cCI6MTcxOTg3NzA4NywibmJmIjoxNzE5ODQ2NDg3LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJZUjE0ODg4Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiNGUxZTIyM2ZkYWRmNWJhNzQzNTFkMGRiMjU1NjhiMTQ4OTViNzAzZGZjYjRhMjgwOWMzNzA3ZTUiLCJub25jZSI6IiIsImFwcF9pZCI6IlhHTEVQWk04VUUiLCJ1dWlkIjoiNmQxODYyZjM2NzViNGQyMDljMDY5YjI4MWU1MmQ2NmUiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.zdQeT-sjrYI2Ep4Q96RJYxbrFUXygNz-EHPfJhQhBnw"

        self.appSession.set_token(auth_code)
        response = self.appSession.generate_token()

        try:
            self.access_token = response["access_token"]
        except Exception as e:
            print(e, response)

    def fyers_model(self):
        """Get the model associated with this authentication.
        """
        self.fyers = fyersModel.FyersModel(
            token=self.access_token, is_async=False, client_id=self.client_id, log_path="fyers_api.log")
