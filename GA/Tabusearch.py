import numpy as np
import random
import time

class TabuSearch:
    def __init__(self, tabu_size, max_iterations, N, m, M, fields):
        self.tabu_size = tabu_size
        self.max_iterations = max_iterations
        self.N = N
        self.m = m
        self.M = M
        self.fields = fields

    def decode(self, individual):
        return individual

    def encode(self, solution):
        return solution

    def fitness_function(self, solution):
        daily_harvest = {}
        total_harvest = 0

        for i in range(self.N):
            day = solution[i]
            if day not in daily_harvest:
                daily_harvest[day] = 0
            daily_harvest[day] += self.fields[i][0]
            total_harvest += self.fields[i][0]

        for harvest in daily_harvest.values():
            if harvest < self.m or harvest > self.M:
                return 0,

        return total_harvest,

    def get_valid_neighbors(self, solution):
        neighbors = []
        for i in range(self.N):
            for day in range(self.fields[i][1], self.fields[i][2] + 1):
                if day != solution[i]:
                    neighbor = solution.copy()
                    neighbor[i] = day

                    # Check if the neighbor is valid
                    if self.is_valid_neighbor(neighbor):
                        neighbors.append(neighbor)
        return neighbors

    def is_valid_neighbor(self, neighbor):
        daily_harvest = {}
        for i in range(self.N):
            day = neighbor[i]
            if day not in daily_harvest:
                daily_harvest[day] = 0
            daily_harvest[day] += self.fields[i][0]

        for harvest in daily_harvest.values():
            if harvest < self.m or harvest > self.M:
                return False
        return True

    def tabu_search(self, initial_solution):
        current_solution = initial_solution
        best_solution = initial_solution
        tabu_list = []
        tabu_list.append(current_solution.copy())
        current_fitness = self.fitness_function(current_solution)[0]
        best_fitness = current_fitness

        for _ in range(self.max_iterations):
            neighbors = self.get_valid_neighbors(current_solution)
            next_solution = None
            next_fitness = -1

            for neighbor in neighbors:
                if neighbor not in tabu_list:
                    neighbor_fitness = self.fitness_function(neighbor)[0]
                    if neighbor_fitness > next_fitness:
                        next_solution = neighbor
                        next_fitness = neighbor_fitness

            if next_fitness <= current_fitness:
                break

            current_solution = next_solution
            current_fitness = next_fitness

            if current_fitness > best_fitness:
                best_solution = current_solution
                best_fitness = current_fitness

            tabu_list.append(next_solution.copy())
            if len(tabu_list) > self.tabu_size:
                tabu_list.pop(0)

        return best_solution

def read_input(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    lines = data.split('\n')
    n, m, M = map(int, lines[0].split())
    fields = []
    for line in lines[1:]:
        if line.strip():
            d, s, e = map(int, line.split())
            fields.append((d, s, e))
    return n, m, M, fields

def check(i, sum, day, mark, d, s, e, M):
    if mark[i] != 0:
        return False
    if sum > M:
        return False
    if day < s[i] or day > e[i]:
        return False
    return True

def greedy(n, m, M, d, s, e):
    max_day = 0
    mark = [0] * (n + 1)

    for i in range(1, n + 1):
        max_day = max(max_day, e[i])

    # Giai đoạn 1: Đảm bảo sản lượng hàng ngày đạt ít nhất m
    for day in range(1, max_day + 1):
        sum = 0
        tmp = []
        for i in range(1, n + 1):
            if check(i, sum + d[i], day, mark, d, s, e, M) and sum < m:
                mark[i] = day
                sum += d[i]
                tmp.append(i)
        if sum < m:
            for i in tmp:
                mark[i] = 0

    # Giai đoạn 2: Tăng sản lượng hàng ngày nếu có thể
    for day in range(1, max_day + 1):
        sum = 0
        for i in range(1, n + 1):
            if mark[i] == day:
                sum += d[i]

        for i in range(1, n + 1):
            if check(i, sum + d[i], day, mark, d, s, e, M) and mark[i] == 0:
                mark[i] = day
                sum += d[i]

    solution = [mark[i] for i in range(1, n + 1)]
    return solution

# Example usage
N, m, M, fields = read_input(r'D:\school\TULKH\Planning-Optimization\Test\test100_100.inp')
d = [0] * (N + 1)
s = [0] * (N + 1)
e = [0] * (N + 1)

for i in range(N):
    d[i + 1], s[i + 1], e[i + 1] = fields[i]

initial_solution = greedy(N, m, M, d, s, e)
tabu_search = TabuSearch(tabu_size=10, max_iterations=1000, N=N, m=m, M=M, fields=fields)
best_solution = tabu_search.tabu_search(initial_solution)
best_fitness = tabu_search.fitness_function(best_solution)[0]

print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
