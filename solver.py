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


class MST():
    def __init__(self, list_of_locations, adjacency_matrix, starting_car_location):
        self.V = list_of_locations
        self.adjacency_matrix = adjacency_matrix
        self.starting_car_location = starting_car_location
        self.inMST = [False] * len(self.V)
        self.inMST[list_of_locations.index(starting_car_location)] = True
        self.mst = [[0] * len(self.V)] * len(self.V)

    def isValidEdge(self, u, v):
        if u == v:
            return False
        if self.inMST[u] == False and self.inMST[v] == False:
            return False
        elif self.inMST[u] == True and self.inMST[v] == True:
            return False
        return True

    def constructMst(self):
        edge_count = 0
        while edge_count < len(self.V) - 1:
            minVal = sys.maxsize
            a = -1
            b = -1
            for i in range(len(self.V)):
                for j in range(len(self.V)):
                    if self.adjacency_matrix[i][j] < minVal and self.adjacency_matrix[i][j] != 0:
                        if self.isValidEdge(i, j):
                            minVal = self.adjacency_matrix[i][j]
                            a = i
                            b = j
            if a != -1 and b != -1:
                self.inMST[a] = self.inMST[b] = True
                self.mst[a][b] = minVal
            edge_count += 1
        return self.mst


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
