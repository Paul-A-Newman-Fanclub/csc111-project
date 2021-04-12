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


def plot_graph(graph: nx.MultiDiGraph) -> None:
    """
    Plot the Multiple Directed graph using the plotly library.
    """
    # Creating the edge trace.
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        # Determine the start and end coordinates of the edge on the graph.
        x0, y0 = graph.nodes[edge[0]]['pos']
        x1, y1 = graph.nodes[edge[1]]['pos']

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

    # Choosing the spring layout to position the vertices of the graph.
    positions = nx.spring_layout(graph)

    # Creating the node trace.
    node_x = []
    node_y = []
    for node in graph.nodes():
        # No positions until you initialize them (use some nx layout for this).
        x, y = positions[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Hot',
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2
        )
    )

    # Setting the text of each node to its address.
    node_text = []
    for node in graph.nodes():
        node_text.append(node)
    node_trace.text = node_text

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

# Ignore this for now.
# def create_edge(label, x, y) -> go.Scatter:
#     """
#     Create an edge for the graph.
#     """
#     edge = go.Scatter(
#         x=x, y=y,
#         line=dict(width=1, color='black'),
#         hoverinfo='text',
#         text=label,
#         mode='lines'
#     )
#
#     return edge


# node_adjacencies = []
# node_text = []
# for node, adjacencies in enumerate(graph.adjacency()):
#     node_adjacencies.append(len(adjacencies[1]))
#     node_text.append('# of connections: ' + str(len(adjacencies[1])))
#
# node_trace.marker.color = node_adjacencies
# node_trace.text = node_text
