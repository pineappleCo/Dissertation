from rdflib import Graph, Literal
from rdflib.namespace import URIRef
import igraph
import plotly
from plotly.graph_objs import *

def visualize_graph(graph):
    print("starting graph_viz")
    interactor_triples = graph.triples((None, URIRef('http://ppi2rdf.org/proteins#hasInteractor'), None))
    for triple in graph.triples((None, URIRef('http://ppi2rdf.org/proteins#hasInteractor'), None)):
        print(triple)
    interactions = set([subject_object[0] for subject_object in interactor_triples])
    print(interactions)
    interactors = set([subject_object[1] for subject_object in interactor_triples])
    print(interactors)
    node_count = len(interactors)
    edges = []
    for interaction in interactions:
        interactors_gen = graph.objects(subject=URIRef(interaction), predicate=URIRef('ppi2rdf.org/proteins#hasInteractor'))
        interactors_temp = [interactor for interactor in interactors_gen]
        interactors_tup = (interactors_temp[0], interactors_temp[1])
        edges.append(interactors_tup)
    viz = igraph.Graph(edges, directed=False)
    #extracting node info will go here....
    kk_layout = viz.layout('kk', dim=3)
    X_nodes = [kk_layout[i][0] for i in range(node_count)]
    Y_nodes = [kk_layout[i][1] for i in range(node_count)]
    Z_nodes = [kk_layout[i][2] for i in range(node_count)]
    X_edges = []
    Y_edges = []
    Z_edges = []
    for edge in edges:
        X_edges += [kk_layout[edge[0]][0], kk_layout[edge[1]][0], None]
        Y_edges += [kk_layout[edge[0]][1], kk_layout[edge[1]][1], None]
        Z_edges += [kk_layout[edge[0]][2], kk_layout[edge[1]][2], None]
    trace1 = Scatter3d(x=X_edges, y=Y_edges, z=Z_edges, mode='lines',
                       line=Line(color='rgb(125,125,125)', width=1), hoverinfo='none')
    trace2 = Scatter3d(x=X_nodes, y=Y_nodes, z=Z_nodes, mode='markers',
                       marker=Marker(symbol='dot', size=6, color='group', colorscale='Viridis',
                                     line=Line(color='rgb(50,50,50)', width=0.5)), hoverinfo='text')
    axis = dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')
    layout = Layout(title='PIN', width=1000, height=1000, showlegend=False,
                    scene=Scene(xaxis=XAxis(axis), yaxis=YAxis(axis), zaxis=ZAxis(axis)),
                    margin=Margin(t=100), hovermode='closest')
    data = Data([trace1, trace2])
    fig = Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='pin.html')