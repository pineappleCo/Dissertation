from rdflib import Graph, Literal
from rdflib.namespace import URIRef
import igraph
import plotly
from plotly.graph_objs import *

def visualize_graph(graph):
    print("starting graph_viz")
    interactor_triples = list(graph.triples((None, URIRef('http://ppi2rdf.org/proteins#hasInteractor'), None)))
    total_interactions = set([triple[0] for triple in interactor_triples])
    total_interactors = set([triple[2] for triple in interactor_triples])
    node_count = len(total_interactors)
    print(node_count)
    interactors_per_interaction = []
    for interaction in total_interactions:
        interactors = [triple[2] for triple in graph.triples((interaction, URIRef('http://ppi2rdf.org/proteins#hasInteractor'), None))]
        interactors_per_interaction.append(interactors)
    #print(interactors_per_interaction)
    self_interactors = [protein for protein in interactors_per_interaction if len(protein) == 1]
    interaction_pairs = [protein_pair for protein_pair in interactors_per_interaction if len(protein_pair) > 1]
    self_interactor_edges = [(int(str(self_int[0]).split('-')[1][:-1]), int(str(self_int[0]).split('-')[1][:-1])) for self_int in self_interactors]
    pair_interactor_edges = [(int(str(int_pair[0]).split('-')[1][:-1]), int(str(int_pair[1]).split('-')[1][:-1])) for int_pair in interaction_pairs]
    print("number of self interactors: " + str(len(self_interactor_edges)))
    print("number of (non-self) interactors: " + str(len(pair_interactor_edges)))
    #edges = self_interactor_edges + pair_interactor_edges
    edges = pair_interactor_edges
    viz = igraph.Graph.TupleList(edges)
    #extracting node info will go here....
    kk_layout = viz.layout('kk', dim=3)
    X_nodes = [kk_layout[i][0] for i in range(node_count)]
    Y_nodes = [kk_layout[i][1] for i in range(node_count)]
    Z_nodes = [kk_layout[i][2] for i in range(node_count)]
    X_edges = []
    Y_edges = []
    Z_edges = []
    for edge in [e.tuple for e in viz.es]:
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
    plotly.offline.plot(fig, filename='dip.html')