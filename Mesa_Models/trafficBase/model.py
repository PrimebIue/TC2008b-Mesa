from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import Road, Traffic_Light, Obstacle, Destination, Car
import json


class TrafficModel(Model):
    """
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """

    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.txt"))
        self.carId = 0
        self.destinationList = []
        self.roadList = []

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r{r*self.width+c}",
                                     self, dataDictionary[col])
                        agent.pos = (c, self.height - r - 1)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.roadList.append(agent)
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(
                            f"tl{r*self.width+c}",
                            self,
                            False if col == "S" else True,
                            int(dataDictionary[col]))
                        agent.pos = (c, self.height - r - 1)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        agent.pos = (c, self.height - r - 1)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.destinationList.append(agent)
        # Initialize traffic light directions
        for agent in self.schedule.agents:
            if isinstance(agent, Traffic_Light):
                agent.getDirection()

        self.num_agents = N
        for _ in range(N):
            new_car = Car(self.carId + 1000, self)
            self.carId += 1
            rAgent = 0

            def randomDest(rAgent):
                if isinstance(rAgent, Destination):
                    new_car.destination = rAgent
                else:
                    rAgent = self.random.choice(self.destinationList)
                    randomDest(rAgent)

            def findPosition(rAgent):
                if isinstance(rAgent, Road):
                    new_car.pos = rAgent.pos
                    new_car.pathFinding()
                    self.grid.place_agent(new_car, new_car.pos)
                    self.schedule.add(new_car)
                else:
                    rAgent = self.random.choice(self.roadList)
                    findPosition(rAgent)

            randomDest(rAgent)
            findPosition(rAgent)
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        if self.schedule.steps % 10 == 0:
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        agent.state = not agent.state
