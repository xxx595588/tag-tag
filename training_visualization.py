import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Visualizer():
    def __init__(self, iteration=1000, step=1):
        """
        iteration:: total amount of game iterations.
        step:: amount of iterations per add (of data).
        """
        # self.plt = plt
        self.step = step
        self.root = tk.Tk()
        self.root.title('Visualizer')
        self.root.geometry('800x600')
        self.root.update()
        self.fig = Figure(figsize=(5, 4), dpi=100)#plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0, iteration+(iteration/10)])
        self.data = []
        self.data_count = []
        self.canvas = FigureCanvasTkAgg(self.fig, self.root)  
        # self.canvas.draw()
        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        self.canvas.draw()
        self.root.update()
        # self.root.update()
    
    def add(self, data):
        self.data.append(data)
        if self.data_count == []:
            self.data_count.append(self.step)
        else:
            self.data_count.append(self.data_count[-1]+self.step)
        self.ax.plot(self.data_count, self.data, "r.-", linewidth=0.7, markersize=3)
        
        self.canvas.draw()

        self.root.update()

    def get_data(self):
        return self.data

    def show(self):
        self.root.mainloop()


if __name__ == '__main__':
    visual = Visualizer()
    # visual.pause()
    visual.add(1)
    # visual.pause()
    visual.add(2)
    visual.show()
    # plt.plot(visual.get_data())
    # plt.show()
    # plt.draw()
    # plt.show()
    # plt.draw()
    # plt.pause(0.01)
    # visual.pause()
    # visual.show()
