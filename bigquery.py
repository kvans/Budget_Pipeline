from google.cloud import bigquery
import google.cloud.bigquery as bq
import os
import json
import csv
with open("config.json", 'r') as json_data:
    secrets = json.load(json_data)



#table_id="budget-app-370619.source_transaction.transactions"
#file_path='transactions.csv'
#'budgetapp_sa'

class importBigquery:
    def __init__(self, app, table, file):
        self.app = app
        self.table = table
        self.file = file
        client = bigquery.Client.from_service_account_json(secrets[self.app])
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV, 
            skip_leading_rows=1, 
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND  
        )
        with open(self.file, "rb") as source_file:
            job = client.load_table_from_file(source_file, self.table, job_config=job_config)
