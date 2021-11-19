from mesa import Agent


class Roomba(Agent):
    """ Modelo para Roomba que se mueve aleatoriamente """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direccion = 4
        self.moveCount = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True
        )

        self.direccion = (self.random.randint(0, 8))

        freeSpaces = []
        for pos in possible_steps:
            var = True
            if pos == self.model.grid.out_of_bounds(pos):
                var = False
            elif self.model.grid.get_cell_list_contents(pos):
                for agent in self.model.grid.get_cell_list_contents(pos):
                    if isinstance(agent, ObstacleAgent):
                        var = False
            freeSpaces.append(var)

        if freeSpaces[self.direccion]:
            self.model.grid.move_agent(self, possible_steps[self.direccion])

    def step(self):
        pass

    def advance(self):
        self.move()
        self.moveCount += 1


class ObstacleAgent(Agent):
    """ Modelo para un Obstaculo """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Floor(Agent):
    """ Modelo para el piso """

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 'Clean'

    def step(self):
        for a in self.model.grid.get_cell_list_contents(self.pos):
            if(isinstance(a, Roomba)):
                self.condition = 'Clean'
