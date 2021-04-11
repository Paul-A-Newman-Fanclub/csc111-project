"""
CSC111 Final Project: main.py file (see instructions in writeup for details)
"""
from google.cloud import bigquery
import os

def bigquery_helper():
    """
    Queries the Ethereum BigQuery dataset according to user's input.
    """
    # TODO: Implement this function (the code below is only sample code)
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(row.name)


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
    bigquery_helper()
