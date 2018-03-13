import random
class Chromosome:
    import numpy as np
    CITIES_COUNT = 312
    DISTANCE_MATRIX = np.zeros((CITIES_COUNT,CITIES_COUNT))

    def __init__(self, _path): #path is an array of integers from [0, 312) denoting teh index of each city in the distance matrix
        self.path = _path
        self.set_fitness()
        self.rank = 0

    def set_fitness(self):
        _fit = 0

        # 0th city is fixed
        current_city = 0
        
        # calculate fitness using distance matrix
        for i in range(1, Chromosome.CITIES_COUNT):
            next_city = self.path[i]
            _fit += Chromosome.DISTANCE_MATRIX[current_city, next_city]
            current_city = next_city
            
        _fit += Chromosome.DISTANCE_MATRIX[current_city, 0]
        self.distance = _fit
        self.fitness = 1/self.distance

    def mutate(self, mutation_rate):
        if (random.uniform(0, 100) < mutation_rate):
            #   here we mutate by swapping two randomly chosen alleles
            gene_1 = int(random.uniform(1, 312))
            gene_2 = int(random.uniform(1, 312))
            self.path[gene_1], self.path[gene_2] = self.path[gene_2], self.path[gene_1]

            # if(gene_2 < gene_1):
            #     gene_2, gene_1 = gene_1, gene_2

            # x = self.path[gene_1:gene_2]
            # x.reverse()
            # self.path[gene_1:gene_2] = x

            self.set_fitness() #because we need to set fitness again
            # recursively call mutate
            self.mutate(mutation_rate)
        
    def two_opt_swap(self):
        s_path = self.path.copy()
        gene_1 = int(random.uniform(0, 311))
        gene_2 = int(random.uniform(0, 311))

        while(gene_2 == gene_1):
            gene_2 = int(random.uniform(1, 311))

        # swap occurs here
        
        _ = s_path[gene_1 + 1]
        s_path[gene_1+1] = s_path[gene_2+1]
        s_path[gene_2+1] = _

        successor_chrom = Chromosome(s_path)

        return successor_chrom



    def successor(self):
        s_path = self.path.copy()
        #   here we mutate by swapping two randomly chosen alleles
        gene_1 = int(random.uniform(1, 312))
        gene_2 = int(random.uniform(1, 312))

        if(gene_2 < gene_1):
            gene_2, gene_1 = gene_1, gene_2

        x = self.path[gene_1:gene_2]
        x.reverse()
        s_path[gene_1:gene_2] = x

        successor_chrom = Chromosome(s_path)
        successor_chrom.set_fitness()

        return successor_chrom

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness