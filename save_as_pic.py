from matplotlib import pylab
import networkx as nx
from matplotlib import pyplot as plt
import json

def load():
    with open("data.json", "r") as file:
        data = json.load(file)

        edges = data['edges']
        vertices = data['vertices']
        name_dict = data['name_dict']

        return edges, vertices, name_dict


a, b, c = load()
c = {int(x):y for x, y in c.items()}

G = nx.Graph()
G.add_edges_from(a)
G.add_nodes_from(b)
#nx.draw_networkx(G, node_size=30, labels=c)
#plt.show()



def save_graph(graph, name_dict, file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(200, 200), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos, edge_color='#DDA0DD')
    nx.draw_networkx_labels(graph, pos, labels=name_dict)

    #cut = 1.00
    #xmax = cut * max(xx for xx, yy in pos.values())
    #ymax = cut * max(yy for xx, yy in pos.values())
    #plt.xlim(0, xmax)
    #plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

#Assuming that the graph g has nodes and edges entered
#save_graph(G, c, "my_graph.svg")

#it can also be saved in .svg, .png. or .ps formats

a = 'asf = {} edfhiyweg'

print(a.format(100))

print(a)