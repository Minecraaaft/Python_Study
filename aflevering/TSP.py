"""
Created on Wed Mar 3 16:39:18 2021
@author: Sila
"""

# Gettting started methods for TSP GA algorithm
# - Read cities from file
#

import pandas as pd
import random
import math

data = pd.read_csv('TSPcities1000.txt',sep='\s+',header=None)
data = pd.DataFrame(data)

import matplotlib.pyplot as plt
x = data[1]
y = data[2]
#plt.plot(x, y,'r.')
#plt.show()

def createRandomRoute():
    tour = [[i] for i in range(num_of_cities)]
    random.shuffle(tour)
    return tour

# plot the tour - Adjust range 0..len, if you want to plot only a part of the tour.
def plotCityRoute(route):
    for i in range(0, len(route) - 1):
        plt.plot(x[route[i][0]:route[i + 1][0]], y[route[i][0]:route[i + 1][0]], 'ro-')
    plt.show()

def totalDistance():
    distance = []
    for i in range(len(initRoutes) - 1):
        route = initRoutes[i]
        total = 0
        for j in range(0, len(route) - 1):
            total += distancebetweenCities(x[route[j][0]], y[route[j][0]], x[route[j+1][0]], y[route[j+1][0]])
        distance.append([total, route])
    return distance

# calculate distance between cities
def distancebetweenCities(city1x, city1y, city2x, city2y):
    xDistance = abs(city1x-city2x)
    yDistance = abs(city1y-city2y)
    distance = math.sqrt((xDistance * xDistance) + (yDistance * yDistance))
    return distance

def sortDistance(array):
    return sorted(array, key=lambda d: d[0])

#--- stats
num_start_routes = 1000
num_of_cities = 10
numOfGenerations = 100
k_mut_prob = 0.3


#----

initRoutes = []
for i in range(0, num_start_routes):
    initRoutes.append(createRandomRoute())

routes = []

routesWithDistance = sortDistance(totalDistance())


def makeBabies(breeders):
    newBreeders = []
    for i in range(0, len(breeders) - 1):
        parent1 = breeders[i][1]
        parent2 = breeders[i + 1][1]
        child = parent1[:len(parent1) // 2]

        i = 0
        while len(child) < len(parent2):
            if parent2[i] not in child:
                child.append(parent2[i])
            i += 1

        newBreeders.append(child)
        sortDistance(newBreeders)

    return newBreeders

def mutate(route_to_mut):
    if random.random() < k_mut_prob:

        # two random indices:
        mut_pos1 = random.randint(0, len(route_to_mut[1]) - 1)
        mut_pos2 = random.randint(0, len(route_to_mut[1]) - 1)

        # if they're the same, skip to the chase
        if mut_pos1 == mut_pos2:
            return route_to_mut

        # Otherwise swap them:
        city1 = route_to_mut[1][mut_pos1]
        city2 = route_to_mut[1][mut_pos2]

        route_to_mut[1][mut_pos2] = city1
        route_to_mut[1][mut_pos1] = city2


half = len(routesWithDistance) // 2
breeders = routesWithDistance[:half]
while (len(breeders) > 3):
    half = len(breeders) // 2
    breeders = breeders[:half]

    for i in breeders:
        mutate(i)

    makeBabies(breeders)

print(breeders[0])
plotCityRoute(breeders[0][1])



# calculate distance between cities


# distance between city number 100 and city number 105
dist= distancebetweenCities(x[100], y[100], x[105], y[105])
#print('Distance, % target: ', dist)

best_score_progress = []  # Tracks progress

fitness_gen0 = 1000 # replace with your value
#print('Starting best score, % target: ', fitness_gen0)

best_score = fitness_gen0
# Add starting best score to progress tracker
best_score_progress.append(best_score)

# Here comes your GA program...
best_score = 980
best_score_progress.append(best_score)
best_score = 960
best_score_progress.append(best_score)


# GA has completed required generation
#print('End best score, % target: ', best_score)

# plt.plot(best_score_progress)
# plt.xlabel('Generation')
# plt.ylabel('Best Fitness - route length - in Generation')
# plt.show()
