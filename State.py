class State:

    # Initialize the state with the given matrix, lower bound, and visited cities
    def __init__(self, matrix, lower_bound, visited):
        self.num_cities = len(matrix)
        self.reduced_cost_matrix = matrix
        self.visited_cities = visited
        self.lower_bound = lower_bound

        self.reduce(None, None)

    # Sets the row and column you are visiting to infinity and adds the adds the intersection to the lower bound
    # Complexity is O(2n) because you loop through one row and one column
    def initialize_ignore(self, ignore_row, ignore_col):
        if ignore_row != None and ignore_col != None:
            self.lower_bound += self.reduced_cost_matrix[ignore_row][ignore_col]

        if ignore_row is None:
            ignore_row = -1
        else:
            for j in range(self.num_cities):
                self.reduced_cost_matrix[ignore_row][j] = float("inf")

        if ignore_col is None:
            ignore_col = -1
        else:
            for i in range(self.num_cities):
                self.reduced_cost_matrix[i][ignore_col] = float("inf")

    # Reduces the given matrix to the reduced cost matrix, visiting the city at the intersection of ignore_row and ignore_col
    # Complexity is O(n^2) becuase you visit each cell in the matrix (twice) but as it goes to infinity it is just O(n^2)
    def reduce(self, ignore_row, ignore_col):
        self.initialize_ignore(ignore_row, ignore_col)

        for i in range(len(self.reduced_cost_matrix)):
            if i == ignore_row:
                continue
            min = float("inf")
            for j in range(len(self.reduced_cost_matrix)): # find the min value in the row
                if j == ignore_col:
                    continue
                if self.reduced_cost_matrix[i][j] < min:
                    min = self.reduced_cost_matrix[i][j]

            if min == float("inf"):
                continue
            for j in range(len(self.reduced_cost_matrix)): # reduce the row based on the found min
                if j == ignore_col:
                    continue
                self.reduced_cost_matrix[i][j] -= min

            self.lower_bound += min

        for j in range(len(self.reduced_cost_matrix)):
            if j == ignore_col:
                continue
            min = float("inf")
            for i in range(len(self.reduced_cost_matrix)): # find the min value in the column
                if i == ignore_row:
                    continue
                if self.reduced_cost_matrix[i][j] < min:
                    min = self.reduced_cost_matrix[i][j]

            if min == float("inf"):
                continue
            for i in range(len(self.reduced_cost_matrix)): # reduce the column based on the found min
                if i == ignore_row:
                    continue
                self.reduced_cost_matrix[i][j] -= min

            self.lower_bound += min

    def __lt__(self, other):
        return (self.lower_bound / len(self.visited_cities)) < (other.lower_bound / len(other.visited_cities)) 
