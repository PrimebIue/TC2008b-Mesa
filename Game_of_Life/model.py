from mesa import Model
from mesa.space import Grid
from mesa.time import SimultaneousActivation

from agent import Cell, agentState


class GameOfLife(Model):

    def __init__(self, height=100, width=100, density=0.9):
        super().__init__()
        self.schedule = SimultaneousActivation(self)
        self.grid = Grid(width, height, True)

        for (contents, x, y) in self.grid.coord_iter():
            new_cell = Cell((x, y), self)
            new_cell.condition = 'Dead'
            if self.random.random() < density:
                new_cell.condition = 'Alive'

            self.grid._place_agent((x, y), new_cell)
            # self.grid.place_agent((x,y), new_cell)
            self.schedule.add(new_cell)

        self.running = True

    def step(self):
        self.schedule.step()

        count = 0
        for cell in self.schedule.agents:
            if cell.condition == agentState[0]:
                count += 1

        if count == 0:
            self.running = False
