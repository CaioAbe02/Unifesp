import random
from collections import deque

class Cell():
    def __init__(self):
        self.wumpus = False
        self.pit = False
        self.gold = False
        self.breeze = False
        self.stench = False

    def is_available(self):
        if self.wumpus == True or self.pit == True or self.gold == True:
            return False
        return True

    def set_wumpus(self):
        self.wumpus = True

    def set_pit(self):
        self.pit = True

    def set_gold(self):
        self.gold = True

    def setBreeze(self):
        self.breeze = True

    def setStench(self):
        self.stench = True

    def print_cell(self):
        if self.wumpus == True:
            cell = 'W'
        elif self.pit == True:
            cell = 'P'
        elif self.gold == True:
            cell = 'G'
        elif self.breeze == True:
            cell = 'B'
        elif self.stench == True:
            cell = 'S'
        else:
            cell = '-'
        print(f"[{cell}]", end='')

class WumpusWorldEnv():
    def __init__(self):
        self.cave = [[Cell() for _ in range(4)] for _ in range(4)]
        self.set_wumpus()

        for _ in range(1):
            self.set_pit()

        self.set_gold()
        self.set_perceptions()

    def random_available_cell(self):
        while True:
            i = random.randint(0, 3)
            j = random.randint(0, 3)
            cell = self.cave[i][j]

            if (i != 0) or (j != 0):
                if cell.is_available() == True:
                    return cell

    def set_wumpus(self):
        cell = self.random_available_cell()
        cell.set_wumpus()

    def set_pit(self):
        cell = self.random_available_cell()
        cell.set_pit()

    def set_gold(self):
        cell = self.random_available_cell()
        cell.set_gold()

    def set_perceptions(self):
        i = 0
        j = 0
        for row in self.cave:
            for cell in row:
                if cell.pit == True:
                    if i != 3:
                        self.cave[i+1][j].setBreeze()
                    if i != 0:
                        self.cave[i-1][j].setBreeze()
                    if j != 3:
                        self.cave[i][j+1].setBreeze()
                    if j != 0:
                        self.cave[i][j-1].setBreeze()
                if cell.wumpus == True:
                    if i != 3:
                        self.cave[i+1][j].setStench()
                    if i != 0:
                        self.cave[i-1][j].setStench()
                    if j != 3:
                        self.cave[i][j+1].setStench()
                    if j != 0:
                        self.cave[i][j-1].setStench()
                j += 1
            i += 1
            j = 0

    def get_percepts(self, i, j):
        cell = self.cave[i][j]
        return {
            "breeze": cell.breeze,
            "stench": cell.stench,
            "glitter": cell.gold,
            "scream": False
        }

