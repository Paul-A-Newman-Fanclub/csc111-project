"""
CSC111 Final Project: Reconstructing the Ethereum Network Using
Graph Data Structures in Python

General Information
------------------------------------------------------------------------------
This file was created for the purpose of applying concepts in learned in
CSC111 to the real world problem domain of cryptocurrency transactions.

Module Info: high_balance.py

This file contains code which intends to find all accounts in the
network that have high balances, and then determine if they tend to make
transactions with other high balance accounts more often.

Copyright Information
------------------------------------------------------------------------------
This file is Copyright of Tobey Brizuela, Daniel Lazaro, Matthew Parvaneh, and
Michael Umeh.
"""
import networkx as nx


def find_avg_balance(graph: nx.MultiDiGraph) -> float:
    """
    Find the average balance of Ether across all accounts
    in this subset of the entire network.

    Preconditions:
        - list(graph.nodes) != []
    """
    balances = []
    for node in graph.nodes():
        # Recall that some accounts take part in transactions
        # but have no balance; this check filters them out.
        if graph.nodes[node] != {}:
            balance = graph.nodes[node]['balance']
            balances.append(balance)

    # Calculate and return the average ether balance.
    return sum(balances) / len(balances)


def high_balance_transactions(graph: nx.MultiDiGraph, avg_balance: float) -> float:
    """
    Return the average proportion of transactions that a high
    balance account engages in with other high balance accounts, relative
    to all of the transactions it engages in, in general.

    All transactions will be counted for each account, both those that were
    sent out by this account, and those that were received by this account
    (so both successor vertices and predecessor vertices are counted).

    Preconditions:
        - list(graph.nodes) != []
        - avg_balance >= 0
    """
    # First, find all high balance accounts in the overall graph.
    all_accounts = list(graph.nodes)
    accounts = find_high_balance_accounts(graph, all_accounts, avg_balance)

    # Accumulator to hold each proportion across all high balance accounts.
    all_props = []
    for account in accounts:
        # First, find ALL successors and predecessors.
        successors = list(graph.successors(account))
        predecessors = list(graph.predecessors(account))

        # Next, find only the successors and predecessors with above
        # avg balances.
        high_successors = len(find_high_balance_accounts(graph, successors,
                                                         avg_balance))
        high_predecessors = len(find_high_balance_accounts(graph, predecessors,
                                                           avg_balance))

        # Calculate the proportion of high balance transactions for the
        # current account (all of its high balance neighbours divided by
        # all of its neighbours in general).
        total_neighbours = len(successors) + len(predecessors)

        if total_neighbours != 0:
            proportion = (high_successors + high_predecessors) / total_neighbours
            all_props.append(proportion)

    if len(all_props) != 0:
        return sum(all_props) / len(all_props)

    # If we reach this point in the code, then there must not
    # have been any valid proportions.
    return 0.0


def find_high_balance_accounts(graph: nx.MultiDiGraph, accounts: list[str],
                               avg_balance: float) -> list[str]:
    """
    Find all the accounts with high balances (greater than the average
    balance provided) in this subset of the Ethereum network.

    Preconditions:
        - graph is not empty
        - avg_balance >= 0
    """
    # Accumulator that holds the addresses of all high balance accounts
    high_balance = []
    for account in accounts:
        if graph.nodes[account] != {}:
            # If the account's balance is greater than average,
            # then we will accept it as having high balance.
            if graph.nodes[account]['balance'] > avg_balance:
                high_balance.append(account)

    return high_balance


if __name__ == "__main__":
    # Check all doctests.
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'allowed-io': [],
        'extra-imports': ['networkx', 'build_graph']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    # Uncomment if necessary, example run of function.
    # from build_graph import build_graph
    # g = build_graph('balances.csv', 'transactions.csv')
    #
    # avg = find_avg_balance(g)
    # prop = high_balance_transactions(g, avg)
