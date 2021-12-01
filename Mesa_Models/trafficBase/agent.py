from mesa import Agent


class Car(Agent):
    """
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction from one of eight directions
    """

    def __init__(self, unique_id, model):
        """
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.pos = 0
        self.destination = 0
        self.pathIter = 1
        self.path = []
        self.visited = []

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def pathFinding(self):

        print(self.destination.pos)

        # Get direction of current position
        for agent in self.model.grid.iter_cell_list_contents(self.pos):
            if isinstance(agent, Road) or isinstance(agent, Traffic_Light):
                self.currDir = agent.direction

        # Dictionary of connected nodes
        currDirDictionary = {"Right": {"x": [1, 1, 1, 0, 0],
                                       "y": [0, 1, -1, -1, 1]},
                             "Left": {"x": [-1, -1, -1, 0, 0],
                                      "y": [0, 1, -1, 1, -1]},
                             "Up": {"x": [0, -1, 1, -1, 1],
                                    "y": [1, 1, 1, 0, 0]},
                             "Down": {"x": [0, -1, 1, 1, -1],
                                      "y": [-1, -1, -1, 0, 0]},
                             }
        self.visited.append(self.pos)

        queue = []

        queue.append([self.pos])

        while queue:

            path = queue.pop(0)

            node = path[-1]

            for agent in self.model.grid.iter_cell_list_contents(node):
                if isinstance(agent, Road) or isinstance(agent, Traffic_Light):
                    self.currDir = agent.direction

            if node == self.destination.pos:
                self.path = path
                print("end: ", self.path)
                break

            delta_x = currDirDictionary[self.currDir]["x"]
            delta_y = currDirDictionary[self.currDir]["y"]
            grid = self.model.grid

            for (x, y) in zip(delta_x, delta_y):
                nPosX = x + node[0]
                nPosY = y + node[1]

                if nPosX < 26 and nPosY < 26 and nPosX > -1 and nPosY > -1:
                    for agent in grid.iter_cell_list_contents((nPosX, nPosY)):
                        if node[0] == 9 and node[1] == 2:
                            print(self.currDir)
                            print(agent.pos)

                        directionDictionary = {"Right": {"x": [-1, -1, -1, 0, 0],
                                                         "y": [0, 1, -1, 1, -1]},
                                               "Left": {"x": [1, 1, 1, 0, 0],
                                                        "y": [0, 1, -1, 1, -1]},
                                               "Up": {"x": [0, -1, 1, -1, 1],
                                                      "y": [-1, -1, -1, 0, 0]},
                                               "Down": {"x": [0, -1, 1, -1, 1],
                                                        "y": [1, 1, 1, 0, 0]},
                                               }

                        if (isinstance(agent, Road) or isinstance(agent, Traffic_Light)) and agent.pos not in self.visited:

                            nCoordX = directionDictionary[agent.direction]["x"]
                            nCoordY = directionDictionary[agent.direction]["y"]
                            xDiff = node[0] - agent.pos[0]
                            yDiff = node[1] - agent.pos[1]

                            if xDiff in nCoordX and yDiff in nCoordY:
                                self.visited.append(agent.pos)
                                new_path = list(path)
                                new_path.append(agent.pos)
                                queue.append(new_path)
                        elif isinstance(agent, Destination) and agent.pos == self.destination.pos and agent.pos not in self.visited:
                            self.visited.append(agent.pos)
                            new_path = list(path)
                            new_path.append(agent.pos)
                            queue.append(new_path)

    def move(self):
        """
        Moves to the next position defined in path
        """
        if self.pathIter < len(self.path):
            moveBool = True

            for agent in self.model.grid.iter_cell_list_contents(self.path[self.pathIter]):
                if isinstance(agent, Car):
                    moveBool = False
                elif isinstance(agent, Traffic_Light) and not agent.state:
                    moveBool = False
                elif agent == self.destination:
                    moveBool = True
                    break
            if moveBool:
                self.model.grid.move_agent(self, self.path[self.pathIter])
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
        self.pos = 0
        self.orientation = 0
        self.direction = 0

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def getDirection(self):
        x = [1, -1, 0, 0]
        y = [0, 0, 1, -1]
        for (x, y) in zip(x, y):
            newX = x + self.pos[0]
            newY = y + self.pos[1]
            if newX < 26 and newX > -1 and newY < 26 and newY > -1:
                for agent in self.model.grid.iter_cell_list_contents((newX, newY)):
                    if isinstance(agent, Traffic_Light):
                        if agent.pos[0] == self.pos[0]:
                            self.orientation = "Vertical"
                            break
                        elif agent.pos[1] == self.pos[1]:
                            self.orientation = "Horizontal"
                            break
        if self.orientation == "Vertical":
            x = [1, -1]
            y = [0, 0]
            for (x, y) in zip(x, y):
                newX = x + self.pos[0]
                newY = y + self.pos[1]
                if newX < 26 and newX > -1 and newY < 26 and newY > -1:
                    for agent in self.model.grid.iter_cell_list_contents((newX, newY)):
                        if isinstance(agent, Road) and (agent.direction == "Right" or agent.direction == "Left"):
                            self.direction = agent.direction
        elif self.orientation == "Horizontal":
            y = [1, -1]
            x = [0, 0]
            for (x, y) in zip(x, y):
                newX = x + self.pos[0]
                newY = y + self.pos[1]
                if newX < 26 and newX > -1 and newY < 26 and newY > -1:
                    for agent in self.model.grid.iter_cell_list_contents((newX, newY)):
                        if isinstance(agent, Road) and (agent.direction == "Up" or agent.direction == "Down"):
                            self.direction = agent.direction

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
        self.pos = 0

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def step(self):
        pass


class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def __lt__(self, other):
        return self.unique_id < other.unique_id

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

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def step(self):
        pass
