import numpy as np
from tkinter import *

SIZE = 30

class playgroundMap():
    def __init__(self, map, runner_z, runner_x, tagger_z, tagger_x):
        self.map = map
        self.window = Tk()
        self.grid = []
        self.window.title("Playground Map")
        self.runner_pre_x = runner_x
        self.runner_pre_z = runner_z
        self.tagger_pre_x = tagger_x
        self.tagger_pre_z = tagger_z

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
        # when runner move horizontally 
        
        if id == 0:
            #if((z-self.runner_pre_z)**2 + (x-self.runner_pre_x)**2) > 1:
            self.clean_trace(self.runner_pre_z, self.runner_pre_x, id)
           
            self.map[x][SIZE-1-z] = 8
            self.map[self.runner_pre_x][SIZE-1-self.runner_pre_z] = 0
            self.runner_pre_z = z
            self.runner_pre_x = x
        else:
            #if((z-self.tagger_pre_z)**2 + (x-self.tagger_pre_x)**2) > 1:
            self.clean_trace(self.tagger_pre_z, self.tagger_pre_x, id)
           
            self.map[x][SIZE-1-z] = 4
            self.map[self.tagger_pre_x][SIZE-1-self.tagger_pre_z] = 0
            self.tagger_pre_z = z
            self.tagger_pre_x = x

        self.grid = np.flip(self.grid, axis=0)

        if id == 0:
            self.grid[x][z].configure(bg="red")
        else:
            self.grid[x][z].configure(bg="blue")

        self.grid = np.flip(self.grid, axis=0)
        self.window.update()

    def clean_trace(self, z, x, id):
        self.grid = np.flip(self.grid, axis=0)

        # clean up previous position
        for i in range(len(self.map[x])-1, -1, -1):
            if self.map[x][i]== 1:
                self.grid[x][SIZE-i-1].configure(bg="black")
            else:
                self.grid[x][SIZE-i-1].configure(bg="white")

        self.grid = np.flip(self.grid, axis=0)