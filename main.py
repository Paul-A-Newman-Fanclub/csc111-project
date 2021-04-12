"""
Main file.
"""
from build_graph import build_graph
from visualize_graph import plot_graph

# Create a graph of the ethereum network using the csv files available.
ethereum_graph = build_graph('ethereum_balances_data.csv', 'ethereum_transaction_data.csv')

# Visualize the graph
plot_graph(ethereum_graph)

"""
Problems: 
    - need to update the size of the nodes based on the ether balance
    - Can color them based on the number of connections they have
    - Make sure edges get drawn in
    - Hoverinfo for nodes should be the balance/account number
    - Hoverinfo for edges should be the value of the transaction.
"""
