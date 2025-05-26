import random
import math
from enum import Enum
from collections import defaultdict

class NeighType(Enum):
    """
    Enum class to represent different types of neighborhood structures for optimization algorithms.
    Attributes:
        SWAP (int): Represents the swap neighborhood structure.
        REVERSE (int): Represents the reverse neighborhood structure.
    """
    SWAP = 0
    REVERSE = 1
    ADHOC = 2

ADHOC_SWP = 0.8
ADHOC_REV = 1 - ADHOC_SWP

class QAP:
    #<- Taboo Table Class
    class Taboo:
        """
        A class to implement a Taboo list for managing forbidden moves in optimization algorithms.
        Attributes:
            n (int): The size or dimension of the problem space.
            tenure (int): The number of iterations a move remains in the Taboo list.
            taboo (dict): A dictionary representing the Taboo list, where keys are moves (tuples)
                          and values are their remaining tenure.
        Methods:
            create_taboo_table():
                Initializes the Taboo list as an empty dictionary.
            update_taboo_table():
                Decrements the tenure of all moves in the Taboo list. Removes moves whose tenure reaches zero.
            add_taboo(p):
                Adds a move to the Taboo list with the specified tenure. Ensures the move is stored in a consistent order.
            is_taboo(p):
                Checks if a move is currently in the Taboo list.
        """
        def __init__(self, n, tenure=5, use_frequencies=False):
            self.n = n
            self.tenure = tenure
            self.use_frequencies = use_frequencies
            self.create_taboo_table()

        def create_taboo_table(self):
            self.taboo = dict()
            self.taboo_frequencies = defaultdict(int)

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
            if self.use_frequencies:
                self.taboo_frequencies[p] += 1
                if self.taboo_frequencies[p] > self.tenure*2:
                    self.taboo[p] = self.tenure * 4
                    self.taboo_frequencies[p] //= 2

        def is_taboo(self, p):
            return p in self.taboo
    # End of Taboo Table Class ->

    def __init__(self, data_file="data/tai12a.dat", tenure=5, neigh_type=NeighType.SWAP, use_frequencies=False):
        """
        Initializes the QAP (Quadratic Assignment Problem) solver.

        Args:
            data_file (str): The path to the data file containing problem instance data.
                            Defaults to "data/tai12a.dat".
            tenure (int): The tenure value for the Taboo search algorithm, which determines
                        how long a move remains taboo. Defaults to 5.

        Attributes:
            tenure (int): The tenure value for the Taboo search algorithm.
            taboo (Taboo): An instance of the Taboo class initialized with the problem size
                        and the specified tenure.
        """
        self.read_data(data_file)
        self.tenure = tenure
        self.neigh_type = neigh_type
        self.taboo = self.Taboo(self.n, tenure=self.tenure, use_frequencies=use_frequencies)

    def add_taboo(self, p):
        """
        Adds a given element to the taboo list.

        Parameters:
            p (Any): The element to be added to the taboo list.
        """
        self.taboo.add_taboo(p)
    
    def update_taboo(self):
        """
        Updates the taboo table by invoking the `update_taboo_table` method 
        of the `taboo` object.

        This method is responsible for maintaining the taboo table, which is 
        typically used in taboo search algorithms to keep track of forbidden 
        moves or states in order to avoid cycles and improve the search process.
        """
        self.taboo.update_taboo_table()

    def fitness_f(self, sol):
        """
        Calculates the fitness value of a given solution for the Quadratic Assignment Problem (QAP).

        The fitness value is computed as the sum of the product of distances and flows
        between facilities based on the given solution.

        Args:
            sol (list): A list representing the solution, where each index corresponds
                        to a facility and the value at that index represents the location
                        assigned to that facility.

        Returns:
            int: The fitness value of the solution, representing the total cost
                based on the distances and flows.
        """
        res = 0
        for i in range(len(sol)):
            for j in range(len(sol)):
                res += self.d[i][j] * self.f[sol[i]][sol[j]]
        return res

    def init_solution(self):
        """
        Initializes a solution for the Quadratic Assignment Problem (QAP).

        This method generates an initial solution by creating a list of integers 
        from 0 to n-1 (where n is the problem size), shuffling the list randomly, 
        and then calculating its fitness using the provided fitness function. 
        The solution is stored as a list containing the shuffled permutation, 
        a placeholder for additional data (set to None), and the fitness value.

        Returns:
            list: A list containing the shuffled solution, a placeholder (None), 
                and the fitness value of the solution.
        """
        self.solution = list(range(self.n))
        random.shuffle(self.solution)
        self.solution = [self.solution, None, self.fitness_f(self.solution)]
        return self.solution

    def get_neighbors(self, solution, count=5):
        """
        Generate a list of neighboring solutions by swapping elements in the current solution.

        Args:
            solution (list): The current solution represented as a list.
            count (int, optional): The number of neighbors to generate. Defaults to 5.

        Returns:
            list: A list of neighbors, where each neighbor is represented as a list containing:
                - The new solution after the swap (list).
                - The action performed as a tuple (a, b), where `a` and `b` are the indices of the swapped elements.
                - The fitness value of the neighbor, initialized to infinity (math.inf).
        """
        neighs = []
        cur_actions = []
        while count > 0:
            a, b = sorted(random.choices(list(range(self.n)), k=2))
            if self.taboo.is_taboo((a, b)) or (a, b) in cur_actions:
                continue
            cur_actions.append((a, b))
            sn = solution[:][0][:] # Copy the current solution encoding
            
            adhoc_neigh = 0
            if self.neigh_type == NeighType.ADHOC:
                if random.random() < ADHOC_SWP:
                    adhoc_neigh = 1
                else:
                    adhoc_neigh = 2
            
            if self.neigh_type == NeighType.SWAP or adhoc_neigh == 1:
                sn[a], sn[b] = sn[b], sn[a]
            elif self.neigh_type == NeighType.REVERSE or adhoc_neigh == 2:
                sn = sn[:a]+sn[a:b][::-1]+sn[b:]
            
            neighs.append([sn, (a, b), math.inf])  # Neighbor, action, fitness
            count -= 1
        return neighs

    def read_data(self, filepath):
        """
        Reads data from a file and initializes the attributes `n`, `d`, and `f`.

        The file is expected to have the following format:
        - The first line contains an integer `n`, representing the size of the problem.
        - The next `n` lines contain the distance matrix `d`, where each line is a row of the matrix.
        - The following `n` lines contain the flow matrix `f`, where each line is a row of the matrix.

        Args:
            filepath (str): The path to the input file.

        Attributes:
            n (int): The size of the problem (number of facilities/locations).
            d (list[list[int]]): The distance matrix, a 2D list of integers.
            f (list[list[int]]): The flow matrix, a 2D list of integers.
        """
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
