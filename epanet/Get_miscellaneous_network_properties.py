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


nodes = sim.network.nodes
links = sim.network.links


# get pipe diameters
d = Link.value_type["EN_DIAMETER"]
print(f"{sim.network.links[1].results[d][0]:.3f}")
print(f"{sim.network.links[5].results[d][0]:.3f}")
print(f"{sim.network.links[5].results[d]}")

# Get the temporary patterns
pattern_1 = sim.network.patterns[1]
print(vars(pattern_1))
print(pattern_1.store)
print(f"{pattern_1.store.values()}")
# print(type(pattern_1))

pattern_list = list(pattern_1.values())
print("%2.1f " * len(pattern_list) % tuple(pattern_list))
