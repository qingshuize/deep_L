#coding:utf8
##使用deap遗传算法解决背包问题


import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

IND_INIT_SIZE = 6 # 基因编码位数
MAX_ITEM = 6
MAX_WEIGHT = 80
NBR_ITEMS = 6

random.seed(64)


items={
    0: [10, 15],
    1: [15, 25],
    2: [20, 35],
    3: [25, 45],
    4: [30, 55],
    5: [35, 70]}
# for i in range(NBR_ITEMS):
#     items[i] = (random.randint(1, 10), random.uniform(0, 100))

creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", set, fitness=creator.Fitness)

toolbox = base.Toolbox()

toolbox.register("attr_item", random.randrange, NBR_ITEMS)

toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_item, IND_INIT_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += items[item][0]
        value += items[item][1]
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return 10000, 0  # Ensure overweighted bags are dominated
    return weight, value,


def cxSet(ind1, ind2):

    temp = set(ind1)  # Used in order to keep type
    ind1 &= ind2  # Intersection (inplace)
    ind2 ^= temp  # Symmetric Difference (inplace)
    return ind1, ind2


def mutSet(individual):

    if random.random() < 0.5:
        if len(individual) > 0:  # We cannot pop from an empty set
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,


toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", cxSet)
toolbox.register("mutate", mutSet)
toolbox.register("select", tools.selNSGA2)


def main():
    random.seed(64)
    NGEN = 100
    MU = 100
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof)

    return pop, stats, hof


if __name__ == "__main__":
    pop, stats, hof = main()
    print(u"最佳装包为(最佳个体) :"+str(hof[-1]))
    print(len(pop))
    print(len(hof))
    print(u"最佳装包时的重量与价值(最佳适应度) :"+str(evalKnapsack(hof[-1])))