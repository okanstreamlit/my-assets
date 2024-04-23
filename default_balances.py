stock_balance = {
        'tabgd': 148 + 159,
        'orge': 208,
        'kmpur': 214,
        'odine': 39
    }

currency_balance = {
        'usd' : 420.94,
        'alt' : 3.69
    }

bank_balance = 283.02

import joblib

joblib.dump(stock_balance, "stock_balance.pkl")
joblib.dump(currency_balance, "currency_balance.pkl")
joblib.dump(bank_balance, "bank_balance.pkl")

