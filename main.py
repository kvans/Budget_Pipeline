from transactions import Transaction, Account
from bigquery import importBigquery
import bigquery
import json
import numpy as np
import pandas as pd
import csv
import plaid
from plaid.api import plaid_api
with open("config.json", 'r') as json_data:
    secrets = json.load(json_data)

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': secrets['client_id'],
        'secret': secrets['secret_id'],
    }
)



def main():
    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    
    acc = Account(client, 'amex')
    acc.to_csv()
    trans = Transaction(client, 'amex',30,secrets['keys']['amex'])
    trans.to_csv()

    tobq = importBigquery('budgetapp_sa',secrets['bqdataset'],'transactions.csv')

if __name__ == '__main__':
    main()