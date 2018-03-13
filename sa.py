from chromosome import Chromosome
import numpy as np
from ga import read_file
import random
import math
CITIES_COUNT = 312
INITIAL_TEMP = 10000



def schedule(t):
    global INITIAL_TEMP
    return INITIAL_TEMP - t

def make_node():
    path = list(range(0, 312))
    _buff = list(range(1, 312))
    random.shuffle(_buff)
    path[1:] = _buff
    return Chromosome(path)

def simmulated_annealing():
    # make initial randomly generated node
    init = make_node()
    
    current = init
    for t in range(1, 10000000):
        T = schedule(t)
        if T == 0: break
        next = current.two_opt_swap()

        
        # subtracting the objective functions for both the nodes
        delta_e = (next.fitness) - (current.fitness)
    

        if (delta_e > 0):
            current = next
        else :
            prob = math.exp(-1000000 / T)
            print("Probability of down step: ", prob)

            if random.uniform(0, 1) < prob:
                current = next

        print("DELTA_E: ", delta_e)
        print("T: ", T)
        print("CURRENT DISTANCE: ", current.distance)

        # input("WAIT FOR USER INPUT")

    print("Initial Dist: ", init.distance)
    print("Final Dist: ", current.distance)


def main():
    distance_matrix = np.zeros((CITIES_COUNT, CITIES_COUNT))

    # reading distances from our file
    file_path = "/Users/noorahmed/Desktop/sem6/AI/Assignments/A2/src/dataset/usca312_dist.txt"
    read_file(file_path, distance_matrix)
    Chromosome.DISTANCE_MATRIX = distance_matrix

    simmulated_annealing()


if __name__ == "__main__":
    main()