from transactions import Transaction, Account
import json
import plaid
from plaid.api import plaid_api
from sqlalchemy import create_engine
import os

db_host = os.environ.get('POSTGRES_HOST')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
port = os.environ.get('POSTGRES_PORT')
db = os.environ.get('POSTGRES_DB')

with open("config.json", 'r') as json_data:
    secrets = json.load(json_data)

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': secrets['client_id'],
        'secret': secrets['secret_id'],
    }
)
# Create a SQLAlchemy engine for easier insertion
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{port}/{db}")


def main():
    print("starting run")
    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    
    for banks, access_key in secrets['keys'].items():
        #too lazy to make this an upsert.
        #Should only be an issue if you have tens of thousands of transactions your pulling daily
        #This is not built for that kind of pull
        acc = Account(client, banks)
        acc.to_transformed_dataframe().to_sql('base_accounts', con=engine, if_exists='append', index=False)
        trans = Transaction(client, banks,11,access_key)
        trans.to_transformed_dataframe().to_sql('base_transactions', con=engine, if_exists='append', index=False)

    print('finished run')    




if __name__ == '__main__':
    main()