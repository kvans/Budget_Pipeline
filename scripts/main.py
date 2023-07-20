from transactions import Transaction, Account
import json
import plaid
from plaid.api import plaid_api
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os
from plaid.model import item_get_request

db_host = os.environ.get('POSTGRES_HOST')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
port = os.environ.get('POSTGRES_PORT')
db = os.environ.get('POSTGRES_DB')

with open("config.json", 'r') as json_data:
    secrets = json.load(json_data)

configuration = plaid.Configuration(
    host=plaid.Environment.Production,
    api_key={
        'clientId': secrets['client_id'],
        'secret': secrets['secret_id'],
        
    }
)

##lazy way to do this but sort
lst_sql_execs_in_order = ['staging__transactions','staging__accounts','true_categories', 'true_transaction','v_true_staging_transactions']

def main():
    print("starting run")
    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    # Create a SQLAlchemy engine for easier insertion
    
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{port}/{db}")

    for banks, access_key in secrets['keys'].items():
        

        #too lazy to make this an upsert.
        #Should only be an issue if you have tens of thousands of transactions your pulling daily
        #This is not built for that kind of pull
        acc = Account(client, banks)
        acc.to_transformed_dataframe().to_sql('base_accounts', con=engine, if_exists='append', index=False)
        trans = Transaction(client, banks,60,access_key)
        trans.to_transformed_dataframe().to_sql('base_transactions', con=engine, if_exists='append', index=False)
        ##
        ##
        ## create a sql script
        ##
        ##
        with engine.begin() as connection:
            for script in lst_sql_execs_in_order:
                with open(f'{script}.sql', 'r') as file:  # Step 2: Read SQL file and execute statements
                    statements = file.read()
                    connection.execute(text(statements)
                    )
        engine.dispose()

    print('finished run')    




if __name__ == '__main__':
    main()