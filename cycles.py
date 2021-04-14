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
import networkx as nx
from build_graph import build_graph


def transaction_cycle(graph: nx.MultiDiGraph) -> bool:
    """
    Find a cycle from an account back to itself, to determine if
    a series of transactions ever comes back full circle.

    This function tracks a series of transactions from one account to
    others, to see if any Ether that this account sent out eventually
    may have come back to it, as a means of studying the flow of currency
    amongst accounts.
    """
    # Find any relevant nodes that we can recurse on:
    # Criteria:
    # - Must have at least 1 successor (outgoing transaction)
    # - Must have at least 1 predecessor (incoming transaction)
    accounts = []
    for node in graph.nodes():
        num_predecessors = len([p for p in graph.predecessors(node)])
        num_successors = len([s for s in graph.successors(node)])

        if num_successors >= 1 and num_predecessors >= 1:
            accounts.append(node)

    # Loop through all the possible candidate accounts for having a cycle.
    while accounts != []:
        main_acc = accounts.pop()

        # Now, we will check every successor of this main node (to see
        # whether or not it is involved in a cycle that ends back at
        # this main node.)
        print(f"Main node: {main_acc}")

        if _check_cycle(graph, main_acc, main_acc, set(), 0):
            return True

    return False


def _check_cycle(graph: nx.MultiDiGraph, current_account: str,
                 target_account: str, visited: set, length: int) -> bool:
    """
    Recursive helper function for transaction_cycle
    """
    # If the current account is equal to the address of the original node,
    # we know that we've found a cycle! Only as long as the length isn't 0,
    # however, since at the very first call, the two must be equal.
    if current_account == target_account and length != 0:
        if length >= 3:
            return True
        else:
            return False
    else:
        # Add the current account node to the visited set if it's not
        # equal to the target account (which is the case on the first
        # call - when length is still 0)
        new_visited = visited
        if current_account != target_account:
            # Using union to avoid mutation!
            new_visited = visited.union(current_account)

        # Check every successor of the current account, to see if it
        # tracks back to the original target account.
        for successor in graph.successors(current_account):
            # Print the current successor being checked and its length (to
            # keep track of where we are).
            print(f"Current Neighbour: {successor}, Length: {length}")
            print([s for s in graph.successors(successor)])

            # If the successor hasn't already been visited, we know we can check it
            # since it might lead us back to the original account.
            if successor not in new_visited and not (successor == target_account and length == 0):
                # Apparently, an account can send transactions to itself on the
                # Ethereum network. The additional check above will account for this possibility
                # skipping it since this is not valid.
                if _check_cycle(graph, successor, target_account, new_visited, length + 1):
                    return True

        # If we reach this, the current successor had no path that led back to the
        # target account, so it can't be part of a cycle.
        return False
