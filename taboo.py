class TabooSearch:
    def __init__(self, problem, iterations=1000, tenure=5):
        """
        Initializes the Taboo search algorithm.
        Args:
            problem (object): The problem instance to solve. This should be a general type
                            that supports the required operations for the Taboo search.
            iterations (int, optional): The maximum number of iterations to perform. 
                                        Defaults to 1000.
            tenure (int, optional): The tenure of the Taboo list, which determines how 
                                    long a move remains forbidden. Defaults to 5.
        """
        # TODO: Define a General Type for different Problems
        self.problem = problem
        self.n_iterations = iterations
        self.iteration = 0
        self.tenure = tenure

        self._init()

    def _init(self):
        """
        Initializes the solution and best_solution attributes for the problem.

        This method sets up the initial solution by calling the `init_solution` 
        method of the problem instance. It also creates a copy of the initial 
        solution to store as the best solution.

        Attributes:
            solution (list): The current solution initialized by the problem.
            best_solution (list): A copy of the initial solution, representing 
                                the best solution found so far.
        """
        self.solution = self.problem.init_solution()
        self.best_solution = self.solution[:]

    def _create_candidates(self):
        """
        Generates a list of candidate solutions by retrieving the neighbors 
        of the current solution from the problem instance.

        This method updates the `self.candidates` attribute with the 
        neighboring solutions of the current solution.

        Returns:
            None
        """
        self.candidates = self.problem.get_neighbors(self.solution)

    def _evaluate_solutions(self):
        """
        Evaluates the fitness of each candidate solution in the list of candidates.

        This method iterates through the list of candidate solutions and updates
        the fitness value of each candidate by calling the fitness function
        defined in the problem instance.

        The candidate solutions are expected to be stored as a list of lists,
        where each candidate is represented as a list with at least three elements:
        - The first element (index 0) is the solution representation.
        - The third element (index 2) is where the fitness value will be stored.

        Assumes that `self.problem.fitness_f` is a callable that takes a solution
        representation as input and returns its fitness value.
        """
        for i in range(len(self.candidates)):
            self.candidates[i][2] = self.problem.fitness_f(self.candidates[i][0])

    def _choose_best_solution(self):
        """
        Selects the best solution from the list of candidate solutions based on fitness value.

        This method iterates through the list of candidate solutions, identifies the one with 
        the lowest fitness value (indicating the best solution), and marks it as taboo to 
        prevent revisiting it in future iterations.

        Returns:
            tuple: The best candidate solution, represented as a tuple containing:
                - Any additional data associated with the candidate (index 0).
                - The solution itself (index 1).
                - The fitness value of the solution (index 2).
        """
        best_fitness = self.candidates[0][2]
        best_ind = 0
        for i in range(1, len(self.candidates)):
            if self.candidates[i][2] < best_fitness:
                best_fitness = self.candidates[i][2]
                best_ind = i
        self.problem.add_taboo(self.candidates[best_ind][1])
        return self.candidates[best_ind]

    def _task_done(self):
        """
        Checks if the task has reached the maximum number of iterations.

        This method determines whether the current iteration count has reached
        or exceeded the specified number of iterations (`n_iterations`). If the
        maximum number of iterations is reached, it returns `True`. Otherwise,
        it increments the iteration count and returns `False`.

        Returns:
            bool: `True` if the maximum number of iterations is reached, otherwise `False`.
        """
        if self.iteration >= self.n_iterations:
            return True
        self.iteration += 1

    def _update_taboo(self):
        """
        Updates the taboo list by delegating the update process to the problem instance.

        This method calls the `update_taboo` method of the associated problem object
        to perform any necessary updates to the taboo list, which is typically used
        in taboo search algorithms to track forbidden moves or solutions.

        """
        self.problem.update_taboo()

    def run(self):
        """
        Executes the main loop of the Taboo search algorithm.
        This method iteratively generates candidate solutions, evaluates them,
        selects the best solution, and updates the Taboo list until the stopping
        condition is met. The best solution found during the search is returned.
        Returns:
            list: The best solution found, represented as a list. The exact format
                and contents of the solution depend on the specific implementation
                of the algorithm.
        """
        while True:
            self._create_candidates()
            self._evaluate_solutions()
            self.solution = self._choose_best_solution()
            if self.solution[2] < self.best_solution[2]:
                self.best_solution = self.solution[:]
            if self._task_done():
                break
            
            self._update_taboo()
        return self.best_solution
