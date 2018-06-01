#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:15:43 2018

@author: hsnsd
"""
import random
import matplotlib.pyplot as plt

#Define problem
TSP = [[0,8,3,1,4,9,3,6],[8,0,5,10,11,4,3,6],[3,5,0,8,7,1,5,12],[1,10,8,0,9,11,6,4],[4,11,7,9,0,5,17,3],[9,4,1,11,5,0,4,1],[3,3,5,6,17,4,0,7],[6,6,12,4,3,1,7,0]]

#Generate random population of given size
def generatePopulation(size):
    population = set()
    A = [0,1,2,3,4,5,6,7]
    while len(population)!=10:
        random.shuffle(A)
        population.add(tuple(A))
    population = list(population)
    population = [(list(i),[getFitness(list(i))]) for i in population]
    return population

#Get fitness of a member of population
def getFitness(member):
    fitness=0
    for i in range(len(member) - 1):
        fitness+=TSP[member[i]][member[i+1]]
    return fitness


        
#Binary tournament in a population
def binaryTournament(population):
    parentA = population[random.randint(0,len(population[0]))]
    parentB = population[random.randint(0,len(population[0]))]
    
    if (parentA[1] < parentB[1]):
        return parentA
    
    return parentB

#Two point cross-over of two parents
def crossover(parentA, parentB):
    offsprings = []
    points = sorted(random.sample(range(8),2))
    offspringA =[None for i in range(len(parentA[0]))]
    offspringB =[None for i in range(len(parentA[0]))]
    
    for i in range(points[0],points[1]):
        offspringA[i] = parentA[0][i]
        offspringB[i] = parentB[0][i]
        

    tmpA = parentA[0][(points[1] - len(parentA[0])):]
    tmpA.extend((parentA[0][:points[1]]))
  
    tmpB = parentB[0][(points[1] - len(parentB[0])):]
    tmpB.extend((parentB[0][:points[1]]))

    tmpB = [x for x in tmpB if x not in offspringA]
    tmpA = [x for x in tmpA if x not in offspringB]

    tmpB.reverse()
    tmpA.reverse()
    

    
    
    for i in range(points[1] - len(parentA[0]), points[0]):
        offspringA[i] = tmpB.pop()
        offspringB[i] = tmpA.pop()
    
    offsprings.append(((offspringA), [getFitness(offspringA)]))
    offsprings.append(((offspringB), [getFitness(offspringB)]))
    
    

    return offsprings    

def generateOffsprings(population, size):
    offsprings = []
    count = 0
    while(count!=size/2):
        parentA = binaryTournament(population)
        parentB = binaryTournament(population)
        tmp = (crossover(parentA,parentB))
        for child in tmp:
            offsprings.append(child)
        count+=1
    return offsprings
    
    
#Mutation of an offspring
def mutation(offspring):
    points = sorted(random.sample(range(8),2))
    
    offspring[0][points[0]], offspring[0][points[1]] = offspring[0][points[1]] , offspring[0][points[0]]
    return offspring


def truncate(population):
    population = sorted(population, key=lambda x:x[1])
    population = population[:10]
    
    return population

def main():
    bestSoFar=[]
    averageSoFar=[]
    count = 0
    numOfGeneration = 100
    populationSize = 10
    population = generatePopulation(populationSize)

    while(count!=numOfGeneration):
        offsprings = generateOffsprings(population,populationSize)
        #print(offsprings)

        for i in range(len(offsprings)):
            if (random.random() >= 0.40):
                offsprings[i] = mutation(offsprings[i])
        population.extend(offsprings)
        population = truncate(population)
        bestSoFar.append(population[0][1][0])
        average = sum(x[1][0] for x in population)/float(len(population))
        averageSoFar.append(average)
        count+=1
    
    plt.plot(bestSoFar)
    plt.xlabel('X-th Generation')
    plt.ylabel('Fitness Value')
    plt.show()
    
    plt.plot(averageSoFar)
    plt.xlabel('X-th Generation')
    plt.ylabel('Average Fitness Value')
    plt.show()

            
main()
                
