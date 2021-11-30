from mesa import Agent


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction from one of eight directions
    """

    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.pos = 0
        self.destination = 0
        self.pathIter = 0
        self.path = []
        self.visited = []

    def recursion(self, currPos):
        for agent in self.model.grid.iter_cell_list_contents(currPos):
            if isinstance(agent, Road):
                self.currDir = agent.direction

        for agent in self.model.grid.iter_neighbors(currPos, True):
            if agent == self.destination:
                print("here")
                return True
            elif isinstance(agent, Road) and agent.pos not in self.visited:
                self.visited.append(agent.pos)
                x = currPos[0]
                y = currPos[1]

                directionDictionary = {"Right": {"x": [-1, -1, -1],
                                                 "y": [0, 1, -1]},
                                       "Left": {"x": [1, 1, 1],
                                                "y": [0, 1, -1]},
                                       "Up": {"x": [0, -1, +1],
                                              "y": [-1, -1, -1]},
                                       "Down": {"x": [0, -1, 1],
                                                "y": [1, 1, 1]},
                                       }

                delta_y = directionDictionary[agent.direction]["y"]
                delta_x = directionDictionary[agent.direction]["x"]

                if x - agent.pos[0] in delta_x and y - agent.pos[1] in delta_y:
                    self.path.append(agent.pos)
                    print("re: ", self.path)
                    if self.recursion(agent.pos):
                        return
                    else:
                        self.path.pop()
                    print("last: ", self.path)
        return False

    def move(self):
        """
        Moves to the next position defined in path
        """
        print(self.path)
        if self.pathIter < len(self.path):
            self.model.grid.move_agent(self, self.path[self.pathIter])
            print(self.pos, self.path[self.pathIter])

            self.pathIter += 1

    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        self.move()


class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model, state=False, timeToChange=10):
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass


class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model, direction="Left"):
        super().__init__(unique_id, model)
        self.direction = direction
        self.pos = 0

    def step(self):
        pass
