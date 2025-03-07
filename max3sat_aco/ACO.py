import time
import math
from random import choice

class Ant:
    def __init__(self, index: int, alpha: int, performance: float = 0):
        self.index: int = index
        self.alpha: int = alpha
        self.parameters: dict | None = None
        self.performance: float = performance

    def __str__(self):
        return f'Ant {self.index}: {self.parameters} \n  Performance => {self.performance}'

    def nextMove(self, value_options: dict, alpha: float):
        # Calculates the value (T/F) for the next variable given the pheromones and alpha 
        def adjustPheromones():
            sum: float = 0
            alpha_pheromones: list[float] = []
            for boolean in value_options.keys():
                phero = value_options[boolean] ** alpha
                alpha_pheromones.append(phero)
                sum += phero
            
            return list(value_options.keys()), alpha_pheromones, float(sum)

        keys, alpha_pheromones, total_sum = adjustPheromones()

        # Pick a value using probabilities
        percentage = [round((pheromone / total_sum) * 100) for pheromone in alpha_pheromones]
        probabilities: list[bool] = []
        for key, repetitions in zip(keys, percentage):
            probabilities.extend([key] * repetitions)

        chosen_option = choice(probabilities)

        return chosen_option

class ACO:
    def __init__(self, file_path: str = 'path_to_sat_file', total_ants:int=500, n_offline_ants: int = 20):
        self.file_path: str             = file_path
        self.variables: set             = set()
        self.clauses: list[dict]        = []
        self.total_clauses_num: int     = 0
        self.graph: dict                = {}
        self.current_index: int         = 0
        self.ants_arr: list[Ant]        = []
        self.best_ant: Ant              = Ant(-1, 0, -1)

        self.total_ants: int            = total_ants
        self.n_offline_ants: int        = n_offline_ants

    def readSAT(self):
        # read and store the clauses and variables
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
            parameters = self.getParameters(ant)
            ant.performance = self.performance(ant)
            self.addPheromones(ant, offline_phase=True)
            
            self.ants_arr.append(ant)

            if ant.performance == self.total_clauses_num:
                return ant
        
        self.evaporate()

        # online search
        for _ in range(self.n_offline_ants, self.total_ants):
            ant = self.generateAnt()
            parameters = self.getParameters(ant)
            ant.performance = self.performance(ant)

            self.addPheromones(ant)
            self.evaporate()

            self.ants_arr.append(ant)

            if ant.performance == self.total_clauses_num:
                return ant
        
        return max(self.ants_arr, key=lambda ant: ant.performance)

    def addPheromones(self, ant: Ant, offline_phase: bool = False):
        # implements the pheromone disposition equation
        def pheromonesEquation(ant: Ant):
            performance = ant.performance / self.total_clauses_num
            performance_component = (performance ** 10) * 100

            stamp = (math.log10(ant.index+1))
            index_component = 1 * stamp
            if offline_phase:
                index_component = 1

            pheromones = (performance_component * index_component)
            
            if ant.performance > self.best_ant.performance: 
                pheromones += 5

            return pheromones

        add_pheromones = pheromonesEquation(ant)
        for v in self.variables:
            chosen_param = ant.parameters[v]
            self.graph[v][chosen_param] += add_pheromones

    def evaporate(self):
        # Decreasingly removes a percentage of the pheromones in all edges
        for v in self.variables:
            for option in self.graph[v].keys():
                evaporation_rate = 90 / 100
                new_pheromones = round(self.graph[v][option] * evaporation_rate, 2)
                self.graph[v][option] = max(10, new_pheromones)
        
    def generateAnt(self, alpha_zero: bool = False) -> Ant:
        if alpha_zero:
            # offline ants
            ant = Ant(self.current_index, 0)

        else:
            # rate that explorer/exploiter ants are generated
            rate = 10
            alpha_map: dict[int, float] = {mod:1 for mod in range(rate)}
            alpha_map[rate-1] = 0.6
            alpha_map[rate-2] = 1.2
            ant = Ant(self.current_index, alpha_map[self.current_index % rate])
        
        self.current_index += 1

        return ant

    def buildGraph(self):
        # initializes the graph with 10 pheromones at each edge
        min_phero = 10
        self.graph = {v: {True: min_phero, False: min_phero} for v in self.variables}

    def getParameters(self, ant: Ant):
        if ant.index % self.n_offline_ants == self.n_offline_ants - 1 and ant.alpha != 0:
            # re-lauches the global best ant
            ant.parameters = self.best_ant.parameters
            return ant.parameters

        # Generates a solution
        parameters = {}
        for v in self.variables:
            next_options = self.graph[v]
            chosen_option = ant.nextMove(next_options, ant.alpha)
            parameters[v] = chosen_option
        
        ant.parameters = parameters
        
        return parameters

    def performance(self, ant: Ant): # parameters = {0: True, 1: False}
        # Calculates the performance (# of sat clauses)
        count = 0
        for clause in self.clauses:
            for variable in clause.keys():
                var_state = ant.parameters[variable]
                if clause[variable] == -1:
                    var_state = not var_state

                if var_state:
                    count += 1
                    break
        
        if count > self.best_ant.performance: 
            self.best_ant = ant

        return count
    
if __name__ == "__main__":
    path_to_sat = 'max3sat_aco\examples\SAT3.txt'
    aco = ACO(path_to_sat)
    best_ant, time = aco.initialize()
    print(f'Performance: {best_ant.performance}')
    print(f'Time spent (s): {time}')