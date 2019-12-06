import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    adjacency_matrix = [[0 if entry == 'x' else entry for entry in row] for row in adjacency_matrix]
    mst_obj = MST(list_of_locations, list_of_homes, adjacency_matrix, starting_car_location)
    approximator = tspApproximation(mst_obj.V, mst_obj.list_of_homes, adjacency_matrix, mst_obj.mst, mst_obj.starting_car_location)
    tour = approximator.find_tour()
    drop_off = { mst_obj.start_index: [list_of_locations.index(x) for x in list_of_homes]}
    return tour, drop_off


class MST():
    """
    reference: https://www.geeksforgeeks.org/prims-algorithm-simple-implementation-for-adjacency-matrix-representation/
    """
    def __init__(self, list_of_locations, list_of_homes, adjacency_matrix, starting_car_location):
        self.V = list_of_locations
        self.num_location = len(self.V)
        self.adjacency_matrix = adjacency_matrix
        self.starting_car_location = starting_car_location
        self.inMST = [False] * self.num_location
        self.start_index = list_of_locations.index(starting_car_location)
        self.inMST[self.start_index] = True
        self.mst = [[0 for i in range(self.num_location)] for j in range(self.num_location)]

        self.visited = {}
        self.list_of_homes = list_of_homes
        self.indices_to_remove = []


    def is_valid_edge(self, u, v):
        if u == v:
            return False
        if self.inMST[u] == False and self.inMST[v] == False:
            return False
        elif self.inMST[u] == True and self.inMST[v] == True:
            return False
        return True

    def construct_mst(self):
        edge_count = 0
        while edge_count < self.num_location - 1:
            min_val = sys.maxsize
            a = -1
            b = -1
            for i in range(self.num_location):
                for j in range(self.num_location):
                    if self.adjacency_matrix[i][j] < min_val and self.adjacency_matrix[i][j] != 0:
                        if self.is_valid_edge(i, j):
                            min_val = self.adjacency_matrix[i][j]
                            a = i
                            b = j
            if a != -1 and b != -1:
                self.inMST[a] = self.inMST[b] = True
                self.mst[a][b] = min_val
                self.mst[b][a] = min_val
            edge_count += 1
        return self.mst

    def remove_non_TA_homes(self):
        self.dfs(self.start_index)
        self.indices_to_remove.sort(reverse=True)
        print(self.indices_to_remove)
        for i in self.indices_to_remove:
            for j in range(self.num_location):
                self.mst[j].pop(i)
            self.mst.pop(i)
            self.V.pop(i)
            self.num_location -= 1
        return self.mst

    def dfs(self, start):
        self.visited = dict([(i, False) for i in range(self.num_location)])
        stack = []
        stack.append(start)
        while (len(stack)):
            s = stack[-1]
            stack.pop()

            self.visited[s] = True
            leaf = True
            for i in range(self.num_location):
                if not self.visited[i]:
                    leaf = False
                    stack.append(i)

            if self.is_leaf(s, leaf, stack) and not self.is_TA_home(s):
                self.indices_to_remove.append(s)

    def is_leaf(self, i, leaf, stack):
        if leaf:
            return True
        for j in range(self.num_location):
            if j not in stack and self.mst[i][j] != 0 and j not in self.indices_to_remove:
                return False
        return True

    def is_TA_home(self, i):
        return i == self.start_index or self.V[i] in self.list_of_homes


class tspApproximation():
    def __init__(self, list_of_locations, list_of_homes, adjacency_matrix, mst, starting_car_location):
        self.V = list_of_locations
        self.list_of_homes = list_of_homes
        self.num_location = len(self.V)
        self.adjacency_matrix = adjacency_matrix
        self.mst = mst
        self.starting_car_location = starting_car_location
        self.start_index = list_of_locations.index(starting_car_location)
        self.visited = self.visited = dict([(i, False) for i in range(self.num_location)])
        self.dfs_tour = []

    def dfs(self, i):
        self.visited[i] = True
        self.dfs_tour.append(i)
        for j in range(self.num_location):
            if self.mst[i][j] != 0 and not self.visited[j]:
                self.dfs(j)
                self.dfs_tour.append(i)

    def find_tour(self):
        self.dfs(self.start_index)
        print(self.dfs_tour)
        return self.compress_tour()

    def compress_tour(self):
        for _ in range(len(self.dfs_tour)):
            for i in range(len(self.dfs_tour)):
                if i == len(self.dfs_tour) - 1:
                    break
                prev_ind = self.dfs_tour[i-1]
                next_ind = self.dfs_tour[i+1]
                if self.dfs_tour[i] in self.dfs_tour[:i] and self.adjacency_matrix[prev_ind][next_ind] != 0:
                    self.dfs_tour.pop(i)
                    break
        return self.dfs_tour



"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
