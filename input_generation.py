#!/usr/bin/env python
# coding: utf-8

# In[233]:


import numpy as np


# In[272]:


class RGraph():
    def __init__(self, num_location, num_home, starting_location):
        self.num_location = num_location
        self.num_home = num_home
        self.starting_location = starting_location
        self.edge_matrix = np.zeros((self.num_location, self.num_location))
        self.visited = {}
        self.locations = [starting_location]
        self.homes = []

    def check_if_connected(self):
        return all([value for value in self.visited.values()])

    def dfs(self, i):
        self.visited[i] = True
        for j in range(self.num_location):
            if self.edge_matrix[i][j] != 0 and not self.visited[j]:
                self.dfs(j)

    def random_input_generator(self):

        p = 0.7
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
        if self.check_if_connected():
            print('connected')
        else:
            print('not connected')

        self.homes = self.locations.copy()[1:self.num_home+1]
        np.random.shuffle(self.homes)

        self.generate_input()

    def generate_input(self):
        print(self.num_location)
        print(self.num_home)

        [print(v, end =  ' ') for v in self.locations]
        print()
        [print(h, end =  ' ') for h in self.homes[:self.num_home]]
        print()
        print(self.starting_location)
        for i in range(self.num_location):
            for j in range(self.num_location):
                if self.edge_matrix[i][j] == 0:
                    print("x", end = ' ')
                else:
                    print(str(self.edge_matrix[i][j]), end = ' ')
            print()

    def generate_random_edge(self):
        return np.around(np.random.uniform(50,100), 5)

    def generate_output(self):
        print("Soda location1 Soda")
        print(1)
        print("location1", end = ' ')
        for h in self.homes:
            print(h, end = ' ')



# In[280]:


g = RGraph(50, 25, "Soda")
g.random_input_generator()


# In[281]:


print("===========================================================")

g.generate_output()


# In[279]:



# In[ ]:





# In[ ]:





# In[ ]:




