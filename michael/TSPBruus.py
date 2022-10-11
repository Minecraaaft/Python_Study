"""
Created on Wed Mar 3 16:39:18 2021
@author: Sila
"""

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# --- Functions --------------------------------------------------------------------------------------------------------

# Plot Cities
def plotCities(cities):
    plt.title("Cities")
    plt.plot([coord["x"] for coord in cities.values()], [coord["y"] for coord in cities.values()], 'r.')
    plt.show()


# Returns array containing all city names in a randomized order.
def createRandomRoute(cities):
    route = list(cities.keys())
    random.shuffle(route)
    return route


# Plot the route
def plotCityRoute(route, cities, title=""):
    x = [cities[city]["x"] for city in route["waypoints"]]
    y = [cities[city]["y"] for city in route["waypoints"]]
    plt.plot(x, y, 'b-', label="Route")
    plt.plot(x, y, 'ro', label="City")
    plt.legend(loc="upper right")
    plt.title(title)
    plt.show()


# Returns combined distance of route legs
def routeDistance(waypoints, cities):
    d = 0
    for i in range(len(waypoints) - 1):
        coord1 = cities[waypoints[i]]
        coord2 = cities[waypoints[i + 1]]
        d += distancebetweenCities(coord1["x"], coord1["y"], coord2["x"], coord2["y"])
    return d


# Calculate distance between cities
def distancebetweenCities(city1x, city1y, city2x, city2y):
    xDistance = abs(city1x - city2x)
    yDistance = abs(city1y - city2y)
    # Use Pythagoras to calc distance between cities.
    distance = math.sqrt((xDistance * xDistance) + (yDistance * yDistance))
    return distance


# Finds and returns route with shortest distance
def filterShortestRoute(routes):
    result = routes[0]

    for i in range(1, len(routes)):
        if routes[i]["distance"] < result["distance"]:
            result = routes[i]

    return result


# Sort routes by ascending distance
def sortRoutesByDistance(routes):
    return sorted(routes, key=lambda route: route["distance"])


# Breeds children (routes) by gene-crossover.
def breedByCrossover(breeders):
    children = []

    # All breeders will mate at lest once!
    for b1 in range(len(breeders)):
        # --- Parent 1 ---
        parent1 = breeders[b1]
        # print("Parent 1: \n" + str(parent1))
        # Determine num of genes to crossover from parent1: min. 1, max. half.
        numOfGenes = random.randint(1, len(parent1["waypoints"]) // 2)
        # Determine starting gene index
        startIdx = random.randint(0, len(parent1["waypoints"]) - 1)
        # print("numOfGenes: " + str(numOfGenes) + " startGeneIndex: " + str(startIdx))

        # Transfer chosen parent1 genes to child
        child = []  # This array will hold our childs genes (waypoints)
        for i in range(startIdx, startIdx + numOfGenes):
            # Wrap index around if necessary
            idx = i % len(parent1["waypoints"])
            child.append(parent1["waypoints"][idx])
        # print("Child: " + str(child))

        # --- Parent 2 ---
        # Choose parent2 randomly among remaning breeders
        b2 = random.randint(0, len(breeders) - 2)  # Random index for breeder population - 1.
        b2 = (b2 + b1) % len(breeders) - 1  # Add b1 to b2 and wrap around with modulus or negative index.
        # print("b1: " + str(b1) + " b2: " + str(b2))
        parent2 = breeders[b2]

        # Grab missing genes (waypoints) from parent2
        while len(child) < len(parent2["waypoints"]):
            i = 0
            while parent2["waypoints"][i] in child:
                i += 1  # Child already has gene - inc and continue
            # print("Missing gene found: " + str(parent2["waypoints"][i]))
            child.append(parent2["waypoints"][i])

        distance = routeDistance(child, cities)
        children.append({"distance": distance, "waypoints": child})

    return children


def mutateRoutes(routes):
    for i in range(len(routes)):
        if random.random() <= mutationProbability:
            idx1 = random.randint(0, len(routes[i]["waypoints"]) - 1)
            idx2 = random.randint(0, len(routes[i]["waypoints"]) - 1)
            if idx1 != idx2:
                # Swap waypoints
                waypoint = routes[i]["waypoints"][idx1]
                routes[i]["waypoints"][idx1] = routes[i]["waypoints"][idx2]
                routes[i]["waypoints"][idx2] = waypoint
                distance = routeDistance(routes[i]["waypoints"], cities)
                routes[i]["distance"] = distance

    return routes


# --- Config -----------------------------------------------------------------------------------------------------------
num_of_routes = 100  # int. Starting population.
num_of_cities = 50  # int. How many cities to use from TSPcities1000.txt file. Max. 1000 (num of genes per route).
numOfGenerations = 100  # int. Value is limited to the factorial of num_of_routes.
mutationProbability = 0.15  # Double. Range: 0 - 1 (incl.)
# ----------------------------------------------------------------------------------------------------------------------

# --- Read cities from csv file ---
# File consists of 1000 entries
# Each entry has white space separated values
# Values: index x-coord y-coord
# Cooordinates are signed integers between -1000 and 1000.
data = pd.read_csv('TSPcities1000.txt', sep='\s+', header=None)
data = pd.DataFrame(data)[:num_of_cities]  # Limit num of cities

# Create dictionary of cities and their coordinates
# data: [0] = city number, [1] = x-coord, [2] = y-coord
cities = {"City_" + str(data[0][i]): {"x": data[1][i], "y": data[2][i]} for i in range(len(data))}
# plotCities(cities)

# --- Create intial routes and calc distance ---
# Create array of dictionaries holdng random city route and distance.
routes = []
for i in range(num_of_routes):
    route = createRandomRoute(cities)  # Returns array with random city names
    distance = routeDistance(route, cities)  # Returns int defning combined distance of route
    routes.append({"distance": distance, "waypoints": route})

# --- Generations ---
generationLimit = math.factorial(num_of_routes)
numOfGenerations = numOfGenerations if numOfGenerations < generationLimit else generationLimit

minDistanceProgress = []
shortestRoute = routes[0]

for i in range(numOfGenerations):
    # --- Evaluate ---
    routes = sortRoutesByDistance(routes)
    if routes[0]["distance"] < shortestRoute["distance"]:
        shortestRoute = routes[0]
        minDistanceProgress.append(shortestRoute["distance"])

    # --- Selection ---
    # Divide sorted population in half for breeding.
    breeders = routes[:len(routes) // 2]  # // = divide and floor result.

    # --- Croosover ---
    children = breedByCrossover(breeders)
    # Ensure we maintain population size
    if len(children) + len(breeders) < num_of_routes:
        # We are one population short
        # Add the next one from routes that we didn't include in breeders
        breeders.append(routes[len(breeders)])

    # Mutate offspring
    children = mutateRoutes(children)
    # Update population
    routes = breeders + children

    # print("Num of breeders: " + str(len(breeders)))
    # print("Num of children: " + str(len(children)))
    # print("Num of updated routes: " + str(len(routes)))


# --- Plot result ---
print("--- GA Completed ---")
print("Progress counter: " + str(len(minDistanceProgress)))
print("Shortes route:")
print(shortestRoute)

plotCityRoute(shortestRoute, cities, "Cities")

plt.plot(minDistanceProgress, "g-")
plt.title("TSP Genetic Algorithm")
plt.xlabel('Generation Progress')
plt.ylabel('Best Fitness - route length - in Generation')
plt.show()

