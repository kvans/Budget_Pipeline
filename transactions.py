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


 ###
 ### Pulls accounts associated to a bank/credit card company
 ###    
class Account:
    def __init__(self, client, companyToken):
        self.client = client
        self.companyToken = companyToken

    def get_account_data(self):
        request = AccountsGetRequest(
            access_token=secrets['keys'][self.companyToken],
        )
        return self.client.accounts_get(request)
    
    def to_csv(self):
        response = self.get_account_data()
        json_string = json.loads(json.dumps(response.to_dict(), default=str))
        df = pd.json_normalize(json_string, record_path=['accounts'])
        df.to_csv('account.csv',index=False)
        
        
 ###
 ### Pulls all transactions for a specific account
 ###       
class Transaction:
    def __init__(self, client, companyToken, dateRange, accountkey):
        self.client = client
        self.companyToken = companyToken
        self.dateRange = dateRange
        self.x_days_ago = datetime.now() - timedelta(self.dateRange)
        self.accountkey = accountkey

    

    def get_transaction_data(self):
        request = TransactionsSyncRequest(
            access_token=self.accountkey,
        )
        return self.client.transactions_sync(request)

    def loop_through_pages(self,response):

        json_string = json.loads(json.dumps(response.to_dict(), default=str))
        df = pd.json_normalize(json_string, record_path=['added'])

        while (response['has_more']):
            transactions = response['added']
            request = TransactionsSyncRequest(
                access_token=secrets['keys']['amex'],
                cursor=response['next_cursor']
            )
            response = self.client.transactions_sync(request)
            transactions += response['added']
            json_string = json.loads(json.dumps(response.to_dict(), default=str))
            df = pd.concat([df,pd.json_normalize(json_string, record_path=['added'])])

        return df
    
    def to_csv(self):
        response = self.get_transaction_data()
        finalListOfTransactions = self.loop_through_pages(response)
        finalListOfTransactions = self.RemoveOldRecords(finalListOfTransactions, self.x_days_ago)
        finalListOfTransactions.to_csv('transactions.csv',index=False)

    def RemoveOldRecords(self,df, dateRange):
        df['date']= pd.to_datetime(df['date'])
        return df[df['date'] >= dateRange]

