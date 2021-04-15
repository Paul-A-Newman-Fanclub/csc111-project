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
import plotly.graph_objects as go
import networkx as nx

from build_graph import build_graph


def plot_graph(graph: nx.MultiDiGraph) -> None:
    """
    Plot the Multiple Directed graph using the plotly library.
    """
    # Choosing the spring layout to position the vertices of the graph.
    pos = nx.spring_layout(graph)

    # Creating the edge trace.
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        # Determine the start and end coordinates of the edge on the graph.
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        # Add all x coordinates to list of x_edge data.
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)

        # Add all y coordinates to list of y_edge data.
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Plotting the edges.
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='black'),
        hoverinfo='text',
        text='Transaction',
        mode='lines'
    )

    # Creating the node trace.
    node_x = []
    node_y = []
    node_size = []
    for node in graph.nodes():
        # Determine the coordinates of each node (using the spring layout defined earlier)
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        size = 10
        if graph.nodes[node] != {}:
            size = graph.nodes[node]['size']

        node_size.append(size)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Hot',
            color=[],
            size=node_size,
            colorbar=dict(
                thickness=10,
                title='# of Transactions (degree)',
                xanchor='left',
                titleside='right'
            ),
            line_width=2
        )
    )

    # Setting the text of each node to its address.
    node_text = []
    for node in graph.nodes():
        node_desc = f"Address: {node}"

        # If the account doesn't have an empty representation
        # in the graph, get its balance.
        if graph.nodes[node] != {}:
            balance = graph.nodes[node]['balance']
            node_desc = f"Address: {node}\nBalance: {balance}"

        # Add the description of the node to the list (which
        # will get added to the trace, updating it).
        node_text.append(node_desc)

    # Update the text and size attributes of the node trace.
    node_trace.text = node_text

    node_neighbours = []
    for node in graph.adjacency():
        # To find the neighbours of this node (accounts who either
        # sent or received transactions from this current account)
        # we must access the second item of a tuple, which contains
        # a dictionary representation of its neighbours (addresses
        # mapped to
        neighbours = len(node[1])
        node_neighbours.append(neighbours)

    node_trace.marker.color = node_neighbours

    # Setting up the layout here.
    layout = go.Layout(
        title='Ethereum Transaction Graph',
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(b=20, l=15, r=15, t=50),  # Setting up the margins around the graph
    )

    # Plot the graph figure.
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=layout
    )

    # update layout
    fig.update_layout(
        title_font_size=15
    )

    fig.show()
