from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine # dataset search wine dataset 3 classes wine 1, wine 2 and wine 3
from random import choice, randint

class Individual:
    def __init__(self, chromosome=None, index=0):
        self.chromosome = chromosome
        self.index      = index
        self.fitness    = 0
    
    def toString(self):
        string = 'ind '+ str(self.index) + ' ->' + ' Chromosome: ' + str(self.chromosome) + '\n'
        string += ' Fitness: ' + str(self.fitness)

        return string
    
class KNNGeneticAlgorithm:
    def __init__(self,
                 x_train,
                 x_test,
                 y_train,
                 y_test,
                 max_generation=10, # 10*10 = 100
                 population_size=10,
                 mutation_rate=10 # percentage 10%
                 ):
        self.x_train            = x_train
        self.x_test             = x_test
        self.y_train            = y_train
        self.y_test             = y_test

        self.means              = [] # ill explain later

        self.max_generation     = max_generation
        self.population_size    = population_size
        self.mutation_rate      = mutation_rate

        self.best_individual    = Individual()
        self.chromosome_shape   = [
            range(3, 30),                       # index 0 -> n_neighbors
            ['uniform', 'distance'],            # index 1 -> weights
            [                                   # index 2 -> metric
                'minkowski',    
                'euclidean', 'chebyshev', 
                'jaccard', 'cosine', 
                'manhattan'
            ]   
        ]

    def generateIndividual(self, index):
        chromosome = []
        chromosome.append( choice(self.chromosome_shape[0]) )
        chromosome.append( choice(self.chromosome_shape[1]) )
        chromosome.append( choice(self.chromosome_shape[2]) )
        
        return Individual(chromosome, index)
    
    def generatePopulation(self):
        population = []
        for i in range(self.population_size):
            population.append( self.generateIndividual(i) )
        
        return population

    def fitness(self, individual): # accuracy as fitness
        n = individual.chromosome[0]
        weight = individual.chromosome[1]
        metric = individual.chromosome[2]

        # building the model and training
        knn = KNeighborsClassifier(n_neighbors=n, weights=weight, metric=metric)
        knn.fit(self.x_train, self.y_train)

        # getting the predictions and accuracy (or fitness)
        predictions = knn.predict(self.x_test)
        accuracy = accuracy_score(self.y_test, predictions)

        # in this case the fitness will be the same as the accuracy score
        fitness = accuracy

        if self.best_individual.fitness < fitness:
            self.best_individual = individual
        
        return fitness

    def populationFitness(self, population) -> None:
        for i in range(len(population)):
            population[i].fitness = self.fitness(population[i]) # list of Individuals

    def selection(self, population):
        parents = []

        for _ in range(2): 
            contestant1 = choice(population) # list of Individuals
            contestant2 = choice(population)

            parent = contestant1
            if contestant2.fitness > contestant1.fitness:
                parent = contestant2
            parents.append(parent)
        
        return parents[0], parents[1]
    
    def crossover(self, parent1, parent2, index):
        partition = randint(1, len(parent1.chromosome)-1)

        chromosome1 = parent1.chromosome[:partition] + parent2.chromosome[partition:]
        chromosome2 = parent2.chromosome[:partition] + parent1.chromosome[partition:]

        child1 = Individual(chromosome1, index)
        child2 = Individual(chromosome2, (index + 1))

        return child1, child2

    def mutation(self, child) -> None:
        new_chromosome = child.chromosome

        for i in range(len(child.chromosome)):
            if randint(1, 100) <= self.mutation_rate: # 100 possibilities | 1, 2, 3, ..., 10
                new_chromosome[i] = choice(self.chromosome_shape[i])
            
        child.chromosome = new_chromosome

    def initialize(self):
        population = self.generatePopulation() # generation zero
        self.populationFitness(population)
        self.writeGeneration(population)

        for generation_index in range(1, self.max_generation):
            new_population = []
            for index in range(0, self.population_size, 2): # index -> 0, 2, 4, 6, 8
                parent1, parent2 = self.selection(population)
                child1, child2 = self.crossover(parent1, parent2, index)
                self.mutation(child1)
                self.mutation(child2)

                new_population.append(child1)
                new_population.append(child2)
            
            self.populationFitness(new_population)
            self.writeGeneration(new_population, generation_index)
            population = new_population

        self.writeBest()

    def writeGeneration(self, population, index=0) -> None:
        # save the accuracy means
        population_mean = 0
        for i in range(len(population)):
            # adding to calculate the mean
            population_mean += population[i].fitness

        population_mean = population_mean / len(population)
        self.means.append(population_mean)

        self.file_name = "KNN_GA.txt"

        # write to file
        if index == 0:
            with open(self.file_name, "w") as out:
                out.write("")
                out.close()  

        with open(self.file_name, "a") as out:
            out.write("\n========================== Generation " + str(index) + " ==========================")
            for i in range(len(population)):
                out.write("\n" + population[i].toString())
            out.write("\n-------------------------- Accuracy Mean --------------------------")
            out.write("\n Acc: " + str(population_mean))
            out.close()

    def writeBest(self):   
        with open(self.file_name, "a") as out:
            out.write("\n-------------------------- Best Individual --------------------------")
            out.write("\n" + str(self.best_individual.toString()))
            out.write("\n-------------------------- Generetion Means --------------------------")
            out.write("\n" + str(self.means))
            out.close()  

# loading dataset
df = load_wine()

# splitting data (train test split)
x_train, x_test, y_train, y_test = train_test_split(df.data, df.target, test_size=0.3, random_state=42)

ga = KNNGeneticAlgorithm(x_train, x_test, y_train, y_test)
ga.initialize()