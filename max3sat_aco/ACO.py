'''clausulas = [
    {0:1, 1:1},
    {0:1, 1:-1},
    {0:-1, 1:1},
    {0:-1, 1:-1}
]'''

import os
import time
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
        self.variables: list            = []
        self.clauses: list[dict]        = []
        self.total_clauses_num: int     = 0
        self.graph: dict                = {}
        self.current_index: int         = 0
        self.ants_arr: list[Ant]        = []

    def readSAT(self):
        self.variables = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49']
        self.clauses = [
            {'x0': 1, 'x1': -1, 'x2': 1},
            {'x1': 1, 'x3': -1, 'x4': 1},
            {'x2': -1, 'x5': 1, 'x6': -1},
            {'x3': 1, 'x7': -1, 'x8': 1},
            {'x4': 1, 'x9': -1, 'x10': 1},
            {'x5': -1, 'x11': 1, 'x12': -1},
            {'x6': 1, 'x13': -1, 'x14': 1},
            {'x7': -1, 'x15': 1, 'x16': -1},
            {'x8': 1, 'x17': -1, 'x18': 1},
            {'x9': -1, 'x19': 1, 'x20': -1},
            {'x10': 1, 'x21': -1, 'x22': 1},
            {'x11': -1, 'x23': 1, 'x24': -1},
            {'x12': 1, 'x25': -1, 'x26': 1},
            {'x13': -1, 'x27': 1, 'x28': -1},
            {'x14': 1, 'x29': -1, 'x30': 1},
            {'x15': -1, 'x31': 1, 'x32': -1},
            {'x16': 1, 'x33': -1, 'x34': 1},
            {'x17': -1, 'x35': 1, 'x36': -1},
            {'x18': 1, 'x37': -1, 'x38': 1},
            {'x19': -1, 'x39': 1, 'x40': -1},
            {'x20': 1, 'x41': -1, 'x42': 1},
            {'x21': -1, 'x43': 1, 'x44': -1},
            {'x22': 1, 'x45': -1, 'x46': 1},
            {'x23': -1, 'x47': 1, 'x48': -1},
            {'x24': 1, 'x49': -1, 'x0': 1},
            {'x25': -1, 'x1': 1, 'x2': -1},
            {'x26': 1, 'x3': -1, 'x4': 1},
            {'x27': -1, 'x5': 1, 'x6': -1},
            {'x28': 1, 'x7': -1, 'x8': 1},
            {'x29': -1, 'x9': 1, 'x10': -1},
            {'x30': 1, 'x11': -1, 'x12': 1},
            {'x31': -1, 'x13': 1, 'x14': -1},
            {'x32': 1, 'x15': -1, 'x16': 1},
            {'x33': -1, 'x17': 1, 'x18': -1},
            {'x34': 1, 'x19': -1, 'x20': 1},
            {'x35': -1, 'x21': 1, 'x22': -1},
            {'x36': 1, 'x23': -1, 'x24': 1},
            {'x37': -1, 'x25': 1, 'x26': -1},
            {'x38': 1, 'x27': -1, 'x28': 1},
            {'x39': -1, 'x29': 1, 'x30': -1},
            {'x40': 1, 'x31': -1, 'x32': 1},
            {'x41': -1, 'x33': 1, 'x34': -1},
            {'x42': 1, 'x35': -1, 'x36': 1},
            {'x43': -1, 'x37': 1, 'x38': -1},
            {'x44': 1, 'x39': -1, 'x40': 1},
            {'x45': -1, 'x41': 1, 'x42': -1},
            {'x46': 1, 'x43': -1, 'x44': 1},
            {'x47': -1, 'x45': 1, 'x46': -1},
            {'x48': 1, 'x47': -1, 'x49': 1},
            {'x49': -1, 'x0': 1, 'x1': -1},
            {'x0': 1, 'x2': 1, 'x3': -1},
            {'x1': -1, 'x4': 1, 'x5': -1},
            {'x2': 1, 'x6': -1, 'x7': 1},
            {'x3': -1, 'x8': 1, 'x9': -1},
            {'x4': 1, 'x10': -1, 'x11': 1},
            {'x5': -1, 'x12': 1, 'x13': -1},
            {'x6': 1, 'x14': -1, 'x15': 1},
            {'x7': -1, 'x16': 1, 'x17': -1},
            {'x8': 1, 'x18': -1, 'x19': 1},
            {'x9': -1, 'x20': 1, 'x21': -1},
            {'x10': 1, 'x22': -1, 'x23': 1},
            {'x11': -1, 'x24': 1, 'x25': -1},
            {'x12': 1, 'x26': -1, 'x27': 1},
            {'x13': -1, 'x28': 1, 'x29': -1},
            {'x14': 1, 'x30': -1, 'x31': 1},
            {'x15': -1, 'x32': 1, 'x33': -1},
            {'x16': 1, 'x34': -1, 'x35': 1},
            {'x17': -1, 'x36': 1, 'x37': -1},
            {'x18': 1, 'x38': -1, 'x39': 1},
            {'x19': -1, 'x40': 1, 'x41': -1},
            {'x20': 1, 'x42': -1, 'x43': 1},
            {'x21': -1, 'x44': 1, 'x45': -1},
            {'x22': 1, 'x46': -1, 'x47': 1},
            {'x23': -1, 'x48': 1, 'x49': -1},
            {'x24': 1, 'x0': -1, 'x1': 1},
            {'x25': -1, 'x2': -1, 'x3': 1},
            {'x26': 1, 'x4': 1, 'x5': -1},
            {'x27': -1, 'x6': 1, 'x7': -1},
            {'x28': 1, 'x8': -1, 'x9': 1},
            {'x29': -1, 'x10': 1, 'x11': -1},
            {'x30': 1, 'x12': -1, 'x13': 1},
            {'x31': -1, 'x14': 1, 'x15': -1},
            {'x32': 1, 'x16': -1, 'x17': 1},
            {'x33': -1, 'x18': 1, 'x19': -1},
            {'x34': 1, 'x20': -1, 'x21': 1},
            {'x35': -1, 'x22': 1, 'x23': -1},
            {'x36': 1, 'x24': -1, 'x25': 1},
            {'x37': -1, 'x26': 1, 'x27': -1},
            {'x38': 1, 'x28': -1, 'x29': 1},
            {'x39': -1, 'x30': 1, 'x31': -1},
            {'x40': 1, 'x32': -1, 'x33': 1},
            {'x41': -1, 'x34': 1, 'x35': -1},
            {'x42': 1, 'x36': -1, 'x37': 1},
            {'x43': -1, 'x38': 1, 'x39': -1},
            {'x44': 1, 'x40': -1, 'x41': 1},
            {'x45': -1, 'x42': 1, 'x43': -1},
            {'x46': 1, 'x44': -1, 'x45': 1},
            {'x47': -1, 'x46': 1, 'x47': -1},
            {'x48': 1, 'x49': -1, 'x0': 1}
        ]
        self.total_clauses_num = len(self.clauses)

    def initialize(self):
        self.readSAT()
        self.buildGraph()

        start = time.perf_counter()
        ant = self.colonize()
        end = time.perf_counter()

        return ant, (end-start)

    def colonize(self, n_offline_ants = 50, total_ants = 500):
        # offline search
        for _ in range(n_offline_ants):
            ant = self.generateAnt(True)
            parameters = ant.getParameters(self.graph, self.variables)
            ant.performance = self.performance(parameters)
            self.addPheromones(ant)
            self.evaporate()

            self.ants_arr.append(ant)

            if ant.performance == self.total_clauses_num:
                return ant
        
        # online search
        for _ in range(n_offline_ants, total_ants):
            ant = self.generateAnt()
            parameters = ant.getParameters(self.graph, self.variables)
            ant.performance = self.performance(parameters)

            self.addPheromones(ant)
            self.evaporate()

            self.ants_arr.append(ant)

            if ant.performance == self.total_clauses_num:
                return ant
        
        return max(self.ants_arr, key=lambda ant: ant.performance)

    def addPheromones(self, ant: Ant):
        def pheromonesEquation(performance):
            return performance * 2

        add_pheromones = pheromonesEquation(ant.performance)
        for v in self.variables:
            chosen_param = ant.parameters[v]
            self.graph[v][chosen_param] += add_pheromones

    def evaporate(self):
        for v in self.variables:
            for option in self.graph[v].keys():
                self.graph[v][option] = max(1, self.graph[v][option] * (90/100))
        
    def generateAnt(self, alpha_zero: bool = False) -> Ant:
        if alpha_zero or self.current_index % 10 == 0:
            ant = Ant(self.current_index, 0)

        else:
            alpha_map: dict[int, float] = {0: 1.2, 1: 1, 2: 0.8}
            ant = Ant(self.current_index, alpha_map[self.current_index % 3])
        
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