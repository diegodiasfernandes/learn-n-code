import time
import math
from random import choice

class Ant:
    def __init__(self, index: int, alpha: int):
        self.index: int = index
        self.alpha: int = alpha
        self.parameters: dict | None = None
        self.performance: int = 0

    def __str__(self):
        return f'Ant {self.index}: {self.parameters} \n  Performance => {self.performance}'

    def getParameters(self, graph: dict, variables: list):
        parameters = {}
        for v in variables:
            next_options = graph[v]
            chosen_option = self.nextMove(next_options, self.alpha)
            parameters[v] = chosen_option
        
        self.parameters = parameters
        
        return parameters

    def nextMove(self, value_options: dict, alpha: float):
        def adjustPheromones():
            sum: float = 0
            alpha_pheromones: list[float] = []
            for boolean in value_options.keys():
                phero = value_options[boolean] ** alpha
                alpha_pheromones.append(phero)
                sum += phero
            
            return list(value_options.keys()), alpha_pheromones, float(sum)

        keys, alpha_pheromones, total_sum = adjustPheromones()

        percentage = [round((pheromone / total_sum) * 100) for pheromone in alpha_pheromones]
        probabilities: list[bool] = []
        for key, repetitions in zip(keys, percentage):
            probabilities.extend([key] * repetitions)

        chosen_option = choice(probabilities)

        return chosen_option

class ACO:
    def __init__(self, file_path: str = 'path_to_sat_file'):
        self.file_path: str             = file_path
        self.variables: set             = set()
        self.clauses: list[dict]        = []
        self.total_clauses_num: int     = 0
        self.graph: dict                = {}
        self.current_index: int         = 0
        self.ants_arr: list[Ant]        = []
        self.best_performance           = 0

        self.total_ants: int            = 500
        self.n_offline_ants: int        = 15

    def readSAT(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                clause = {}
                for num in line.split(sep=' '):
                    try:
                        num = int(num)
                        if num > 0:
                            clause[num] = 1
                        else:
                            clause[abs(num)] = -1

                        self.variables.add(abs(num))
                    except ValueError:
                        continue

                self.clauses.append(clause)

        self.total_clauses_num = len(self.clauses)

    def initialize(self):
        self.readSAT()
        self.buildGraph()

        start = time.perf_counter()
        ant = self.colonize()
        end = time.perf_counter()

        return ant, (end-start)

    def colonize(self):
        # offline search
        for _ in range(self.n_offline_ants):
            ant = self.generateAnt(True)
            parameters = ant.getParameters(self.graph, self.variables)
            ant.performance = self.performance(parameters)
            self.addPheromones(ant, offline_phase=True)
            
            self.ants_arr.append(ant)

            if ant.performance == self.total_clauses_num:
                return ant
        
        self.evaporate()

        # online search
        for _ in range(self.n_offline_ants, self.total_ants):
            ant = self.generateAnt()
            parameters = ant.getParameters(self.graph, self.variables)
            ant.performance = self.performance(parameters)

            self.addPheromones(ant)
            self.evaporate()

            self.ants_arr.append(ant)

            if ant.performance == self.total_clauses_num:
                return ant
        
        return max(self.ants_arr, key=lambda ant: ant.performance)

    def addPheromones(self, ant: Ant, offline_phase: bool = False):
        def pheromonesEquation(ant: Ant):
            performance = ant.performance / self.total_clauses_num
            e: float = 2.71
            sig: float = 1 / (1 + (e ** (-performance + 0.4)))
            performance_component: float = (sig + 0.55) ** 20

            stamp = (math.log10(ant.index+1))
            index_component = 1 * stamp
            if offline_phase:
                index_component = 1

            pheromones = (performance_component * index_component) / 2

            if performance >= self.best_performance: 
                pheromones += 5
                self.best_performance = performance
            
            return pheromones

        add_pheromones = pheromonesEquation(ant)
        for v in self.variables:
            chosen_param = ant.parameters[v]
            self.graph[v][chosen_param] += add_pheromones

    def evaporate(self):
        for v in self.variables:
            for option in self.graph[v].keys():
                evaporation_rate = 90 / 100
                new_pheromones = round(self.graph[v][option] * evaporation_rate, 2)
                self.graph[v][option] = max(10, new_pheromones)
        
    def generateAnt(self, alpha_zero: bool = False) -> Ant:
        if alpha_zero:
            ant = Ant(self.current_index, 0)

        else:
            alpha_map: dict[int, float] = {0: 0.8, 1: 1, 2: 2, 3: 3}
            ant = Ant(self.current_index, alpha_map[self.current_index % 4])
        
        self.current_index += 1

        return ant

    def buildGraph(self):
        min_phero = 1
        self.graph = {v: {True: min_phero, False: min_phero} for v in self.variables}

    def performance(self, parameters: dict): # parameters = {0: True, 1: False}
        count = 0
        for clause in self.clauses:
            for variable in clause.keys():
                var_state = parameters[variable]
                if clause[variable] == -1:
                    var_state = not var_state

                if var_state:
                    count += 1
                    break
        
        return count