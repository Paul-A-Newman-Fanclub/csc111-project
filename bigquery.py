"""
CSC111 Final Project: ...
"""
from google.cloud import bigquery
import os
import csv

def bigquery_helper():
    """
    Queries the Ethereum BigQuery dataset according to user's input.
    """
    print('Fetching the most recent Ethereum transaction/balance data from Google BigQuery.')
    print('This may take a while...')
    # Initialize client (this will use the credentials in 'credentials.json' to authenticate)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
    client = bigquery.Client()

    # Perform the transactions query (query written in SQL)
    QUERY = (
        'SELECT nonce, from_address, to_address, value, gas, gas_price, receipt_status, block_timestamp '
        'FROM `bigquery-public-data.crypto_ethereum.transactions` '
        'WHERE DATE_ADD(CURRENT_DATE(), INTERVAL -1 day) <= DATE(block_timestamp) '
        'ORDER BY block_timestamp DESC '
        'LIMIT 1000')
    query_job = client.query(QUERY)  # Make API request
    transactions = query_job.result()  # Wait for query to finish and assign the returned table 

    # Write results to 'transactions.csv' (file is placed in working directory)
    with open('transactions.csv', mode='w', newline='') as transactions_file:
        writer = csv.writer(transactions_file)
        # Write header row
        writer.writerow(['nonce', 'from_address', 
                        'to_address', 'value', 
                        'gas', 'gas_price', 
                        'receipt_status', 'block_timestamp'])
        # Write all transactions
        for transaction in transactions:
            writer.writerow([transaction.nonce, transaction.from_address, 
                            transaction.to_address, transaction.value, 
                            transaction.gas, transaction.gas_price, 
                            transaction.receipt_status, transaction.block_timestamp])

    # Perform the balances query
    QUERY = (
        'SELECT eth_balance, address '
        'FROM `bigquery-public-data.crypto_ethereum.balances` '
        'WHERE address IN ( '
            'SELECT from_address '
            'FROM `bigquery-public-data.crypto_ethereum.transactions` '
            'WHERE DATE_ADD(CURRENT_DATE(), INTERVAL -1 day) <= DATE(block_timestamp) '
            'ORDER BY block_timestamp DESC '
            'LIMIT 1000 '
        ') OR address IN ( '
            'SELECT to_address '
            'FROM `bigquery-public-data.crypto_ethereum.transactions` '
            'WHERE DATE_ADD(CURRENT_DATE(), INTERVAL -1 day) <= DATE(block_timestamp) '
            'ORDER BY block_timestamp DESC '
            'LIMIT 1000 '
        ')')
    query_job = client.query(QUERY)  # Make API request
    accounts = query_job.result()  # Wait for query to finish and assign the returned table 

    # Write results to 'balances.csv'
    with open('balances.csv', mode='w', newline='') as transactions_file:
        writer = csv.writer(transactions_file)
        # Write header row
        writer.writerow(['eth_balance', 'address'])
        # Write all accounts/balances
        for account in accounts:
            writer.writerow([account.eth_balance, account.address])
    
    # The working directory should now contain the files used to build the transaction graph
    print('Successfully queried BigQuery.')
    print("The 'transactions.csv' and 'balances.csv' files should now be in the working directory.")
