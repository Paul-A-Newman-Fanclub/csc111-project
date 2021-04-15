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
from build_graph import build_graph

import networkx as nx


def transaction_network(graph: nx.MultiDiGraph, account: str) -> list[str]:
    """
    Find a maximally connected subset of accounts in the greater
    representation of the ethereum network.

    This might help us figure out who potential future transaction partners
    may be, based on which accounts have interacted with
    """
    # Find any relevant nodes that we can recurse on:
    # Criteria:
    # - Must have at least 1 successor (outgoing transaction)
    # - Must have at least 1 predecessor (incoming transaction)
    succ = _find_trans_network_successors(graph, account, set())
    pred = _find_trans_network_predecessors(graph, account, set())

    total_connected = succ.copy()
    for p in pred:
        if p not in total_connected:
            total_connected.append(p)

    return total_connected


def _find_trans_network_successors(graph: nx.MultiDiGraph, account: str,
                                   visited: set) -> list[str]:
    """
    Like spanning trees.
    """
    current_network = [account]

    new_visited = visited.union({account})
    for successor in graph.successors(account):
        if successor not in new_visited:
            current_network += _find_trans_network_successors(graph, successor, new_visited)

    return current_network


def _find_trans_network_predecessors(graph: nx.MultiDiGraph, account: str,
                                     visited: set) -> list[str]:
    """
    Like spanning trees.
    """
    current_network = [account]

    new_visited = visited.union({account})
    for predecessor in graph.predecessors(account):
        if predecessor not in new_visited:
            current_network += _find_trans_network_predecessors(graph, predecessor, new_visited)

    return current_network


def biggest_subnetwork(graph: nx.MultiDiGraph) -> list[str]:
    """
    Find the biggest subnetwork.
    """
    accounts = []
    for node in graph.nodes():
        num_predecessors = len([p for p in graph.predecessors(node)])
        num_successors = len([s for s in graph.successors(node)])

        if num_successors >= 1 and num_predecessors >= 1:
            accounts.append(node)

    # A list of list that will contain every single subnetwork in the graph.
    networks = []
    for account in accounts:
        subnetwork = transaction_network(graph, account)
        networks.append(subnetwork)

    return max(networks, key=len)


def future_partners(graph: nx.MultiDiGraph, subnetwork: list[str]) -> None:
    """
    Find future partners of the main account at the center of the
    biggest subnetwork.
    """
    main_account = subnetwork[0]
    main_neighbours = set(list(graph.successors(main_account)) +
                          list(graph.predecessors(main_account)))

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

    print(f"The account at center of the biggest subnetwork is: {main_account}\n")
    print("Below are the accounts in the subnetwork that are most likely to engage\n" +
          "in future transactions with the main account, ranked on how many of the\n" +
          'same neighbours they have. (To be a future partner, they must have AT LEAST\n' +
          "ONE common neighbour.\n")

    for i in range(0, len(partners)):
        if partners[i][1] > 0:
            print(f"#{i + 1} - Account Address: {partners[i][0]}")
            print(f"Number of shared neighbours: {partners[i][1]}\n")


if __name__ == '__main__':
    ethereum_graph = build_graph('balances.csv', 'transactions.csv')
    subnet = biggest_subnetwork(ethereum_graph)
    future_partners(ethereum_graph, subnet)
