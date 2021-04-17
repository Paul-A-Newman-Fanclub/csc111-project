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
from bigquery import user_input_query_helper
from build_graph import build_graph
from cycles import transaction_cycle
from high_balance import find_avg_balance, high_balance_transactions
from subnetworks import biggest_subnetwork, future_partners
from regression import balance_correlation_and_plot
from visualize_graph import plot_graph


# Prompt user for input, run a query on BigQuery, and write the results to csv files.
# If the query fails due to exceeding the quota, replace 
# 'credentials.json' with 'backup-credentials.json'
# user_input_query_helper('credentials.json')

# Create a graph of the ethereum network using the csv files available.
ethereum_graph = build_graph('balances.csv', 'transactions.csv')

# Visualize the graph
plot_graph(ethereum_graph)

# Run the linear regression and output the result.
r2, rmse = balance_correlation_and_plot(ethereum_graph)
print("Coefficient of determination (r^2): " + str(r2) + "\nRMSE: " + str(rmse) + "\n")

# Prompt the user if they are ready to run high_balance, run it if they are.
print("Enter 'y' when you wish to run the high_balance.py.")

user_input = input("Are you ready?: ")
if user_input.lower() == 'y':
    avg = find_avg_balance(ethereum_graph)
    prop = high_balance_transactions(ethereum_graph, avg)

    print("The proportion of transactions that a high balance account makes\n"
          + f"with other high balance accounts in this network is: {prop}")

# Prompt the user if they are ready to run subnetworks, run it if they are.
print("Enter 'y' when you wish to run the subnetworks.py.")

user_input = input("Are you ready?: ")
if user_input.lower() == 'y':
    subnet = biggest_subnetwork(ethereum_graph)
    future_partners(ethereum_graph, subnet)

# Prompt the user if they are ready to run cycles, run it if they are.
print("Enter 'y' when you wish to run the cycles.py.")

user_input = input("Are you ready?: ")
if user_input.lower() == 'y':
    transaction_cycle(ethereum_graph)
