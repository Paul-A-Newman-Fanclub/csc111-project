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
from typing import Optional

import networkx as nx


def transaction_cycle(graph: nx.MultiDiGraph) -> None:
    """
    Find a cycle from an account back to itself, to determine if
    a series of transactions ever comes back full circle.

    This function tracks a series of transactions from one account to
    others, to see if any Ether that this account sent out eventually
    may have come back to it, as a means of studying the flow of currency
    amongst accounts.

    Preconditions:
      - list(graph.nodes) != []
    """
    # Find any relevant nodes that we can recurse on to find cycles:
    # Criteria:
    # - Must have at least 1 successor (outgoing transaction)
    # - Must have at least 1 predecessor (incoming transaction)
    accounts = []
    for node in graph.nodes():
        num_predecessors = len(list(graph.predecessors(node)))
        num_successors = len(list(graph.successors(node)))

        if num_successors >= 1 and num_predecessors >= 1:
            accounts.append(node)

    # Loop through all the possible candidate accounts for having a cycle.
    cycles = []
    for account in accounts:
        main_acc = account

        # Now, we will check every successor of this main node (to see
        # whether or not it is involved in a cycle that ends back at
        # this main node.)
        print(f"Starting Account: {main_acc}")
        print("Beginning search for cycle starting with this account...")

        cycle = _check_cycle(graph, main_acc, main_acc, set(), 0)
        if cycle is not None:
            print(f"Cycle found for: {main_acc}")
            cycles.append(cycle)
        else:
            print(f"No Cycle found for: {main_acc}")

        print("---------------------------------------")

    # Print a summary of what was found.
    print("###########SUMMARY############")
    print(f"Number of cycles found: {len(cycles)}")

    if cycles == []:
        print("Unfortunately, no cycles could be found.")
    else:
        for i in range(0, len(cycles)):
            print(f"Cycle {i + 1}: {cycles[i]}")


def _check_cycle(graph: nx.MultiDiGraph, current_account: str,
                 target_account: str, visited: set, length: int) -> Optional[list]:
    """
    Recursive helper function for transaction_cycle.

    Recurses on all of the successors of current_account to see if it is
    connected back to target_account in the form of a cycle.

    Returns a list of the cycle's path if it exists, None if it doesn't.

    Preconditions:
        - list(graph.nodes) != []
        - length >= 0

    Sample Usage:
    >>> g = nx.MultiDiGraph()
    >>> for n in range(1, 5):
    ...     g.add_node(str(n))
    >>> for n in range(1, 4):
    ...     g.add_edge(str(n), str(n + 1))
    0
    0
    0
    >>> g.add_edge("4", "1")
    0
    >>> cycle = _check_cycle(g, "1", "1", set(), 0)
      Successor #0: 2
        Successor #1: 3
          Successor #2: 4
            Successor #3: 1
    >>> cycle == ["1", "2", "3", "4", "1"]
    True
    """
    # If the current account is equal to the address of the original node,
    # we know that we've found a cycle! Only as long as the length isn't 0,
    # however, since at the very first call, the two must be equal.
    if current_account == target_account and length != 0:
        # A cycle is only defined for length 3, but there are some
        # transactions
        if length >= 3:
            return [current_account]
        else:
            return None
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
        cycle_path = [current_account]
        for successor in graph.successors(current_account):
            # Print the current successor being checked and its length (to
            # keep track of where we are).
            print('  ' * (length + 1) + f"Successor #{length}: {successor}")

            # If the successor hasn't already been visited, we know we can check it
            # since it might lead us back to the original account.
            if successor not in new_visited and not (successor == target_account and length == 0):
                # Apparently, an account can send transactions to itself on the
                # Ethereum network. The additional check above will account for this possibility
                # skipping it since this is not valid.
                new_path = _check_cycle(graph, successor, target_account, new_visited, length + 1)

                if new_path is not None:
                    cycle_path += new_path
                    return cycle_path

        # If we reach this, the current successor had no path that led back to the
        # target account, so it can't be part of a cycle.
        return None


if __name__ == "__main__":
    # Check all doctests.
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'allowed-io': ['transaction_cycle', '_check_cycle'],
        'extra-imports': ['networkx']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    # Uncomment if necessary, example run of function.
    # from build_graph import build_graph
    # g = build_graph('balances.csv', 'transactions.csv')
    # transaction_cycle(g)
