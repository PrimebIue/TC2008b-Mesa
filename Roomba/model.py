from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import Roomba, ObstacleAgent, Floor


class RoombaModel(Model):
    """ Modelo para Roomba """

    def __init__(self, N, alto, ancho, percentage, maxTime):
        self.num_agents = N
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(alto, ancho, torus=False)
        self.maxTime = maxTime
        self.time = 0

        self.datacollector = DataCollector(
            {
                "Dirty": lambda m: self.count_type(m, "Dirty"),
                "Clean": lambda m: self.count_type(m, "Clean"),
                "Moves": lambda m: self.count_moves(m),
            }
        )

        # Obstaculos en los limites
        numObs = (ancho * 2) + (alto * 2 - 4)
        listaPosLimite = [(col, ren) for col in [0, ancho-1]
                          for ren in range(alto)]

        for col in range(1, ancho-1):
            for ren in [0, alto-1]:
                listaPosLimite.append((col, ren))

        for i in range(numObs):
            a = ObstacleAgent(i+1000, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaPosLimite[i])

        # Add the Roombas
        for i in range(self.num_agents):
            a = Roomba(i+2000, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        # Place a floor agent everywhere and let it be dirty based on %
        for (contents, x, y) in self.grid.coord_iter():
            if (self.grid.is_cell_empty((x, y))):
                # Create floor
                new_dirt = Floor((x, y), self)
                if self.random.random() < percentage:
                    new_dirt.condition = 'Dirty'
                self.grid.place_agent(new_dirt, (x, y))
                self.schedule.add(new_dirt)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.time += 1
        self.schedule.step()
        self.datacollector.collect(self)

        if self.count_type(self, 'Dirty') == 0 or self.time >= self.maxTime:
            self.running = False

    @staticmethod
    def count_type(model, floor_condition):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Floor) and agent.condition == floor_condition:
                count += 1

        return count

    @staticmethod
    def count_moves(model):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Roomba):
                count += agent.moveCount
        return count
