from model import RoombaModel, Roomba, ObstacleAgent, Floor
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

COLORS = {'Clean': "#00FFFF", 'Dirty': "#964B00"}


def roombaPortrayal(agent):
    if agent is None:
        return

    if (isinstance(agent, Floor)):
        portrayal = {
            "Shape": "rect",
            "w": 0.7,
            "h": 0.7,
            "Color": COLORS[agent.condition],
            "Layer": 0,
            "Filled": "true"
        }

    if (isinstance(agent, Roomba)):
        portrayal = {
            "Shape": "circle",
            "Color": "brown",
            "Layer": 1,
            "Filled": "true",
            "r": 0.5
        }

    if (isinstance(agent, ObstacleAgent)):
        portrayal = {
            "Shape": "circle",
            "Color": "grey",
            "Layer": 2,
            "Filled": "true",
            "r": 0.2
        }
    return portrayal


grid = CanvasGrid(roombaPortrayal, 10, 10, 500, 500)

moves_chart = ChartModule(
    [{"Label": "Moves", "Color": "#000000"}]
)
floor_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

floor_pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

server = ModularServer(RoombaModel,
                       [grid, moves_chart, floor_pie_chart, floor_chart],
                       "Roomba Cleaning",
                       {"N": UserSettableParameter("number", "Roomba Number: ", value=4), "ancho": 10, "alto": 10,
                        "percentage": UserSettableParameter("slider", "Floor Percentage", 0.6, 0.01, 1.0, 0.1),
                        "maxTime": UserSettableParameter("number", "Maximum number of steps", value=1000)
                        })

server.port = 8521
server.launch()
