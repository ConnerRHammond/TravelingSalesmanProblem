import heapq
import time
import copy

from TSPClasses import *
from State import *


class BranchAndBound:

    def __init__(self, bssf, cities):
        self.bssf = bssf
        self.cities = cities
        self.num_cities = len(cities)
        self.bssf_path = []

    # Technically the complexity of the full algorithm is O(n^2 * (n+1)!) because the number of states
    # created would be a total of (n+1)! and the work done at each state is O(n^2) but because of our aggressive
    # pruning it ends up being much less. It is difficult to say what the exact complexity is without doing a lot of empircal analysis.
    def solve(self, time_allowance):
        start_time = time.time()
        created_states = 1
        pruned = 0
        total_solutions = 0
        max_queue_size = 1

        initial_state = State(copy.deepcopy(
            self.initialize_reduced_cost_matrix(self.cities)), 0, [0])
        PQ = [initial_state]
        heapq.heapify(PQ)

        while len(PQ) > 0 and time.time() - start_time < time_allowance: # if time runs out our current bssf is returned
            state = heapq.heappop(PQ)
            current_city = state.visited_cities[-1]
            if state.lower_bound >= self.bssf:
                pruned += 1
                continue
            else:
                for j in range(len(state.reduced_cost_matrix)):
                    if j in state.visited_cities:
                        continue
                    else:
                        new_state = copy.deepcopy(state)
                        new_state.visited_cities.append(j)
                        new_state.reduce(current_city, j)
                        created_states += 1
                        if self.is_solution(new_state):
                            self.bssf = new_state.lower_bound
                            self.bssf_path = copy.deepcopy(
                                new_state.visited_cities)
                            total_solutions += 1
                        elif new_state.lower_bound < self.bssf: # This statement will prune states that should never be visited because they are already over our bssf
                            heapq.heappush(PQ, new_state)
                        else:
                            pruned += 1
                        max_queue_size = max(max_queue_size, len(PQ))

        # Prune the states that were never visited
        if not len(PQ) <= 0:
            pruned += len(PQ)

        results = {}
        results['cost'] = self.bssf
        results['time'] = time.time() - start_time
        results['count'] = total_solutions
        results['soln'] = self.create_tsp_solution(self.bssf_path)
        results['max'] = max_queue_size
        results['total'] = created_states
        results['pruned'] = pruned
        return results

    # A solution has been found if every city has been visited
    def is_solution(self, state):
        if len(state.visited_cities) == self.num_cities:
            return True
        else:
            return False

    # Create a TSPSolution object based on the given bssf_path
    def create_tsp_solution(self, bssf_path):
        tsp_solution = []
        for i in range(len(bssf_path)):
            tsp_solution.append(self.cities[bssf_path[i]])
        return TSPSolution(tsp_solution)

    # Initialize the reduced cost matrix with the distance between each city
    def initialize_reduced_cost_matrix(self, initial_cities):
        reduced_cost_matrix = [[float("inf") for i in range(
            self.num_cities)] for j in range(self.num_cities)]
        for i in range(len(initial_cities)):
            for j in range(len(initial_cities)):
                if i == j:
                    continue
                else:
                    reduced_cost_matrix[i][j] = initial_cities[i].costTo(
                        initial_cities[j])
        return reduced_cost_matrix
