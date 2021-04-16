"""
CSC111 Final Project: Reconstructing the Ethereum Network Using
Graph Data Structures in Python

General Information
------------------------------------------------------------------------------
This file was created for the purpose of applying concepts in learned in
CSC111 to the real world problem domain of cryptocurrency transactions.

Module Info: subnetworks.py

This file contains code which attempts to look for the largest interconnected
group of accounts (linked by transactions) within the Ethereum network
graph.

Copyright Information
------------------------------------------------------------------------------
This file is Copyright of Tobey Brizuela, Daniel Lazaro, Matthew Parvaneh, and
Michael Umeh.
"""
import networkx as nx


def transaction_network(graph: nx.MultiDiGraph, account: str) -> list[str]:
    """
    Find the largest connected subset of accounts in the graphical
    representation of the Ethereum network.

    The algorithm used to do this is somewhat similar to that which
    calculates a spanning tree.

    Preconditions:
        - list(graph.nodes) != []
    """
    # Find any relevant nodes that we can recurse on:
    # Criteria:
    # - Must have at least 1 successor (outgoing transaction)
    # - Must have at least 1 predecessor (incoming transaction)
    # We must find the successors and predecessors for a given account
    # separately
    succ = _find_trans_network_successors(graph, account, set())
    pred = _find_trans_network_predecessors(graph, account, set())

    # First, initialize the entire subnetwork of all accounts
    # to just that of the successors. Next, we can add all the predecessor
    # accounts to the subnetwork if they haven't already been counted
    # as successors.
    total_connected = succ.copy()
    for p in pred:
        if p not in total_connected:
            total_connected.append(p)

    return total_connected


def _find_trans_network_successors(graph: nx.MultiDiGraph, account: str,
                                   visited: set) -> list[str]:
    """
    Recursive helper function for transaction_network.

    Recurses on all of the successors of account, using a depth-first
    approach, finding all items that are linked to account through
    a series of transactions.

    Preconditions:
        - list(graph.nodes) != []
        - account != ''
    """
    # Initialize the current network to contain only account
    # (since it is the central account which we start at, and
    # branch out from).
    current_network = [account]

    new_visited = visited.union({account})
    for successor in graph.successors(account):
        if successor not in new_visited:
            # If the successor hasn't already been visited, we recurse
            # on it to find its successors.
            current_network += _find_trans_network_successors(graph, successor,
                                                              new_visited)

    return current_network


def _find_trans_network_predecessors(graph: nx.MultiDiGraph, account: str,
                                     visited: set) -> list[str]:
    """
    Recursive helper function for transaction_network.

    Recurses on all of the predecessors of account, using a depth-first
    approach, finding all items that are linked to account through
    a series of transactions.

    Preconditions:
        - list(graph.nodes) != []
        - account != ''
    """
    current_network = [account]

    new_visited = visited.union({account})
    for predecessor in graph.predecessors(account):
        if predecessor not in new_visited:
            # If the predecessor hasn't already been visited, we recurse
            # on it to find its predecessors.
            current_network += _find_trans_network_predecessors(graph, predecessor,
                                                                new_visited)

    return current_network


def biggest_subnetwork(graph: nx.MultiDiGraph) -> list[str]:
    """
    Find and return a list containing all of the accounts
    that make up the biggest subnetwork of the graph.

    Preconditions:
        - list(graph.nodes) != []
    """
    accounts = []
    for node in graph.nodes():
        # Find the number of successors and predecessors for each account.
        num_predecessors = len(list(graph.predecessors(node)))
        num_successors = len(list(graph.successors(node)))

        # If there is at least 1 successor and 1 predecessor, this account
        # is a viable candidate for having a large subnetwork.
        if num_successors >= 1 and num_predecessors >= 1:
            accounts.append(node)

    # A list of list that will contain every single subnetwork in the graph.
    networks = []
    for account in accounts:
        subnetwork = transaction_network(graph, account)
        networks.append(subnetwork)

    # Find the largest subnetwork (the longest list of accounts).
    biggest_sub = max(networks, key=len)

    # Return information about the biggest subnetwork of interconnected
    # accounts on the
    print("------Biggest Subnetwork------")
    print(f"*Central Account*: {biggest_sub[0]}")
    print(f"Entire subnetwork: {biggest_sub}")
    print("\n")

    return biggest_sub


def future_partners(graph: nx.MultiDiGraph, subnetwork: list[str]) -> None:
    """
    Find future partners of the central account of the biggest subnetwork,
    meaning all those accounts which the central one is likely to engage
    in future transactions with.

    This function employs a similar metric as similarity score in A3,
    except it just uses the number of shared neighbours (accounts) as
    a means of determining which accounts are most likely to be future
    transactions partners.

    Preconditions:
        - list(graph.nodes) != []
    """
    # The account at the center of the
    main_account = subnetwork[0]
    main_neighbours = set(list(graph.successors(main_account))
                          + list(graph.predecessors(main_account)))

    partners = []
    for account in subnetwork[1:]:
        preds = list(graph.predecessors(account))
        succs = list(graph.successors(account))
        acct_neighbours = set(preds + succs)

        # Find out how many of the same accounts as the main account that
        # this account has engaged made a transaction with.
        same_neighbours = len(main_neighbours.intersection(acct_neighbours))

        partners.append((account, same_neighbours))

    # Sort by same neighbours from least to greatest.
    partners.sort(key=lambda partner: partner[1])
    partners.reverse()

    # Print a summary of the central accounts potential future partners.
    print(f"The account at center of the biggest subnetwork is: {main_account}\n")
    print("Below are the accounts in the subnetwork that are most likely to engage\n"
          + "in future transactions with the central account, ranked on how many of the\n"
          + "same neighbours they have. (To be a potential future partner, they must have\n"
          + "AT LEAST ONE common neighbour.)\n")

    for i in range(0, len(partners)):
        if partners[i][1] > 0:
            print(f"#{i + 1} - Account Address: {partners[i][0]}")
            print(f"Number of shared neighbours: {partners[i][1]}\n")

    # If all accounts in the subnetwork had no shared neighbours with the central
    # account, we won't classify them as future partners.
    if all(partners[n][1] == 0 for n in range(0, len(partners))):
        print("It looks like there were no accounts that shared neighbours with"
              + "the main account in this subnetwork. We cannot tell who might be"
              + "a future transactional partner with them.")


if __name__ == '__main__':
    # Check all doctests.
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'allowed-io': ['future_partners', 'biggest_subnetwork'],
        'extra-imports': ['networkx', 'build_graph']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    # Example Test Run
    # from build_graph import build_graph
    # ethereum_graph = build_graph('balances.csv', 'transactions.csv')
    # subnet = biggest_subnetwork(ethereum_graph)
    # future_partners(ethereum_graph, subnet)
