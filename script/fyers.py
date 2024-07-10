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
        print("In generate_accesstoken()")
        self.appSession.set_token(auth_code)
        response = self.appSession.generate_token()

        try:
            self.access_token = response["access_token"]
            print("Generating authorization token : " + self.access_token)
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
        response = {
            "s": "ok",
            "code": 200,
            "message": "",
            "netPositions":
            [{
                "netQty": 1,
                "qty": 1,
                "avgPrice": 72256.0,
                "netAvg": 71856.0,
                "side": 1,
                "productType": "MARGIN",
                "realized_profit": 400.0,
                "unrealized_profit": 461.0,
                "pl": 861.0,
                "ltp": 72717.0,
                "buyQty": 2,
                "buyAvg": 72256.0,
                "buyVal": 144512.0,
                "sellQty": 1,
                "sellAvg": 72656.0,
                "sellVal": 72656.0,
                "slNo": 0,
                "fyToken": "1120200831217406",
                "crossCurrency": "N",
                "rbiRefRate": 1.0,
                "qtyMulti_com": 1.0,
                "segment": 20,
                "symbol": "MCX:SILVERMIC20AUGFUT",
                "id": "MCX:SILVERMIC20AUGFUT-MARGIN",
                "cfBuyQty": 0,
                "cfSellQty": 0,
                "dayBuyQty": 0,
                "daySellQty": 1,
                "exchange": 10,
            },
                {
                "netQty": -11,
                "qty": -1,
                "avgPrice": 72256.0,
                "netAvg": 71856.0,
                "side": 1,
                "productType": "MARGIN",
                "realized_profit": 400.0,
                "unrealized_profit": 461.0,
                "pl": 861.0,
                "ltp": 72717.0,
                "buyQty": 1,
                "buyAvg": 72256.0,
                "buyVal": 144512.0,
                "sellQty": 2,
                "sellAvg": 72656.0,
                "sellVal": 72656.0,
                "slNo": 0,
                "fyToken": "1120200831217406",
                "crossCurrency": "N",
                "rbiRefRate": 1.0,
                "qtyMulti_com": 1.0,
                "segment": 20,
                "symbol": "NSE:HDFCBANK-EQ",
                "id": "MCX:SILVERMIC20AUGFUT-MARGIN",
                "cfBuyQty": 0,
                "cfSellQty": 0,
                "dayBuyQty": 0,
                "daySellQty": 1,
                "exchange": 10,
            }],
            "overall":
            {
                "count_total": 1,
                "count_open": 1,
                "pl_total": 861.0,
                "pl_realized": 400.0,
                "pl_unrealized": 461.0
            }
        }
        if response["code"] == 200:
            return response["netPositions"], response["overall"]
        else:
            return None

    def place_order(self):
        """Fetches all the orders placed by the user across 
        all platforms and exchanges in the current trading day.

        Returns:
            dict: All the orders placed by the user
        """
        data = {
            "symbol": "NSE:IDEA-EQ",
            "qty": 1,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
            "orderTag": "tag1"
        }

        response = self.fyers.place_order(data=data)

        if response["code"] == 200:
            print(response)
            return response["orderBook"]
        else:
            return None

    def basket_orders(self):
        """Fetches all the orders placed by the user across 
        all platforms and exchanges in the current trading day.

        Returns:
            dict: All the orders placed by the user
        """
        data = [{
            "symbol": "NSE:SBIN-EQ",
            "qty": 1,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
        },
            {
            "symbol": "NSE:IDEA-EQ",
            "qty": 1,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
        }, {
            "symbol": "NSE:SBIN-EQ",
            "qty": 1,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
        },
            {
            "symbol": "NSE:IDEA-EQ",
            "qty": 1,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
        }]

        response = self.fyers.place_order(data=data)

        if response["code"] == 200:
            print(response)
            return response["orderBook"]
        else:
            return None

    def modify_pending_order(self):
        """Fetches all the orders placed by the user across 
        all platforms and exchanges in the current trading day.

        Returns:
            dict: All the orders placed by the user
        """


        orderId = "8102710298291"
        data = {
            "id": orderId,
            "type": 1,
            "limitPrice": 61049,
            "qty": 1
        }

        response = self.fyers.modify_order(data=data)
        if response["code"] == 200:
            print(response)
            return response["orderBook"]
        else:
            return None
