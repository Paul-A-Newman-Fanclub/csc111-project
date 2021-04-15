"""
Main file.
"""
from build_graph import build_graph
from visualize_graph import plot_graph
from bigquery import user_input_query_helper

# Prompt user for input, run a query on BigQuery, and write the results to csv files.
user_input_query_helper()

# Create a graph of the ethereum network using the csv files available.
ethereum_graph = build_graph('balances.csv', 'transactions.csv')

# Visualize the graph
plot_graph(ethereum_graph)

"""
Problems: 
    - need to update the size of the nodes based on the ether balance
    - Can color them based on the number of connections they have
    - ~~Make sure edges get drawn in~~ DONE
    - Hoverinfo for nodes should be the balance/account number
    - Hoverinfo for edges should be the value of the transaction.
"""
