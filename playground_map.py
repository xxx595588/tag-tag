import numpy as np
from tkinter import *

SIZE = 30

class playgroundMap():

    def __init__(self, map):
        self.map = np.rot90(map, 3)   
        self.grid = []
        self.window = Tk()
        self.window.title("Playground Map")
        self.runner_pre_x = None
        self.runner_pre_z = None

        Canvas(self.window, bg="black")

        for i in range(len(self.map)):
            self.grid.append([])
            for j in range(len(self.map[i])):
                if self.map[i][j] == 1:
                    self.grid[i].append(Canvas(self.window, bg="black", height="20", width="20"))
                else:
                    self.grid[i].append(Canvas(self.window, bg="white", height="20", width="20"))
                self.grid[i][j].grid(row=i, column=j)

        self.window.update()

    def render(self, runner_x, runner_z, is_hor):
        temp = []

        #print(f"current ({runner_z}, {runner_x})")
        self.map[SIZE-runner_x-1][runner_z] = 8
        

        # when runner move horizontally 
        if is_hor:
            self.grid = np.flipud(self.grid)

            for i, j in enumerate(np.flipud(self.map)[runner_x]):
                if i == runner_z:
                    temp.append(Canvas(self.window, bg="red", height="20", width="20"))
                elif j == 1:
                    temp.append(Canvas(self.window, bg="black", height="20", width="20"))
                else:
                    temp.append(Canvas(self.window, bg="white", height="20", width="20"))

            self.grid[runner_x] = temp
            self.grid = np.flipud(self.grid)
        # when runner move vertically 
        else:
            self.grid = np.transpose(np.flip(self.grid, 0))

            for i, j in enumerate(np.transpose(np.flip(self.map, 0))[runner_z]):
                if i == runner_x:
                    temp.append(Canvas(self.window, bg="red", height="20", width="20"))
                elif j == 1:
                    temp.append(Canvas(self.window, bg="black", height="20", width="20"))
                else:
                    temp.append(Canvas(self.window, bg="white", height="20", width="20"))

            self.grid[runner_z] = temp
            self.grid = np.flip(np.transpose(self.grid), 0)
        
        # clean up previous position
        if self.runner_pre_x != None and self.runner_pre_z != None:
            self.grid = np.transpose(np.flip(self.grid, 0))
            temp = []
            #print(f"clean up ({self.runner_pre_z}, {self.runner_pre_x})")
            for i, j in enumerate(np.transpose(np.flip(self.map, 0))[self.runner_pre_z]):
                if i == self.runner_pre_x:
                    temp.append(Canvas(self.window, bg="white", height="20", width="20"))
                elif j == 1:
                    temp.append(Canvas(self.window, bg="black", height="20", width="20"))
                else:
                    temp.append(Canvas(self.window, bg="white", height="20", width="20"))
            self.grid[self.runner_pre_z] = temp

            temp = []
            for i, j in enumerate(np.transpose(np.flip(self.map, 0))[runner_z]):
                if i == runner_x:
                    temp.append(Canvas(self.window, bg="red", height="20", width="20"))
                elif j == 1:
                    temp.append(Canvas(self.window, bg="black", height="20", width="20"))
                else:
                    temp.append(Canvas(self.window, bg="white", height="20", width="20"))
            self.grid[runner_z] = temp

            self.grid = np.flip(np.transpose(self.grid), 0)

            self.map[SIZE-self.runner_pre_x-1][self.runner_pre_z] = 0
        
        self.runner_pre_z = runner_z
        self.runner_pre_x = runner_x

        # reconstruct the map
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.grid[i][j].grid(row=i, column=j)

        # display the map in termial (1 represents wall, 8 reoresents runner)
        #print(self.map)
        
        
        self.window.update()