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
# from Graph import Graph
# from Vertex import _Vertex

import csv
import networkx as nx
import math


def build_graph(accounts_file: str, transactions_file: str) -> nx.MultiDiGraph:
    """
    Build up and return a networkx Graph object from data provided in
    .csv file format.

    Specifically:
    Initialize the vertices of the graph to hold the address of the ethereum external
    accounts and their respective balances.

    Then, add edges between all accounts based on transactions that have occurred (must be
    a directed graph).
    """
    # Initialize an empty networkx graph.
    graph = nx.MultiDiGraph()

    # Begin adding all nodes (account/balance pairings as vertices to graph).
    # Each vertex will be initialize to hold the tuple (account address, Ether balance).
    vertex_dict = {}
    with open(accounts_file) as af:
        accounts = csv.reader(af)

        # Skip header
        next(accounts, None)

        # Can change this so that instead, the address is the only item in the node
        # then balance becomes attribute, e.g.
        # balance=ether_balance
        for account in accounts:
            # item = (account[1], account[0])
            item = account[1]
            value = int(account[0])

            # Determine what the node size should be, based on the balance in the account
            # the more ether the bigger the node.
            ether = value / 10**18
            if ether == 0:
                node_size = 1
            else:
                node_size = int(math.log(ether, 10)) + 1

            graph.add_node(item, balance=value, size=node_size)

            # Add the pairing to the dict to keep track of it.
            vertex_dict[account[1]] = account[0]

    # Add directed edges between nodes based on which addresses complete transactions
    # w/ one another. Edge will be directed going form vertex corresponding to
    # from_address to vertex corresponding to to_address in transaction record.
    with open(transactions_file) as tf:
        transactions = csv.reader(tf)

        # Skip header
        next(transactions, None)

        for transaction in transactions:
            from_addr = transaction[1]
            to_addr = transaction[2]
            value = transaction[3]

            # Convert the value of Wei into Ether
            # Wei is a smaller denomination of Ether, 1 Ether = 10^18 Wei.
            value = float(value) / (10 ** 18)

            # First check that both the to_ and from_ addresses are present in the
            # graph before trying to add an edge b/w them. - since datasets might not
            # be comprehensive or line up w/ each other.
            if from_addr in vertex_dict and to_addr in vertex_dict:
                # Add an edge between the two accounts based on the transaction.
                graph.add_edge((from_addr, vertex_dict[from_addr]), (to_addr, vertex_dict[to_addr]), weight=value)

    return graph


if __name__ == '__main__':
    # Run PythonTA
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['csv', 'networkx'],
        'allowed-io': ['load_review_graph'],
        'max-nested-blocks': 4
    })

    # Create the representation of the Ethereum blockchain network based on the
    # subset of data collected.
    #ethereum_graph = build_graph('ethereum_balances_data.csv', 'ethereum_transaction_data.csv')
