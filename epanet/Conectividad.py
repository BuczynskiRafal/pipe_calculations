import os, pprint
from epanettools.epanettools import (
    EPANetSimulation,
    Node,
    Link,
    Network,
    Nodes,
    Links,
    Patterns,
    Pattern,
    Controls,
    Control,
)
from epanettools.examples import simple

file = os.path.join(os.path.dirname(simple.__file__), "Net3.inp")
sim = EPANetSimulation(file)


# get information about nodes
nodes = sim.network.nodes
# nodes count
# print(len(nodes))
nodes_list = list(sim.network.nodes)[:5]
# get first 5 nodes
id_5 = [sim.network.nodes[x].id for x in nodes_list]
# print(id_5)

all_ids = [nodes[node].id for node in list(nodes)]
# print(all_ids)

links = sim.network.links
# print(len(links))

# get id pipe 1
id_pipe_1 = links[1].id
# print(id_pipe_1)


# information about connections
# start and end connector
connector = [links[1].start.id, links[1].end.id]
# print(connector)

# all connections with 169 node
connections_169 = [connector.id for connector in nodes['169'].links]
# print(vars(nodes['169']))
# print(nodes['169'].links)
print(connections_169)

