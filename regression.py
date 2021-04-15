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
import plotly.express as px
import plotly.graph_objects as go
import math

from sklearn import linear_model, metrics
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

import numpy as np
import networkx as nx
import pandas as pd

from build_graph import build_graph


def balance_correlation_and_plot(graph: nx.MultiDiGraph) -> tuple:
    """
    Calculate the coefficient of determination (r^2) b/w the number of transactions to/from
    an account and it's ether balance, and the root mean squared value
    of the linear model that gives this r^2 value.

    Scatter Plot the number of transactions to/from an account and it's ether balance

    Return results in tuple of the form (r^2, rmse)
    """
    # Choose a random seed (stays the same each time for reproducible results)
    np.random.seed(1212)

    # Dictionary accumulator that maps the balance of a UNIQUE account
    # to its degree (the sum of all transactions that it has both sent
    # and received).
    account_data = {}
    for node in graph.nodes():
        if graph.nodes[node] != {}:
            balance = graph.nodes[node]['balance']
            degree = graph.degree(node)

            # Add pairing as an entry to the dictionary.
            account_data[balance] = degree

    # Convert the predictor data (balance) and response data (number of
    # transactions) into numpy arrays.
    balance_x = np.array(list(account_data)).reshape((-1, 1))
    transactions_y = np.array(list(account_data.values())).reshape(-1, 1)

    # Create a dataframe with the two variables as columns.
    ether_df = pd.DataFrame(list(account_data.items()), columns=['balance', 'degree'])

    # Create the model.
    lin_reg = linear_model.LinearRegression()

    # Perform a train/test split on the data.
    balance_train, balance_test, transaction_train, \
    transaction_test = train_test_split(balance_x, transactions_y, test_size=0.2)

    # Train the model
    reg_model = lin_reg.fit(balance_train, transaction_train)

    # Compute Coefficient of determination
    r2 = reg_model.score(balance_test, transaction_test)

    # Compute RMSE
    predictions = reg_model.predict(transaction_test)
    rmse = metrics.mean_squared_error(y_true=balance_test, y_pred=predictions, squared=False)


    # plot
    fig = px.scatter(ether_df, x='balance', y='degree',
                     title="Degree vs. Balance Scatter Plot",
                     labels={"Balance", "Degree"})
    fig.show()
    return (r2, rmse)
