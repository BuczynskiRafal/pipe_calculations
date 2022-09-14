# Program to read pressures in EPANET and tell if there are nodes with negative P
import PySimpleGUI as sg
from epanettools.epanettools import EPANetSimulation, Node, Link, Network, Node
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# deploy the GUI
event, values = sg.Window(
    "Pressures and Velocities v1.0",
    [
        [sg.Text("Select EPANET.inp file")],
        [sg.Input(), sg.FileBrowse()],
        [sg.OK()],
    ],
).Read()

# read the network
file = values[0]
sim = EPANetSimulation(file)

# creating nodes and pipes
links = sim.network.links
nodes = sim.network.nodes

# get the count of pipes
_, num_links = sim.ENgetcount(sim.EN_LINKCOUNT)  # count of links
# print(ret, num_links)
ret, num_nodes = sim.ENgetcount(sim.EN_NODECOUNT)  # count of nodes
# print(ret, num_nodes)


# instanciar los objetos link y nodos del modelo
diameter = Link.value_type["EN_DIAMETER"]
pressure = Node.value_type["EN_PRESSURE"]
flow = Link.value_type["EN_FLOW"]

sim.run()  # correr el modelo
NODES = ""
P = []
ID = []
P_neg = []
ID_neg = []
# para mostrar las presiones
for i in range(num_nodes - 1):

    if nodes[i + 1].results[pressure][0] < 0:
        NODES = NODES + " " + nodes[i].id
        P_neg.append(nodes[i + 1].results[pressure][0])
        ID_neg.append(nodes[i + 1].id)
    else:
        P.append(nodes[i + 1].results[pressure][0])
        ID.append(nodes[i + 1].id)

sg.Popup("Nodos negativos son: ", NODES)

# Configurar las características del gráfico
plt.bar(ID, P, label="Presiones+(mca)", width=0.5, color="lightblue")
plt.bar(ID_neg, P_neg, label="Presiones-(mca)", width=0.5, color="orange")
# Definir título y nombres de ejes
plt.title("Piso de Presiones")
plt.ylabel("P mca")
plt.xlabel("Nodos")
# Mostrar leyenda y figura
plt.legend()
plt.show()
