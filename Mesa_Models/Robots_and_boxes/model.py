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
        self.m = [[1 for i in range(width)] for j in range(height)]

        self.objectivePos = self.grid.find_empty()

        # Add Objective
        objective = Objective(1000, self)
        self.m[self.objectivePos[0]][self.objectivePos[1]]
        self.grid.place_agent(objective, self.objectivePos)
        self.schedule.add(objective)

        # Add the Robot
        for i in range(self.agentN):
            a = Robot(i, self)
            a.objPos = self.objectivePos
            self.grid.place_agent(a, self.objectivePos)
            self.schedule.add(a)

        # Add Boxes
        id = 0
        for (contents, x, y) in self.grid.coord_iter():
            if (self.grid.is_cell_empty((x, y))):
                if self.random.random() < density:
                    newBox = Box(id+2000, self)
                    self.grid.place_agent(newBox, (x, y))
                    newBox.objPos = self.objectivePos
                    self.schedule.add(newBox)
                    id += 1
                    self.m[y][x] = float('inf')
        self.running = True

    def step(self):
        count = 0
        for (a, x, z) in self.grid.coord_iter():
            if (x, z) != self.objectivePos:
                for b in a:
                    if isinstance(b, Box):
                        count += 1
        if count < 1:
            self.running = False

        self.schedule.step()
