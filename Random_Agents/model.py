from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa import Model
from agent import RandomAgent, ObstacleAgent


class RandomModel(Model):
    """ Modelo para los autos """

    def __init__(self, N, ancho, alto):
        self.num_agents = N
        self.grid = SingleGrid(ancho, alto, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Crear obstaculos en los limites del grid
        numObs = (ancho * 2) + (alto * 2 - 4)
        listaPosLimite = [(col, ren) for col in [0, ancho-1]
                          for ren in range(alto)]
        # Los dos renglones limite
        for col in range(1, ancho-1):
            for ren in [0, alto-1]:
                listaPosLimite.append((col, ren))
        print(listaPosLimite)

        for i in range(numObs):
            a = ObstacleAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaPosLimite[i])

        for i in range(self.num_agents):
            # La numeracion de los agentes empieza en el 1000
            a = RandomAgent(i+1000, self)
            self.schedule.add(a)
            # Add the agent to a random empty grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while (not self.grid.is_cell_empty((x, y))):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
