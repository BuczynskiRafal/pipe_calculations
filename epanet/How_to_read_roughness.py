import os
from epanettools.epanettools import (
    EPANetSimulation,
    Node,
    Link,
)
from epanettools.examples import simple

file = os.path.join(os.path.dirname(simple.__file__), "Net3.inp")
# print(f"file path {file}")
sim = EPANetSimulation(file)

# Compare ENgetlinkvalue to get data from the network tube 81 and node 55
diameter = Link.value_type["EN_DIAMETER"]
elevation = Node.value_type["EN_ELEVATION"]

# first way to get diameter
diam_81_A = sim.network.links[81].results[diameter]
# print(diam_81_A)
# second way to get diameter
diam_81_B = sim.ENgetlinkvalue(81, diameter)[1]
# print(dir(es.ENgetlinkvalue))
# print(diam_81_B)

# get roughness
roughness = Link.value_type["EN_ROUGHNESS"]
print(f"key of roughness: {roughness}")
pipe_5 = sim.network.links[5].results[roughness]
print(f"results in dict: {sim.network.links[5].results}")
# print(dir(sim.network.links[5].results))
print(pipe_5)