class Agent:
    def __init__(self):
        self.i = 0
        self.j = 0
        self.alive = True
        self.has_gold = False
        self.direction = "E"

        self.visited = set()
        self.safe = set()
        self.safe.add((0, 0))

    def perceive(self, env):
        return env.get_percepts(self.i, self.j)

    def update_knowledge(self, perception, env):
        pos = (self.i, self.j)
        self.visited.add(pos)
        self.safe.add(pos)

        if perception["glitter"]:
            self.has_gold = True

        neighbors = self.get_neighbors(env, self.i, self.j)

        if not perception["breeze"] and not perception["stench"]:
            for n in neighbors:
                self.safe.add(n)

    def get_neighbors(self, env, i, j):
        neighbors = []
        size = len(env.cave)

        if i+1 < size:
            neighbors.append((i+1, j))
        if i-1 >= 0:
            neighbors.append((i-1, j))
        if j+1 < size:
            neighbors.append((i, j+1))
        if j-1 >= 0:
            neighbors.append((i, j-1))

        return neighbors

    def choose_action(self, env):
        if self.has_gold and self.i == 0 and self.j == 0:
            return ("plan", ["CLIMB"])

        if self.has_gold:
            path = self._find_path((self.i, self.j), (0,0), env)

            if path is None:
                return "stop"

            actions = ["GRAB"] + self.path_to_actions(path)
            return ("plan", actions)

        neighbors = self.get_neighbors(env, self.i, self.j)

        safe_moves = [n for n in neighbors if n in self.safe and n not in self.visited]

        if safe_moves:
            target = random.choice(safe_moves)
            path = [(self.i, self.j), target]
            actions = self.path_to_actions(path)
            return ("plan", actions)

        fallback_moves = [n for n in neighbors if n in self.safe]

        if fallback_moves:
            target = random.choice(fallback_moves)
            path = [(self.i, self.j), target]
            actions = self.path_to_actions(path)
            return ("plan", actions)

        return "stop"

    def act(self, action, env):
        if action == "TURN_LEFT":
            self.turn_left()
        elif action == "TURN_RIGHT":
            self.turn_right()
        elif action == "MOVE_FORWARD":
            self.move_forward(env)
        elif action == "GRAB":
            pass
        elif action == "CLIMB":
            print(">>> Vitória! O agente escapou da caverna com o ouro! <<<")
            self.alive = False

    def turn_left(self):
        directions = ["N", "W", "S", "E"]
        idx = directions.index(self.direction)
        self.direction = directions[(idx + 1) % 4]

    def turn_right(self):
        directions = ["N", "E", "S", "W"]
        idx = directions.index(self.direction)
        self.direction = directions[(idx + 1) % 4]

    def move_forward(self, env):
        if self.direction == "N":
            ni, nj = self.i - 1, self.j
        elif self.direction == "S":
            ni, nj = self.i + 1, self.j
        elif self.direction == "E":
            ni, nj = self.i, self.j + 1
        elif self.direction == "W":
            ni, nj = self.i, self.j - 1

        size = len(env.cave)

        if ni < 0 or ni >= size or nj < 0 or nj >= size:
            print("BUMP! (Agente bateu na parede)")
            return

        self.i, self.j = ni, nj

    def path_to_actions(self, path):
        actions = []
        current_direction = self.direction

        for k in range(len(path) - 1):
            (i1, j1) = path[k]
            (i2, j2) = path[k+1]

            if i2 == i1 - 1:
                desired = "N"
            elif i2 == i1 + 1:
                desired = "S"
            elif j2 == j1 + 1:
                desired = "E"
            elif j2 == j1 - 1:
                desired = "W"

            while current_direction != desired:
                actions.append("TURN_RIGHT")
                current_direction = self._simulate_right(current_direction)

            actions.append("MOVE_FORWARD")

        return actions

    def _simulate_right(self, direction):
        order = ["N", "E", "S", "W"]
        idx = order.index(direction)
        return order[(idx + 1) % 4]

    def _find_path(self, start, target, env):
        queue = deque()
        queue.append((start, [start]))

        visited = set()
        visited.add(start)

        while queue:
            (current, path) = queue.popleft()

            if current == target:
                return path

            neighbors = self.get_neighbors(env, current[0], current[1])

            for n in neighbors:
                if n in self.safe and n not in visited:
                    visited.add(n)
                    queue.append((n, path + [n]))
        return None

agent = Agent()
wumpus_world_env = WumpusWorldEnv()

print("Mapa Inicial do Wumpus (G=Ouro, W=Wumpus, P=Abismo):")
for row in wumpus_world_env.cave:
    print("[", end='')
    for cell in row:
        cell.print_cell()
    print("]")
print("\nIniciando simulação...\n")

for step in range(50):
    if not agent.alive:
        break

    perception = wumpus_world_env.get_percepts(agent.i, agent.j)
    agent.update_knowledge(perception, wumpus_world_env)

    action = agent.choose_action(wumpus_world_env)

    if action == "stop":
        print("Agente parou. Não há movimentos seguros ou caminhos disponíveis.")
        break

    if action[0] == "plan":
        actions = action[1]

        for act in actions:
            agent.act(act, wumpus_world_env)
            print(f"Action: {act} | Pos: ({agent.i},{agent.j}) | Dir: {agent.direction}")
            if not agent.alive:
                break
        continue