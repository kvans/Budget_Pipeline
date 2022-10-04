import plaid
from datetime import datetime, timedelta
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.api import plaid_api
import json
import numpy as np
import pandas as pd
import csv
with open("config.json", 'r') as json_data:
    secrets = json.load(json_data)

thirtyDaysAgo = datetime.now() - timedelta(30)

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

def RemoveOldRecords(df, daterange):
    df['date']= pd.to_datetime(df['date'])
    return df[df['date'] >= daterange]
    
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
    df = RemoveOldRecords(df, thirtyDaysAgo)
df.to_csv('test.csv',index=False)



class Account:
    def __init__(self, client):
        self.client = client

    def get_account_data(self):
        request = AccountsGetRequest(
            access_token=secrets['keys']['amex'],
        )
        return self.client.accounts_get(request)
    
    def to_csv(self):
        response = self.get_account_data()
        json_string = json.loads(json.dumps(response.to_dict(), default=str))
        df = pd.concat([df,pd.json_normalize(json_string, record_path=['accounts'])])
        df.to_csv('account.csv',index=False)
        
        
        
