import plaid
from datetime import datetime, timedelta
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.accounts_get_request import AccountsGetRequest
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

class Account:
    def __init__(self, client, companyToken):
        self.client = client
        self.companyToken = companyToken

    def get_account_data(self):
        request = AccountsGetRequest(
            access_token=secrets['keys']['amex'],
        )
        return self.client.accounts_get(request)
    
    def to_csv(self):
        response = self.get_account_data()
        json_string = json.loads(json.dumps(response.to_dict(), default=str))
        df = pd.json_normalize(json_string, record_path=['accounts'])
        df.to_csv('account.csv',index=False)
        
        
        
class Transaction:
    def __init__(self, client, companyToken, dateRange):
        self.client = client
        self.companyToken = companyToken
        self.dateRange = dateRange
        self.thirtyDaysAgo = datetime.now() - timedelta(30)

    

    def get_transaction_data(self):
        request = TransactionsSyncRequest(
            access_token=secrets['keys']['amex'],
        )
        return client.transactions_sync(request)

    def loop_through_pages(self,response):

        json_string = json.loads(json.dumps(response.to_dict(), default=str))
        df = pd.json_normalize(json_string, record_path=['added'])

        while (response['has_more']):
            transactions = response['added']
            request = TransactionsSyncRequest(
                access_token=secrets['keys']['amex'],
                cursor=response['next_cursor']
            )
            response = client.transactions_sync(request)
            transactions += response['added']
            json_string = json.loads(json.dumps(response.to_dict(), default=str))
            df = pd.concat([df,pd.json_normalize(json_string, record_path=['added'])])

        return df
    
    def to_csv(self):
        response = self.get_transaction_data()
        finalListOfTransactions = self.loop_through_pages(response)
        finalListOfTransactions = self.RemoveOldRecords(finalListOfTransactions, thirtyDaysAgo)
        finalListOfTransactions.to_csv('transactions.csv',index=False)

    def RemoveOldRecords(self,df, dateRange):
        df['date']= pd.to_datetime(df['date'])
        return df[df['date'] >= dateRange]

acc = Account(client, 'amex')
acc.to_csv()

trans = Transaction(client, 'amex',30)
trans.to_csv()