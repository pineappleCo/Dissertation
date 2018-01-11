import sys
import igraph
from pickler import unpickle
import plotly
from plotly.graph_objs import *

def edges_to_ids(nodes, edges):
    return [(nodes.index(edge[0]), nodes.index(edge[1])) for edge in edges]

def get_verbose_labels(nodes):
    

def vis_pin(pin, filename):
    g = igraph.Graph()
    g.add_vertices(pin[0])
    edge_ids = edges_to_ids(pin[0], pin[1])
    g.add_edges(edge_ids)
    print('graph constructed')

    labels = [str(node)[28:] for node in pin[0]]
    verbose_labels = get_verbose_labels(pin[0])

    print('calculating layout...')
    kk_layout = g.layout('kk', dim=3)
    print('layout done')

    node_count = len(pin[0])

    x_nodes = [kk_layout[i][0] for i in range(node_count)]
    y_nodes = [kk_layout[i][1] for i in range(node_count)]
    z_nodes = [kk_layout[i][2] for i in range(node_count)]
    x_edges = []
    y_edges = []
    z_edges = []
    for edge in [e.tuple for e in g.es]:
        x_edges += [kk_layout[edge[0]][0], kk_layout[edge[1]][0], None]
        y_edges += [kk_layout[edge[0]][1], kk_layout[edge[1]][1], None]
        z_edges += [kk_layout[edge[0]][2], kk_layout[edge[1]][2], None]

    edge_trace = Scatter3d(x=x_edges, y=y_edges, z=z_edges, mode='lines',
                           line=Line(color='rgb(125,125,125)', width=1), hoverinfo='none')
    node_trace = Scatter3d(x=x_nodes, y=y_nodes, z=z_nodes, mode='markers',
                           marker=Marker(symbol='dot', size=6, color='group', colorscale='Viridis',
                                         line=Line(color='rgb(50,50,50)', width=0.5)), text=labels, hoverinfo='text')
    axis = dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')
    layout = Layout(title=filename, width=1000, height=1000, showlegend=False,
                    scene=Scene(xaxis=XAxis(axis), yaxis=YAxis(axis), zaxis=ZAxis(axis)),
                    margin=Margin(t=100), hovermode='closest')
    data = Data([edge_trace, node_trace])
    fig = Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=filename + '.html')

if __name__ == '__main__':
    filename = sys.argv[1]
    pin = unpickle(filename)
    vis_pin(pin, filename)