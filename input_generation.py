#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[226]:


class RGraph():
    def __init__(self, num_location, num_home, starting_location):
        self.num_location = num_location
        self.num_home = num_home
        self.starting_location = starting_location
        self.edge_matrix = np.zeros((self.num_location, self.num_location))
        self.visited = {}
        self.locations = [starting_location]

    def check_if_connected(self):
        return all([value for value in self.visited.values()])

    def dfs(self, i):
        self.visited[i] = True
        for j in range(self.num_location):
            if self.edge_matrix[i][j] != 0 and not self.visited[j]:
                self.dfs(j)


    def generate_random_edge(self):
        return np.around(np.random.uniform(50,100), 5)
    def random_input_generator(self):

        p = 0.6
        for i in range(self.num_location-1):
            self.locations.append("location{}".format(i+1))

        for i in range(self.num_location):
            for j in range(self.num_location):
                if j > i or i == j :
                    continue
                if np.random.uniform(0,1) < p:
                    rand_num = self.generate_random_edge()
                    self.edge_matrix[i][j], self.edge_matrix[j][i] = rand_num, rand_num

        # check if the graph is connected
        self.visited = dict([(i, False) for i in range(self.num_location)])
        self.dfs(0)
#         if self.check_if_connected():
#             print('connected')
#         else:
#             print('not connected')

        homes = self.locations.copy()[1:]
        np.random.shuffle(homes)

        self.generate_input(homes)

    def generate_input(self, homes):
        print(self.num_location)
        print(self.num_home)

        [print(v, end =  ' ') for v in self.locations]
        print()
        [print(h, end =  ' ') for h in homes[:self.num_home]]
        print()
        print(self.starting_location)
        for i in range(self.num_location):
            for j in range(self.num_location):
                if self.edge_matrix[i][j] == 0:
                    print("x", end = ' ')
                else:
                    print(str(self.edge_matrix[i][j]), end = ' ')
            print()


# In[ ]:





# In[225]:


g = RGraph(100, 50, "Soda")
g.random_input_generator()


# In[223]:




# In[ ]:





# In[ ]:





# In[ ]:




