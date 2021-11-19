from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation

from agents import Robot, Box, Objective


class RobotsAndBoxes(Model):

    def __init__(self, height, width, density, agentN):
        super().__init__()
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(width, height, False)
        self.agentN = agentN

        objectivePos = self.grid.find_empty()
        print(objectivePos)

        # Add Objective
        objective = Objective(1000, self)
        self.grid.place_agent(objective, objectivePos)
        self.schedule.add(objective)

        # Add the Robot
        for i in range(self.agentN):
            a = Robot(i, self)
            self.grid.place_agent(a, objectivePos)
            self.schedule.add(a)

        # Add Boxes
        id = 0
        for (contents, x, y) in self.grid.coord_iter():
            if (self.grid.is_cell_empty((x, y))):
                if self.random.random() < density:
                    newBox = Box(id+2000, self)
                    self.grid.place_agent(newBox, (x, y))
                    self.schedule.add(newBox)
                    id += 1

    def step(self):
        self.schedule.step()
