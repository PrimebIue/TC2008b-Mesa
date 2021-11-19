from mesa import Agent


class RandomAgent(Agent):
    """ Modelo para un agente que se mueve aleatoriamente """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direccion = 4

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,  # 8 conectado. Orden: arriba izquierda, centro, derecha; enmedio izquierda y derecha; abajo izquierda, centro, derecha
            include_center=True)  # incluye su posición

        self.direccion = (self.random.randint(0, 8))

        # Verificar cuales espacios a mi alrededor están ocupados
        freeSpaces = []
        for pos in possible_steps:
            freeSpaces.append(self.model.grid.is_cell_empty(pos))

        if freeSpaces[self.direccion]:
            self.model.grid.move_agent(self, possible_steps[self.direccion])
            print(f"Se mueve de {self.pos} a {possible_steps[self.direccion]}")

    def step(self):
        """ En cada paso moverse aleatoriamente """
        print(f"Agente: {self.unique_id} movimiento {self.direccion}")
        self.move()


class ObstacleAgent(Agent):
    """ Modelo para un Obstaculo """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
