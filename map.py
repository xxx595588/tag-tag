import numpy as np
import math
from queue import PriorityQueue

class map():
    class grid():
        def __init__(self, x, y, obs=False):
            self.x = x
            self.y = y
            self.obs = obs
            self.h = np.inf
            self.prev = None

    def __init__(self, width, height, map_txt):
        self.width = width
        self.height = height
        self.start = None
        self.end = None
        self.cur = None
        self.content = np.empty((self.height, self.width), dtype = self.grid)

        for i in range(len(map_txt)):
            for j in range(len(map_txt[i])-1, -1, -1):
                if map_txt[i][j] == 1:
                    self.content[i][len(map_txt[i])-1-j] = self.grid(len(map_txt[i])-1-j, i, True)
                else:
                    self.content[i][len(map_txt[i])-1-j] = self.grid(len(map_txt[i])-1-j, i)
                    if map_txt[i][j] == 8:
                        self.end = (len(map_txt[i])-1-j, i)
                    if map_txt[i][j] == 4:
                        self.start = (len(map_txt[i])-1-j, i)
                        self.cur = (len(map_txt[i])-1-j, i)

        # calculate the value of h((x, y))
        self.reset()

    def update_end(self, end):
        self.end = end
        self.calculate_h()
    
    def update_start(self, start):
        self.start = start
    
    """
    The function is used to calculated the heuristic value of non-obstacle grids (Euclidean distance)
    """
    def calculate_h(self):
        for i in range(len(self.content)):
            for j in range(len(self.content[i])):
                if not self.content[i][j].obs:
                    self.content[i][j].h = math.sqrt((self.content[i][j].x - self.end[0])**2 + (self.content[i][j].y - self.end[1])**2)

    """
    This function must be call when starting a new search
    """
    def reset(self):
        self.cur = self.start

        for i in range(len(self.content)):
            for j in range(len(self.content[i])):
                if not self.content[i][j].obs:
                    self.content[i][j].prev = None
                    self.content[i][j].h = math.sqrt((self.content[i][j].x - self.end[0])**2 + (self.content[i][j].y - self.end[1])**2)
    
    """
    This function will collect all unfinished and non-obstacle grids and return as a list of tuple
    """
    def find_avaliable_grid(self, visited):
        avaliable_grid = list()
        cur_x = self.cur[0]
        cur_y = self.cur[1]

        # right search
        if cur_x - 1 >= 0 and (not self.content[cur_y][cur_x - 1].obs) and ((cur_x - 1, cur_y) not in visited):
            avaliable_grid.append((cur_x - 1, cur_y))

        # up search
        if cur_y + 1 < self.width and (not self.content[cur_y + 1][cur_x].obs) and ((cur_x, cur_y + 1) not in visited):
            avaliable_grid.append((cur_x, cur_y + 1))

        # left search
        if cur_x + 1 < self.height and (not self.content[cur_y][cur_x + 1].obs) and ((cur_x + 1, cur_y) not in visited):
            avaliable_grid.append((cur_x + 1, cur_y))

        # down search
        if cur_y - 1 >= 0 and (not self.content[cur_y - 1][cur_x].obs) and ((cur_x, cur_y - 1) not in visited):
            avaliable_grid.append((cur_x, cur_y - 1))

        return avaliable_grid
    
    """
    This function was called recursively to obtain the distance of current point from start point
    """
    def dis_from_start(self, x, y):
        if x == self.start[0] and y ==  self.start[1]:
            return 0

        prev = self.content[y][x].prev
        return 1 + self.dis_from_start(prev[0], prev[1])
    
    """
    The function must be run after calling find_shortest_path()
    It will retrieve the shortest path in reversed order
    """
    def retrieve(self):
        path = list()
        grid = self.content[self.end[1]][self.end[0]]

        while (grid.x, grid.y) != self.start:
            path.append((grid.x, grid.y))
            prev_x = grid.prev[0]
            prev_y = grid.prev[1]
            grid = self.content[prev_y][prev_x]

        return path

    """
    A* search will be used for finding the shortest path from start point to end point.

    The function was defined as: f(n) = g(n) + h(n)
    g(n), represents the cost from start point to current point n, was computed by dis_from_start()
    h(n), represents the heuristic cost at point n (which will always be less or equal to the actialy distance from n to the end point), was computed by calculate_h()

    After running this function, call retrieve() to obtain the path
    """
    def find_shortest_path(self):
        visited = set()
        pq = PriorityQueue()

        while self.cur != self.end:
            visited.add(self.cur)
            avaliable_grid = self.find_avaliable_grid(visited)
            for i in avaliable_grid:
                self.content[i[1]][i[0]].prev = self.cur
                dis = self.dis_from_start(i[0], i[1]) + self.content[i[1]][i[0]].h
                pq.put((dis, (i[0], i[1])))

            self.cur = pq.get()[1]