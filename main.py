import math
import random
import matplotlib.pyplot as plt

''' 
i know i shouldve used some structure like object but i thought it wont be a problem if i 
just keep the index same for everything. it did work but added some unnecessary complexities.
'''

candidates = []
num_cities = 50
random_nums = list(range(0,num_cities))

num_candidates = 500

for x in range(num_candidates):
    random.shuffle(random_nums)
    candidates.append(random_nums[:])

def cities(num_cities):
    city_location = []
    for i in range(num_cities):
        x = (random.randint(0,255), random.randint(0,255))
        city_location.append(x)
    return city_location

def distance(candidates, city_location):
    distances = []
    for j in range(num_candidates):
        distance_each_candidate = 0
        for i in range(num_cities-1):
            point_a = city_location[candidates[j][i]]
            point_b = city_location[candidates[j][i+1]]
            distance_each_city = math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)
            distance_each_candidate += distance_each_city

        #returning to the first city
        point_a = city_location[candidates[j][num_cities-1]]
        point_b = city_location[candidates[j][0]]
        distance_last_to_first = math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)
        distance_each_candidate += distance_last_to_first
        
        distances.append(distance_each_candidate)
        
    return distances


def fitness(distances):
    return [1/d**4 for d in distances]

num_survivors = int(math.ceil(num_candidates * 0.4))

#less exploration because of roulette
def selection(candidates, distances, num_survivors):
    survivors = []
    
    fitness_scores = fitness(distances)
    total_fitness = sum(fitness_scores)

    cumulative_sum = []
    running_sum = 0
    for x in range(len(fitness_scores)):
        running_sum += fitness_scores[x]
        cumulative_sum.append(running_sum)

    for x in range(num_survivors):
        dart = random.uniform(0, total_fitness)
        for i, v in enumerate(cumulative_sum):
            if dart<cumulative_sum[i]:
                survivors.append(candidates[i])
                break
    return survivors

#less exploration due to custom PMX but more due to one child per pair of parents
def crossover(survivors):
    next_gen = survivors[:]

    while(len(next_gen)<num_candidates):
        cut_1 = random.randint(0, num_cities-1)
        cut_2 = random.randint(0, num_cities-1)
        if cut_1>cut_2:
            cut_1, cut_2 = cut_2, cut_1
    
        parent_1, parent_2 = random.sample(survivors, 2)
        child = [None]*num_cities
        child[cut_1:cut_2] = parent_1[cut_1:cut_2]
    
        taken = parent_1[cut_1:cut_2]
    
        indices = list(range(0, cut_1)) + list(range(cut_2, len(child)))
        i = 0
        for x in parent_2:
            if x not in taken:
                child[indices[i]] = x
                i+=1
    
        next_gen.append(child)

    return next_gen


def mutation(next_gen):
    for i in range(num_candidates):
        for j in range(num_cities):
            mutate = random.randint(1,1000)
            if mutate>999:
                k = random.randint(0,num_cities-1)
                next_gen[i][j], next_gen[i][k] = next_gen[i][k], next_gen[i][j]
    return next_gen

num_generation = 500
best_distance_each_gen = []
avg_distance_each_gen = []

city_location = cities(num_cities)

for x in range(num_generation):
    distances = distance(candidates, city_location)
    best_distance_each_gen.append(min(distances))
    avg_distance_each_gen.append(sum(distances)/num_candidates)
    survivors = selection(candidates, distances, num_survivors)
    next_gen = crossover(survivors)
    candidates = mutation(next_gen)

best_route_idx = distances.index(min(distances))
best_route = candidates[best_route_idx]

print("best path-> ", best_route)

# plt.plot(best_distance_each_gen, label='Best')
# plt.plot(avg_distance_each_gen, label='Average')
# plt.xlabel('Generation')
# plt.ylabel('Fitness')
# plt.legend()
# plt.show()