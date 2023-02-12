import numpy as np
from tkinter import *

SIZE = 30

class playgroundMap():
    def __init__(self, map, runner_z, runner_x, tagger_z, tagger_x):
        self.map = map
        self.window = Tk()
        self.grid = []
        self.window.title("Playground Map")

        self.runner_cur_x = runner_x
        self.runner_cur_z = runner_z
        self.tagger_cur_x = tagger_x
        self.tagger_cur_z = tagger_z

        self.runner_pre_x = None
        self.runner_pre_z = None
        self.tagger_pre_x = None
        self.tagger_pre_z = None

        Canvas(self.window, bg="black")

        Canvas(self.window, bg="black")

        for i in range(len(self.map)):
            self.grid.append([])
            for j in range(len(self.map[i])-1, -1, -1):
                if i == runner_x and j == SIZE-1-runner_z:
                    self.grid[i].append(Canvas(self.window, bg="red", height="20", width="20"))
                    self.map[i][j] = 8
                elif i == tagger_x and j == SIZE-1-tagger_z:
                    self.grid[i].append(Canvas(self.window, bg="blue", height="20", width="20"))
                    self.map[i][j] = 4
                elif self.map[i][j] == 1:
                    self.grid[i].append(Canvas(self.window, bg="black", height="20", width="20"))
                else:
                    self.grid[i].append(Canvas(self.window, bg="white", height="20", width="20"))

        self.grid = np.flip(self.grid, axis=0)

        for i in range(SIZE):
            for j in range(SIZE):
                self.grid[i][j].grid(row=i, column=j)
        
        self.window.update()

    def render(self, z, x, id):  
        if id == 0:
            self.runner_pre_z = self.runner_cur_z
            self.runner_pre_x = self.runner_cur_x
            self.runner_cur_z = z
            self.runner_cur_x = x
            self.clean_trace(self.runner_pre_z, self.runner_pre_x)
            self.map[x][SIZE-1-z] = 8
            self.map[self.runner_pre_x][SIZE-1-self.runner_pre_z] = 0
            
        else:
            self.tagger_pre_z = self.tagger_cur_z
            self.tagger_pre_x = self.tagger_cur_x
            self.tagger_cur_z = z
            self.tagger_cur_x = x
            self.clean_trace(self.tagger_pre_z, self.tagger_pre_x)
            self.map[x][SIZE-1-z] = 4
            self.map[self.tagger_pre_x][SIZE-1-self.tagger_pre_z] = 0
            

        self.grid = np.flip(self.grid, axis=0)
        self.grid[self.runner_cur_x][self.runner_cur_z].configure(bg="red")
        self.grid[self.tagger_cur_x][self.tagger_cur_z].configure(bg="blue")

        self.grid = np.flip(self.grid, axis=0)
        self.window.update()

    def clean_trace(self, z, x):
        self.grid = np.flip(self.grid, axis=0)

        # clean up previous position
        for i in range(len(self.map[x])-1, -1, -1):
            if self.map[x][i] == 1:
                self.grid[x][SIZE-i-1].configure(bg="black")
            else:
                self.grid[x][SIZE-i-1].configure(bg="white")

        self.grid = np.flip(self.grid, axis=0)