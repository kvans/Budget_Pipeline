import plaid
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import datetime
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest

import json
from plaid.api import plaid_api
import numpy as np
import pandas as pd
import csv
with open("config.json", 'r') as json_data:
    secrets = json.load(json_data)

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': secrets['client_id'],
        'secret': secrets['secret_id'],
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


    
request = TransactionsSyncRequest(
    access_token=secrets['keys']['amex'],
)
response = client.transactions_sync(request)
transactions = response['added']
json_string = json.loads(json.dumps(response.to_dict(), default=str))
df = pd.json_normalize(json_string, record_path=['added'])

##Transactions in response can be thought of like a document. There are a certain number of transactions
#on one doc then you have to move to the next.
while (response['has_more']):
    request = TransactionsSyncRequest(
        access_token=secrets['keys']['amex'],
        cursor=response['next_cursor']
    )
    response = client.transactions_sync(request)
    transactions += response['added']
    json_string = json.loads(json.dumps(response.to_dict(), default=str))
    df = pd.concat([df,pd.json_normalize(json_string, record_path=['added'])])
df.to_csv('test.csv',index=False)
