from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import RobotsAndBoxes, Robot, Objective, Box


def robotsAndBoxesPortrayal(agent):
    if agent is None:
        return

    if (isinstance(agent, Robot)):
        portrayal = {
            "Shape": "circle",
            "Color": "#FF0000",
            "Layer": 2,
            "Filled": "true",
            "r": 0.5
        }

    if (isinstance(agent, Box)):
        portrayal = {
            "Shape": "rect",
            "Color": "#964B00",
            "Layer": 0,
            "Filled": "true",
            "w": 0.5,
            "h": 0.5
        }

    if (isinstance(agent, Objective)):
        portrayal = {
            "Shape": "rect",
            "Color": "#00FFFF",
            "Layer": 1,
            "Filled": "true",
            "w": 0.8,
            "h": 0.8
        }

    return portrayal


grid = CanvasGrid(robotsAndBoxesPortrayal, 10, 10, 500, 500)

server = ModularServer(RobotsAndBoxes,
                       [grid],
                       "Robots and Boxes",
                       {"agentN": UserSettableParameter("number", "Robot: ", value=4),
                        "density": UserSettableParameter("slider", "Box Density", 0.6, 0.01, 1.0, 0.1),
                        "height": 10,
                        "width": 10})

server.port = 8521
server.launch()
