import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import random

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
    total_energy = sys.maxsize
    final_path = []
    final_ret_dict = {}
    
    if len(adjacency_matrix[0]) <= 50:
        num_iterations = 100
    elif len(adjacency_matrix[0]) <= 100:
        num_iterations = 10
    elif len(adjacency_matrix[0]) > 100:
        num_iterations = 2
    
    for i in range(num_iterations):

        # generating a random path first (Can be optimized by choosing paths from MST and using DFS)
        path = generate_path(list_of_locations, starting_car_location, adjacency_matrix)

        # generate random drop off locations
        drop_off_locations = generate_drop_off_locations(path)
        
        # generate dictionary mapping drop off locations to list of ta's
        dict_ta_to_dropoff_location = find_closest_dropoff_location_to_ta(drop_off_locations, list_of_locations, list_of_homes, adjacency_matrix)
        ret_dict = convert_to_return(dict_ta_to_dropoff_location)
    
        curr_total_energy = 0
    
        # finding total_energy from just driving
        for p1 in range(len(path) - 1):
            curr_total_energy += 0.667 * adjacency_matrix[path[p1]][path[p1+1]]
    
        # finding total_energy from ta's walking as well
        for k in ret_dict:
            for v in ret_dict[k]:
                if (k != v): # if they equal, the cost is 0
                    curr_total_energy += dict_ta_to_dropoff_location[v][1]  
                
        if curr_total_energy < total_energy:
            # update path and ret_dict
            total_energy = curr_total_energy
            final_path = path
            final_ret_dict = ret_dict
        
    
    return final_path, final_ret_dict
    
 

# Helper Functions for solve
def generate_path(list_of_locations, starting_car_location, adjacency_matrix):
    path = []
    
    starting_index = list_of_locations.index(starting_car_location)
    next_index = adjacency_matrix[starting_index].index(random.choice([i for i in adjacency_matrix[starting_index] if i != 0 and i != 'x']))
    path.append(starting_index)
    path.append(next_index)

    path_counter = 0
    while next_index != starting_index:
        # this first if condition solely for limiting path size for performance reasons
        if path_counter >= 100 and (adjacency_matrix[next_index][starting_index] != 0 and adjacency_matrix[next_index][starting_index] != 'x'):
            next_index = starting_index
            path.append(next_index)
        # another performance sacrifice...if path_counter exceeds 2000, drop everyone off at start. This usually happens with sparse graphs
        elif path_counter >= 2000:
            path = []
            path.append(starting_index)
        else:
            next_index = adjacency_matrix[next_index].index(random.choice([i for i in adjacency_matrix[next_index] if i != 0 and i != 'x']))
            path.append(next_index)

        path_counter += 1        
    return path


def generate_drop_off_locations(path):
    path_length = len(path)
    # pick a random number of locations as drop-off locations
    drop_off_locations = random.sample(path, random.randrange(1, path_length))
    return drop_off_locations



def find_closest_dropoff_location_to_ta(drop_off_locations, list_of_locations, list_of_homes, adjacency_matrix):
    num_vertices = len(adjacency_matrix[0])
    
    # filling in a dictionary mapping TA home to [dropoff location, dropoff distance]
    dict_ta_to_dropoff_location = {}
    for h in list_of_homes:
        dict_ta_to_dropoff_location[list_of_locations.index(h)] = [0, sys.maxsize]
    
    # finding the closest dropoff location to each TA's home using previous dictionary dict_ta_to_dropoff_location
    for d in drop_off_locations:
        for h in list_of_homes:
            home_index = list_of_locations.index(h)
            dist_d_to_h = dijkstra(num_vertices, adjacency_matrix, d)[home_index]
            if dist_d_to_h < dict_ta_to_dropoff_location[home_index][1]:
                dict_ta_to_dropoff_location[home_index] = [d, dist_d_to_h]
                
    return dict_ta_to_dropoff_location


def convert_to_return(dict_ta_to_dropoff_location): 
    # converting dict_ta_to_dropoff_location to output dictionary format
    ret_dict = {}  # dict mapping dropoff_location to list_of_TAs
    for h in dict_ta_to_dropoff_location:
        if dict_ta_to_dropoff_location[h][0] in ret_dict:
            ret_dict[dict_ta_to_dropoff_location[h][0]].append(h)
        else:
            ret_dict[dict_ta_to_dropoff_location[h][0]] = [h]
    
    return ret_dict


# returns array that represents distances from src to each other vertex (by index) in graph 
def dijkstra(num_vertices, adjacency_matrix, src):    
    dist = [sys.maxsize] * num_vertices
    dist[src] = 0
    sptSet = [False] * num_vertices

    for cout in range(num_vertices):
        u = minDistance(num_vertices, dist, sptSet)
        sptSet[u] = True 
        for v in range(num_vertices):
            if adjacency_matrix[u][v] != 'x' and adjacency_matrix[u][v] > 0 and sptSet[v] == False and \
                dist[v] > dist[u] + adjacency_matrix[u][v]:
                dist[v] = dist[u] + adjacency_matrix[u][v]

    return dist


def minDistance(num_vertices, dist, sptSet):
    min = sys.maxsize
    for v in range(num_vertices):
        if dist[v] < min and sptSet[v] == False:
            min = dist[v]
            min_index = v

    return min_index




class MST():
    """
    reference: https://www.geeksforgeeks.org/prims-algorithm-simple-implementation-for-adjacency-matrix-representation/
    """
    def __init__(self, list_of_locations, adjacency_matrix, starting_car_location):
        self.V = list_of_locations
        self.num_location = len(self.V)
        self.adjacency_matrix = adjacency_matrix
        self.starting_car_location = starting_car_location
        self.inMST = [False] * self.num_location
        self.start_index = list_of_locations.index(starting_car_location)
        self.inMST[self.start_index] = True
        self.mst = [[0 for i in range(self.num_location)] for j in range(self.num_location)]

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
