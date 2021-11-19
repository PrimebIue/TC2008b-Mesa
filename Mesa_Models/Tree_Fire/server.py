from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import ForestFire

colors = {"Fine": "#00AA00", "On Fire": "#AA0000", "Burned": "#000000"}


def forest_portrayal(tree):
    if tree is None:
        return

    portrayal = {
        "Filled": "true",
        "Shape": "rect",
        "w": 0.7,
        "h": 0.7,
        "Layer": 0,
    }

    (x, y) = tree.pos

    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = colors[tree.condition]

    return portrayal


canvas_element = CanvasGrid(forest_portrayal, 100, 100)

model_param = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree Density",
                                     0.6, 0.01, 1.0, 0.1)
}

server = ModularServer(
    ForestFire, [canvas_element], "Forest Fire", model_param)

server.launch()
