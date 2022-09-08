import os
import pprint
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
print(f"file path {file}")
sim = EPANetSimulation(file)
# print(dir(es))



nodes = sim.network.nodes
# print(len(nodes))
nodes_list = list(sim.network.nodes)[:5]
# print(nodes_list)
id_5 = [sim.network.nodes[x].id for x in nodes_list]
# print(id_5)
# print([nodes[node].id for node in nodes_list])
#
m = sim.network.links
print(len(m))
id_pipe_1 = m[1].id
print(id_pipe_1)

a = [m[1].start.id, m[1].end.id]
pipes = m
print(pipes.items())
print(pipes['10'].link_type)
print({k:v.link_type for k, v in pipes.items()})
print(Link.link_types["PUMP"])
pp = pprint.PrettyPrinter()
# pipe types
# pp.pprint(Node.node_types)

pp.pprint(Link.link_types)
print(Link.link_types)

# saber cuantas bombas hay en total y su identificador
# print("Identificador de Bombas")
print([value.id for key, value in pipes.items() if value.link_type == Link.link_types["PUMP"]])
