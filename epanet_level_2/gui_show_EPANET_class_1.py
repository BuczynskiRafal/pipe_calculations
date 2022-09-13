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

# leer la red
file = values[0]
es = EPANetSimulation(file)

# instanciar nodos y conductos
cond = es.network.links
nod = es.network.nodes

# obtener la cantidad de tubos
ret, num_links = es.ENgetcount(es.EN_LINKCOUNT)  # numero de links
ret, num_nodes = es.ENgetcount(es.EN_NODECOUNT)  # numero de nodos

# instanciar los objetos link y nodos del modelo
diametros = Link.value_type["EN_DIAMETER"]
presiones = Node.value_type["EN_PRESSURE"]
flow = Link.value_type["EN_FLOW"]

es.run()  # correr el modelo
NODOS = ""
P = []
ID = []
P_neg = []
ID_neg = []
# para mostrar las presiones
for i in range(num_nodes - 1):

    if nod[i + 1].results[presiones][0] < 0:
        NODOS = NODOS + " " + nod[i].id
        P_neg.append(nod[i + 1].results[presiones][0])
        ID_neg.append(nod[i + 1].id)
    else:
        P.append(nod[i + 1].results[presiones][0])
        ID.append(nod[i + 1].id)

sg.Popup("Nodos negativos son: ", NODOS)

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
