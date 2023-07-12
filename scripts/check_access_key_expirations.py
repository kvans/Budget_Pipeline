import plaid
from plaid.api import plaid_api
import json

with open("C:/Users/nanu/Desktop/Dev/budgetapp/Budget_Pipeline/config.json", 'r') as json_data:
    secrets = json.load(json_data)

# Initialize Plaid client
configuration = plaid.Configuration(
    host=plaid.Environment.Production,
    api_key={
        'clientId': secrets['client_id'],
        'secret': secrets['secret_id'],
        
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Retrieve access token and expiration date
#access_token =  # Replace with your actual access token
response = client.Item.get(access_token)
expiration_date = response['item']['access_token_expiration_date']

# Print the expiration date
print("API token expiration date:", expiration_date)