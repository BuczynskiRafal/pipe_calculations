import os
from epanettools.epanettools import (
    EPANetSimulation,
    Node,
)
from epanettools.examples import simple

file = os.path.join(os.path.dirname(simple.__file__), "Net3.inp")
es = EPANetSimulation(file)


nodes = es.network.nodes
links = es.network.links

# Simulate/run the network
es.run()
# get pressure at node 103 for all simulations
pressure = Node.value_type["EN_PRESSURE"]
print(f"pressure key: {pressure}")
pressure_103 = es.network.nodes["103"].results[pressure]
print(f"pressures for pipe 103: {pressure_103} (after simulation)")
# Get the demand on the node
demand = Node.value_type["EN_DEMAND"]
print(f"demand key: {demand}")
demand_103 = es.network.nodes["103"].results[demand][3]
print(f"demand: {demand_103}")
