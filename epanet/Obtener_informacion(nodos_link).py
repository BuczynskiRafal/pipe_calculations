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
from epanettools.examples import (
    simple,
)

file = os.path.join(os.path.dirname(simple.__file__), "Net3.inp")
es = EPANetSimulation(file)
