class TabooSearch:
    def __init__(self, problem, iterations=1000, tenure=5):
        # TODO: Define a General Type for different Problems
        self.problem = problem
        self.n_iterations = iterations
        self.iteration = 0
        self.tenure = tenure

        self._init()

    def _init(self):
        self.solution = self.problem.init_solution()
        self.best_solution = self.solution[:]

    def _create_candidates(self):
        self.candidates = self.problem.get_neighbors(self.solution)

    def _evaluate_solutions(self):
        for i in range(len(self.candidates)):
            self.candidates[i][2] = self.problem.fitness_f(self.candidates[i][0])

    def _choose_best_solution(self):
        best_fitness = self.candidates[0][2]
        best_ind = 0
        for i in range(1, len(self.candidates)):
            if self.candidates[i][2] < best_fitness:
                best_fitness = self.candidates[i][2]
                best_ind = i
        self.problem.add_taboo(self.candidates[best_ind][1])
        return self.candidates[best_ind]

    def _task_done(self):
        if self.iteration >= self.n_iterations:
            return True
        self.iteration += 1

    def _update_taboo(self):
        self.problem.update_taboo()

    def run(self):
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
