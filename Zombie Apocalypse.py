"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        self._human_or_zombie = {'human':[self._human_list, self.eight_neighbors], 'zombie':[self._zombie_list, self.four_neighbors]}
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for item3 in self._zombie_list:
            yield item3

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for item2 in self._human_list:
            yield item2
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        distance = 1
        visited = self
        #print visited
        grid_height = poc_grid.Grid.get_grid_height(self)
        grid_width = poc_grid.Grid.get_grid_width(self)
        distance_field = [[grid_height * grid_width for dummy_col in range(grid_width)] for dummy_row in range(grid_height)]
        #print distance_field
        boundary = poc_queue.Queue()
        for item0 in self._human_or_zombie[entity_type][0]:
            boundary.enqueue(item0)
            visited.set_full(item0[0], item0[1])
            distance_field[item0[0]][item0[1]] = 0
            #print visited
        while len(boundary) > 0:
            neighbors = []
            while len(boundary) > 0:
                cell = boundary.dequeue()
                for item1 in self.four_neighbors(cell[0], cell[1]):
                    neighbors.append(item1)
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = distance
                    boundary.enqueue(neighbor)
            distance += 1
            
        return distance_field
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in self._human_list:
            h_neighbors = self.eight_neighbors(human[0], human[1])
            h_neighbors.append(human)
            max_neighbor = []
            max_distance = 0
            for h_neighbor in h_neighbors:
                distance = zombie_distance[h_neighbor[0]][h_neighbor[1]]
                if distance > max_distance:
                    max_distance = distance
                    max_neighbor = h_neighbor
            self._human_list[self._human_list.index(human)] = max_neighbor
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        grid_height = poc_grid.Grid.get_grid_height(self)
        grid_width = poc_grid.Grid.get_grid_width(self)
        for zombie in self._zombie_list:
            z_neighbors = self.four_neighbors(zombie[0], zombie[1])
            z_neighbors.append(zombie)
            min_neighbor = []
            min_distance = grid_height * grid_width
            for z_neighbor in z_neighbors:
                distance = human_distance[z_neighbor[0]][z_neighbor[1]]
                if distance < min_distance:
                    min_distance = distance
                    min_neighbor = z_neighbor
            self._zombie_list[self._zombie_list.index(zombie)] = min_neighbor

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#for item in Zombie(3, 3, [], [], [(2, 2)]).compute_distance_field('human'):
    #print item, "\n"
#poc_zombie_gui.run_gui(Zombie(30, 40))
#[-15.0 pts] For obj = Zombie(3, 3, [], [(2, 2)], [(1, 1)]), dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]], obj.move_humans(dist) then obj.humans() expected location to be one of [(0, 0)] but received (1, 1)
#[-12.0 pts] For obj = Zombie(3, 3, [], [(1, 1)], [(2, 2)]), dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]], obj.move_zombies(dist) then obj.zombies() expected location to be one of [(1, 2), (2, 1)] but received (1, 1)
#print Zombie(3, 3, [], [(2, 2)], [(1, 1)]).move_humans([[4, 3, 2], [3, 2, 1], [2, 1, 0]])
#print Zombie(3, 3, [], [(1, 1)], [(2, 2)]).move_zombies([[4, 3, 2], [3, 2, 1], [2, 1, 0]])
#Zombie(3, 3, [], [(1, 1)], [(1, 1)]).move_zombies([[2, 1, 2], [1, 0, 1], [2, 1, 2]])
