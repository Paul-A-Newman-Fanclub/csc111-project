"""
CSC111 Final Project: Reconstructing the Ethereum Network Using
Graph Data Structures in Python

General Information
------------------------------------------------------------------------------
This file was created for the purpose of applying concepts in learned in
CSC111 to the real world problem domain of cryptocurrency transactions.

Copyright Information
------------------------------------------------------------------------------
This file is Copyright of Tobey Brizuela, Daniel Lazaro, Matthew Parvaneh, and
Michael Umeh.
"""
from google.cloud import bigquery
import os
import csv

def user_input_query_helper():
    """
    Passes arguments to bigquery_helper according to user input.
    """
    # Default values (default strings used in the query)
    filter_values = ''  # No filtering
    transaction_limit = 'LIMIT 1000 '  # Limit to 1000 transactions
    sorting = 'ORDER BY block_timestamp DESC '  # Sort by time descending
    range = '1'  # Transactions occuring during the last day

    default = input('Would you like to customize your query? (Y/N, default N): ')
    while default.lower().strip() not in {'y', 'yes', 'n', 'no', ''}:
        print('Invalid input.')
        default = input('Would you like to customize your query? (Y/N, default N): ')
    if default.lower().strip() in {'n', 'no', ''}:
        print('\nQuerying using default parameters (see report for details).\n')
        _bigquery_helper(filter_values, transaction_limit, sorting, range)
    else:
        # Filter out transactions with value 0?
        filter_values_input = input(
            'Would you like to filter out transactions with value 0? ' 
            '(Y/N, default N): ')
        while filter_values_input.lower().strip() not in {'y', 'yes', 'n', 'no', ''}:
            print('Invalid input.')
            filter_values_input = input(
                'Would you like to filter out transactions with value 0? ' 
                '(Y/N, default N): ')
        if filter_values_input.lower().strip() in {'y', 'yes'}:
            filter_values = 'AND value > 0 '

        # Date range?
        # Note: higher values only make a difference when sorting by date ASC
        range_input = input(
            'How many days (in the past) of transactions would you like to query? ' 
            '(default 1, high values may lead to query failing): ')
        while not range_input.strip().isnumeric() or int(range_input) == 0:
            if range_input == '':
                range_input = '1'
                break
            print('Invalid input.')
            range_input = input(
                'How many days (in the past) of transactions would you like to query? ' 
                '(default 1, high values may lead to query failing): ')
        if range_input.strip() != '':
            range = range_input.strip()

        # Sorting?
        sorting_input = input(
            'How would you like the transaction times to be sorted? ' 
            '(ASC/DESC, default DESC): ')
        while sorting_input.strip().lower() not in {'ascending', 'descending', 
                                                    'asc', 'desc', 'a', 'd', ''}:
            print('Invalid input.')
            sorting_input = input(
                'How would you like the transactions to be sorted? ' 
                '(ASC/DESC, default DESC): ')
        if sorting_input.strip() in {'ascending', 'asc', 'a'}:
            sorting = 'ORDER BY block_timestamp ASC '
                    
        # Transaction limit = ?
        transaction_limit_input = input(
            'How many transactions would you like to limit the query to? ' 
            '(default 1000, higher limits not recommended): ')
        while not (transaction_limit_input.strip().isnumeric() or transaction_limit_input == ''):
            print('Invalid input.')
            transaction_limit_input = input(
                'How many transactions would you like to limit the query to? ' 
                '(default 1000, higher limits not recommended): ')
        if transaction_limit_input.strip() != '':
            transaction_limit = 'LIMIT ' + transaction_limit_input.strip() + ' '

        print('\nQuerying using user-specified parameters.\n')
        _bigquery_helper(filter_values, transaction_limit, sorting, range)
        

def _bigquery_helper(filter_values, transaction_limit, sorting, range):
    """
    Queries the Ethereum BigQuery dataset according to user's input.
    """
    print('Fetching the Ethereum transaction/balance data from Google BigQuery.')
    print('This may take a while...\n')
    # Initialize client (this will use the credentials in 'credentials.json' to authenticate)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
    client = bigquery.Client()

    # Perform the transactions query (query written in SQL)
    QUERY = ''.join([
        'SELECT nonce, from_address, to_address, value, block_timestamp ',
        'FROM `bigquery-public-data.crypto_ethereum.transactions` ',
        'WHERE DATE_ADD(CURRENT_DATE(), INTERVAL -', range, ' day) <= DATE(block_timestamp) ',
        filter_values,
        sorting,
        transaction_limit])
    query_job = client.query(QUERY)  # Make API request
    transactions = query_job.result()  # Wait for query to finish and assign the returned table 
    print('Transactions query successful. (1/2)\n')

    # Write results to 'transactions.csv' (file is placed in working directory)
    with open('transactions.csv', mode='w', newline='') as transactions_file:
        writer = csv.writer(transactions_file)
        # Write header row
        writer.writerow(['nonce', 'from_address', 'to_address', 'value'])
        # Write all transactions
        for transaction in transactions:
            writer.writerow([transaction.nonce, transaction.from_address, 
                            transaction.to_address, transaction.value])

    # Perform the balances query
    QUERY = ''.join([
        'SELECT eth_balance, address ',
        'FROM `bigquery-public-data.crypto_ethereum.balances` ',
        'WHERE address IN ( ',
            'SELECT from_address ',
            'FROM `bigquery-public-data.crypto_ethereum.transactions` ',
            'WHERE DATE_ADD(CURRENT_DATE(), INTERVAL -', range, ' day) <= DATE(block_timestamp) ',
            filter_values,
            sorting,
            transaction_limit,
        ') OR address IN ( ',
            'SELECT to_address ',
            'FROM `bigquery-public-data.crypto_ethereum.transactions` ',
            'WHERE DATE_ADD(CURRENT_DATE(), INTERVAL -', range, ' day) <= DATE(block_timestamp) ',
            filter_values,
            sorting,
            transaction_limit,
        ')'])
    query_job = client.query(QUERY)  # Make API request
    accounts = query_job.result()  # Wait for query to finish and assign the returned table 
    print('Balances query successful. (2/2)\n')

    # Write results to 'balances.csv'
    with open('balances.csv', mode='w', newline='') as transactions_file:
        writer = csv.writer(transactions_file)
        # Write header row
        writer.writerow(['eth_balance', 'address'])
        # Write all accounts/balances
        for account in accounts:
            writer.writerow([account.eth_balance, account.address])
    
    # The working directory should now contain the files used to build the transaction graph
    print('Successfully queried BigQuery for desired data.')
    print("The 'transactions.csv' and 'balances.csv' files should now be in the working directory.")
