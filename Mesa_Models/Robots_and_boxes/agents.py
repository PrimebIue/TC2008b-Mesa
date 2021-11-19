from mesa import Agent


class Robot(Agent):

    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.direction = 0

    def move(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )

        print("pos: ")

        freeSpaces = []
        for pos in possibleSteps:
            var = True
            if self.model.grid.get_cell_list_contents(pos):
                for agent in self.model.grid.get_cell_list_contents(pos):
                    if isinstance(agent, Robot):
                        var = False
                    # TODO - Check if box if Robot has box
            freeSpaces.append(var)

        self.direction = (self.random.randint(0, len(freeSpaces)-1))
        print("free: ", freeSpaces)
        print(self.direction)

        if freeSpaces[self.direction]:
            self.model.grid.move_agent(self, possibleSteps[self.direction])
            print(possibleSteps[self.direction])

    def step(self):
        self.move()


class Box(Agent):

    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)


class Objective(Agent):

    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
