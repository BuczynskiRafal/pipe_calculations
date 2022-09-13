import os
import tempfile
from epanettools.epanettools import (
    EPANetSimulation,
    Node,
    Link,
)
from epanettools.examples import simple

file = os.path.join(os.path.dirname(simple.__file__), "Net3.inp")
sim = EPANetSimulation(file)

# Compare ENgetlinkvalue to get data from the network tube 81 and node 55
diameters = Link.value_type["EN_DIAMETER"]
elevation = Node.value_type["EN_ELEVATION"]
# print(f"diameters value in dict value_type from epanettools Link: {diameters}")
# print(f"elevation value in dict value_type from epanettools Node: {elevation}")

# first way
diam_81_a = sim.network.links[81].results[diameters]
# print(diam_81_a)
diam_81_b = sim.ENgetlinkvalue(81, diameters)[1]
# print(diam_81_b)

# Use ENsetnodevalue to change network parameters
pipe = sim.ENsetlinkvalue(1, diameters, 10)

print(dir(sim.ENsetlinkvalue))
print(pipe)
# We must save the changes in a new inp file


file = os.path.join(tempfile.gettempdir(), "new.inp")
sim.ENsaveinpfile(file)
es2 = EPANetSimulation(file)
