import numpy as np
from random import shuffle
import random
from chromosome import Chromosome
CITIES_COUNT = 312

#====================================== HEPER FUNCTIONS
def read_file(_fn, arr):
    with open(_fn, 'r') as f:
        count = 0
        
        i = 0
        j = 0
        for line in f:
            distances = line.split()
            if count == 32: 
                count = 0
                i += 1
                j = 0
            for dist in distances:
                arr[i, j] = int(dist)
                j += 1
                
            count+=1


def print_max_fitness(current_population):
    max = current_population[0].fitness
    j = 0
    for i in range(1,len(current_population)):
        if (max < current_population[i].fitness):
            max = current_population[i].fitness
            j = i
    print("Fittest chromosome in this generation: ",max)
    print("Fittest tour lenght in this generation: ", current_population[j].distance)

#====================================== INITIALIZER FUNCTIONS
def init_population(distance_matrix, N):
    pop = []
    path = list(range(312))
    _buff = list(range(1, 312))

    for _ in range(0, N):
        shuffle(_buff)
        path[1:] = _buff
        _c = Chromosome(path)
        pop.append(_c)
    
    return pop


#====================================== GENETIC ALGO SUB FUNCTIONS
def rank_population(current_population):
    # get total fitness
    t_fitness = 0.0
    for i in range(len(current_population)):
        t_fitness += current_population[i].fitness

    csum = 0
    for i in range(len(current_population)):
        current_population[i].rank = current_population[i].fitness / t_fitness
        current_population[i].rank = current_population[i].rank * 100
        csum += current_population[i].rank
        current_population[i].rank = csum

    return


def rank_selection(ranked_current_population):
    _rand = random.uniform(0, 100)
    i = 0
    while i in range(0, len(ranked_current_population)):
        if (_rand <= ranked_current_population[i].rank):
            break
        i+=1
    return ranked_current_population[i]
        
def select_bad_parent(ranked_current_population, N = 200):
    sorted_arr = ranked_current_population.copy()
    sorted_arr.sort()
    one_fifth = int(N/5)
    return sorted_arr[int(random.uniform(0, one_fifth-1))]


def select_parents(current_population):
    father = rank_selection(current_population)
    mother = father
    while (mother == father):
        if (random.uniform(0, 5) < 4):
            mother = rank_selection(current_population)
        else:
            mother = select_bad_parent(current_population, 200)
    return mother, father

# Partially mapped crossover is a two point crossover with a specific algroithm used below
def PMX(mother, father):
    crossover_1 = int(random.uniform(0, 312)) 
    crossover_2 = crossover_1
    while (crossover_2 == crossover_1):
        crossover_2 = int(random.uniform(0, 312))

    if not crossover_2 > crossover_1:
        buff = crossover_1
        crossover_1 = crossover_2 
        crossover_2 = buff


    # initializing empty chromosomes
    o1 = [-1 for i in range(312)]
    o2 = [-1 for i in range(312)]

    # this is arbitrarily chosen
    o1[crossover_1:crossover_2] = mother.path[crossover_1:crossover_2]
    o2[crossover_1:crossover_2] = father.path[crossover_1:crossover_2]

    cross_range = list(range(crossover_1, crossover_2))
    o1_index = 0
    o2_index = 0

    for alelle in father.path:
        if alelle not in o1 and o1_index not in cross_range:
            o1[o1_index] = alelle
        o1_index += 1

    for alelle in mother.path:
        if alelle not in o2 and o2_index not in cross_range:
            o2[o2_index] = alelle
        o2_index += 1

    new_alelle = 0
    for i in range(0, 312):
        if o1[i] == -1:
            while new_alelle in o1:
                new_alelle += 1
            o1[i] = new_alelle

    new_alelle = 0
    for i in range(0, 312):
        if o2[i] == -1:
            while new_alelle in o2:
                new_alelle += 1
            o2[i] = new_alelle

    return o1, o2

def crossover(mother, father):
    child_one_path, child_two_path = PMX(mother, father)
    child_one = Chromosome(child_one_path)
    child_two = Chromosome(child_two_path)

    return child_one, child_two


def get_fittest(current_population):
    max = current_population[0].fitness
    max_i = 0
    for i in range(1,len(current_population)):
        if (max < current_population[i].fitness):
            max = current_population[i].fitness
            max_i = i
    return current_population[i]


def BRAUN_update_population(current_population, children, N):
    current_population.extend(children)
    # sort by fitness
    current_population.sort()
    # in Brauns paper the update population is written as such
    # His algorithm chooses a fit chromosome 4 times more often than a bad Chromosome
    # He omits the criteria for a fit and unfit chromosome so i'm going to create my own
    # Im going to choose from the 4/5th part of the sorted array based off a value generated from a uniform dist
    # given that the value is less than 4
    new_pop = []
    pop_count = int(len(current_population))
    four_fifth = int(pop_count * (1/5))
    l = pop_count-1
    k = 0
    for i in range(0, N):
        _rand = int(random.uniform(0, 5))
        if (_rand < 4):
            new_pop.append(current_population[l])
            l -= 1
        else:
            new_pop.append(current_population[k])
            k+=1

    return new_pop


def update_population(current_population, children):
    current_population.extend(children)
    # sort by fitness
    current_population.sort()
    return current_population[int(len(current_population)/2):]


#====================================== ALGORITHM
def genetic_algorithm(distance_matrix):
    # N is the number of competitng chromosomes, max_generations is how many generation till end 
    # chromosome representation
    # Current population has 100 competing chromosomes
    N = 300
    generation = 0
    max_generation = 500
    mutation_rate = 10
    global CITIES_COUNT

    # create initial population
    current_population = init_population(distance_matrix, N)

    while (generation < max_generation):
        children = []

        rank_population(current_population)
        
        for i in range(0, int(N/2)):
            mother, father = select_parents(current_population)
            child_one, child_two = crossover(mother, father)
            
            child_one.mutate(mutation_rate)
            child_two.mutate(mutation_rate)

            children.append(child_one)
            children.append(child_two)
        

        # Russel and Norvig update. This may be done in order to preserve diversity in the population
        # current_population = update_population(current_population, children)
        
        current_population = update_population(current_population, children)

        generation += 1
        mutation_rate += 0.05

        print("\nGENERATION: ", generation)
        print_max_fitness(current_population)

        # input("WAIT FOR USER INPUT: ")


    return get_fittest(current_population)

def main():
    # initializing our 312 square matrix
    global CITIES_COUNT
    distance_matrix = np.zeros((CITIES_COUNT, CITIES_COUNT))

    # reading distances from our file
    file_path = "/Users/noorahmed/Desktop/sem6/AI/Assignments/A2/src/dataset/usca312_dist.txt"
    read_file(file_path, distance_matrix)
    Chromosome.DISTANCE_MATRIX = distance_matrix


    genetic_algorithm(distance_matrix)

    return 0

if __name__ == '__main__':
    main()
