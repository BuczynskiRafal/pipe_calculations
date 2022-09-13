import os
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
# get information about links
links = sim.network.links

sim.run()

# get min and max value of pressure
pressure = Node.value_type["EN_PRESSURE"]
# min
# print(f"{min(sim.network.nodes['101'].results[pressure]):.3f}")
# max
# print(f"{max(sim.network.nodes['101'].results[pressure]):.3f}")
# all pressures
# print(f"{sim.network.nodes['101'].results[pressure]}")

# Jakie są węzły z podciśnieniem?
negative_pressure_nodes = [
    node.id for _, node in nodes.items() if min(node.results[pressure]) < 0
]
# nodes_neg = sorted([y.id for x, y in nodes.items() if min(y.results[pressure]) < 0])
print(negative_pressure_nodes)


# które są węzłami z jednostkami wydatków większymi niż 4500
demands = Node.value_type["EN_DEMAND"]
junction = Node.node_types["JUNCTION"]
print(f"number of junction in dict of node types: {junction}")
nodes_greater_4500 = sorted(
    [
        node.id
        for _, node in nodes.items()
        if max(node.results[demands]) > 4500 and node.node_type == junction
    ]
)
print(nodes_greater_4500)
