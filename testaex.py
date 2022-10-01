from email.policy import default
import plaid
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import datetime
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
import requests

import json
from plaid.api import plaid_api
import numpy as np
import pandas as pd

# Available environments are
# 'Production'
# 'Development'
# 'Sandbox'
configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': '',
        'secret': '',
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

import plaid
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest

request = TransactionsGetRequest(
    access_token='',
    start_date=datetime.strptime('2022-09-01', '%Y-%m-%d').date(),
    end_date=datetime.strptime('2022-09-19', '%Y-%m-%d').date(),
)
response = client.transactions_get(request)
transactions = response['transactions']



json_string = json.loads(json.dumps(response.to_dict(), default=str))
df = pd.json_normalize(json_string, record_path=['accounts'])
df.to_csv('test.txt')