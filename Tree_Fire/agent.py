from mesa import Agent

agentState = ['Fine', 'On Fire', 'Burned']


class TreeCell(Agent):

    def __init__(self, pos, model) -> None:
        super().__init__(pos, model)
        self.pos = pos
        self.condition = agentState[0]

    def step(self):
        if self.condition == agentState[1]:
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == agentState[0]:
                    neighbor.condition = agentState[1]
                self.condition = agentState[2]
