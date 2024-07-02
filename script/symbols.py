import pandas as pd


class Symbols:
    """_summary_
    """

    def __init__(self):
        """_summary_
        """
        self.url = 'https://public.fyers.in/sym_details/NSE_CM.csv'
        self.headers = ["Fytoken", "Symbol Details", "Exchange Instrument type", "Minimum lot size", "Tick size", "ISIN", "Trading Session", "Last update date", "Expiry date", "Symbol ticker", "Exchange",
                        "Segment", "Scrip code", "Underlying symbol", "Underlying scrip code", "Strike price", "Option type", "Underlying FyToken", "Reserved column1", "Reserved column2", "Reserved column3"]

    def symbols(self):
        """_summary_
        """
        self.symbols_df = pd.read_csv(self.url, names=self.headers)
        return self.symbols_df['Symbol ticker'].str.cat(self.symbols_df['Symbol Details'], sep=" : ")
