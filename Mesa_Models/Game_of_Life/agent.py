from mesa import Agent

agentState = ['Alive', 'Dead']


class Cell(Agent):

    def __init__(self, pos, model) -> None:
        super().__init__(pos, model)
        self.pos = pos
        self.condition = agentState[0]
        self.n_state = self.condition

    def step(self):
        self.n_state = self.condition
        count = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if (neighbor.condition == 'Alive'):
                count += 1
        if (self.condition == 'Alive' and (count != 3 and count != 2)):
            self.n_state = 'Dead'
        elif(self.condition == 'Dead' and count == 3):
            self.n_state = 'Alive'

    def advance(self):
        self.condition = self.n_state
