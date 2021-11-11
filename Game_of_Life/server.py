from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import GameOfLife

colors = {"Alive": "#000000", "Dead": "#FFFFFF"}


def cell_portrayal(cell):
    if cell is None:
        return

    portrayal = {
        "Filled": "true",
        "Shape": "rect",
        "w": 0.7,
        "h": 0.7,
        "Layer": 0,
    }

    (x, y) = cell.pos

    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = colors[cell.condition]

    return portrayal


canvas_element = CanvasGrid(cell_portrayal, 100, 100)

model_param = {
    "height": 100,
    "width": 100,
    "density": 0.2
}

server = ModularServer(GameOfLife, [canvas_element],
                       "Game Of Life", model_param)

server.launch()
