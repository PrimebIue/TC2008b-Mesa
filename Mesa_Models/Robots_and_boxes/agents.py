from mesa import Agent

from pathUtils import findPath


class Robot(Agent):

    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.direction = 0
        self.isEmpty = True
        self.currBox = None
        self.objPos = 0
        self.pathIter = 0

    def moveEmpty(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )

        freeSpaces = []
        for pos in possibleSteps:
            var = True
            if self.model.grid.get_cell_list_contents(pos):
                for agent in self.model.grid.get_cell_list_contents(pos):
                    if isinstance(agent, Robot):
                        var = False
            freeSpaces.append(var)

        self.direction = (self.random.randint(0, len(freeSpaces)-1))

        if freeSpaces[self.direction]:
            coord = possibleSteps[self.direction]
            self.model.m[self.pos[1]][self.pos[0]] = 1
            self.model.grid.move_agent(self, coord)
            if self.model.m[coord[1]][coord[0]] != 2:
                self.model.m[coord[1]][coord[0]] = float('inf')

    def exeMoveFull(self, path, i):
        if path != -1 and len(path) > 1:
            self.model.m[self.pos[1]][self.pos[0]] = 1
            self.model.grid.move_agent(self, (path[i].x, path[i].y))
            self.model.grid.move_agent(self.currBox, (path[i].x, path[i].y))

            if self.model.m[path[i].y][path[i].x] != 2:
                self.model.m[path[i].y][path[i].x] = float('inf')

    def moveFull(self):

        if self.pathIter == 0:
            self.pathIter += 1
            self.path = findPath(self.model.m.copy(),
                                 self.pos[0], self.pos[1], self.objPos[0], self.objPos[1])
            self.exeMoveFull(self.path, self.pathIter)
        else:
            self.pathIter += 1
            if self.path != -1 and self.model.m[self.path[self.pathIter].y][self.path[self.pathIter].x] != float('inf'):
                self.exeMoveFull(self.path, self.pathIter)
            else:
                self.path = findPath(self.model.m.copy(),
                                     self.pos[0], self.pos[1], self.objPos[0], self.objPos[1])
                self.pathIter = 1
                self.exeMoveFull(self.path, self.pathIter)

    def getBox(self):
        for agent in self.model.grid.get_cell_list_contents(self.pos):
            if isinstance(agent, Box):
                self.isEmpty = False
                self.currBox = agent

    def checkObj(self):
        for agent in self.model.grid.get_cell_list_contents(self.pos):
            if isinstance(agent, Objective):
                self.isEmpty = True
                self.currBox = None
                self.pathIter = 0

    def step(self):
        if not self.isEmpty:
            pass
        else:
            self.moveEmpty()

    def advance(self):
        if not self.isEmpty:
            self.moveFull()
            self.checkObj()
        else:
            self.getBox()


class Box(Agent):

    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.objPos = 0

    def advance(self):
        if self.pos == self.objPos:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)


class Objective(Agent):

    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
