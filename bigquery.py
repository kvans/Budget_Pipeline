from google.cloud import bigquery
import google.cloud.bigquery as bq
import os
import json
import csv
with open("config.json", 'r') as json_data:
    secrets = json.load(json_data)



client = bigquery.Client.from_service_account_json(secrets['budgetapp_sa'])

table_id="budget-app-370619.source_transaction.transactions"
file_path='transactions.csv'


job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND  
)

with open(file_path, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)
