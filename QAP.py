import random
import math

class QAP:
    #<- Taboo Table Class
    class Taboo:
        def __init__(self, n, tenure=5):
            self.n = n
            self.tenure = tenure
            self.create_taboo_table()

        def create_taboo_table(self):
            self.taboo = dict()

        def update_taboo_table(self):
            to_be_removed = []
            for t in self.taboo:
                self.taboo[t] -= 1
                if self.taboo[t] == 0:
                    to_be_removed.append(t)
            for t in to_be_removed:
                self.taboo.pop(t)

        def add_taboo(self, p):
            if p[0] > p[1]:
                p[0], p[1] = p[1], p[0]
            self.taboo[p] = self.tenure

        def is_taboo(self, p):
            return p in self.taboo
    # End of Taboo Table Class ->

    def __init__(self, data_file="data/tai12a.dat", tenure=5):
        self.read_data(data_file)
        self.tenure = tenure
        self.taboo = self.Taboo(self.n, tenure=self.tenure)

    def add_taboo(self, p):
        self.taboo.add_taboo(p)
    
    def update_taboo(self):
        self.taboo.update_taboo_table()

    def fitness_f(self, sol):
        res = 0
        for i in range(len(sol)):
            for j in range(i+1, len(sol)):
                res += self.d[i][j] * self.f[sol[i]][sol[j]]
        return res

    def init_solution(self):
        self.solution = list(range(self.n))
        random.shuffle(self.solution)
        self.solution = [self.solution, None, self.fitness_f(self.solution)]
        print(self.solution)
        return self.solution

    def get_neighbors(self, solution, count=5):
        neighs = []
        cur_actions = []
        while count > 0:
            a, b = sorted(random.choices(list(range(self.n)), k=2))
            if self.taboo.is_taboo((a, b)) or (a, b) in cur_actions:
                continue
            cur_actions.append((a, b))
            sn = solution[:][0][:]
            sn[a], sn[b] = sn[b], sn[a]
            neighs.append([sn, (a, b), math.inf])  # Neighbor, action, fitness
            count -= 1
        return neighs

    def read_data(self, filepath):
        with open(filepath, "r") as file:
            lines = file.readlines()
        self.n = int(lines[0].strip())
        self.d = []
        i = 1
        cnt = self.n
        while cnt>0:
            cur = list(map(int, lines[i].strip().split()))
            if len(cur) > 0:
                self.d.append(cur)
                cnt -= 1
            i += 1
        self.f = []
        cnt = self.n
        while cnt>0:
            cur = list(map(int, lines[i].strip().split()))
            if len(cur) > 0:
                self.f.append(cur)
                cnt -= 1
            i += 1
