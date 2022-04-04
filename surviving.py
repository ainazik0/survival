from copy import deepcopy
import random
import tkinter as tk

class Sim:
    def __init__(self, c, n, m, height, width):
        self.__n = n
        self.__m = m
        self.c = c
        self.height = height
        self.width = width
        self.s = 0
        
        self.make_surface()
        self.spawn_supply(random.randint(8, 15))
        self.spawn_sims((self.__n * self.__m) // 10)
    
    def make_surface(self):
        self.surface = []
        for i in range(self.__n):
            row = []
            for j in range(self.__m):
                row.append(0)
            self.surface.append(row)
    
    def spawn_sims(self, amount):
        co = 0
        t = 0
        while co != amount and t <= self.__m * self.__n:
            i = random.randint(0, self.__n - 1)
            j = random.randint(0, self.__m - 1)
            if self.surface[i][j] == 0:
                self.surface[i][j] = 1
                co += 1
            t += 1
    
    def spawn_supply(self, amount):
        co = 0
        t = 0
        while co != amount and t <= self.__m * self.__n:
            i = random.randint(0, self.__n - 1)
            j = random.randint(0, self.__m - 1)
            if self.surface[i][j] == 0:
                self.surface[i][j] = 9
                co += 1
            t += 1
    
    def draw(self):
        self.c.delete('all')
        sizen = self.width // (self.__n)
        sizem = self.height // (self.__m)
        for i in range(self.__n):
            for j in range(self.__m):
                if self.surface[i][j] == 1:
                    color = 'green'
                elif self.surface[i][j] == 9:
                    color = 'red'
                else:
                    color = 'white'
                self.c.create_rectangle(0 + (i * sizen), 0 + (j * sizem), sizen + (i * sizen), sizem + (j * sizem), fill = color)
        self.step()
        self.c.after(50, self.draw)
    
    def step(self):
        if self.s == 30:
            self.s = 0
            self.__clear_supply()
            self.spawn_supply(random.randint(8, 15))
        sur = deepcopy(self.surface)
        for i in range(self.__n):
            for j in range(self.__m):
                if self.surface[i][j] != 9:
                    supply = False
                    neib_num = 0
                    
                    if 0 <= i - 1 < self.__n and 0 <= j - 1 < self.__m:
                        if self.surface[i - 1][j - 1] == 1:
                            neib_num += 1
                        if self.surface[i - 1][j - 1] == 9:
                            supply = True
                    if 0 <= i < self.__n and 0 <= j - 1 < self.__m:
                        if self.surface[i][j - 1] == 1:
                            neib_num += 1
                        if self.surface[i][j - 1] == 9:
                            supply = True
                    if 0 <= i + 1 < self.__n and 0 <= j - 1 < self.__m:
                        if self.surface[i + 1][j - 1] == 1:
                            neib_num += 1
                        if self.surface[i + 1][j - 1] == 9:
                            supply = True
                    
                    if 0 <= i + 1 < self.__n and 0 <= j < self.__m:
                        if self.surface[i - 1][j] == 1:
                            neib_num += 1
                        if self.surface[i - 1][j] == 9:
                            supply = True
                    if 0 <= i + 1 < self.__n and 0 <= j < self.__m:
                        if self.surface[i + 1][j] == 1:
                            neib_num += 1
                        if self.surface[i + 1][j] == 9:
                            supply = True
                    
                    if 0 <= i - 1 < self.__n and 0 <= j + 1 < self.__m:
                        if self.surface[i - 1][j + 1] == 1:
                            neib_num += 1
                        if self.surface[i - 1][j + 1] == 9:
                            supply = True
                    if 0 <= i < self.__n and 0 <= j + 1 < self.__m:
                        if self.surface[i][j + 1] == 1:
                            neib_num += 1
                        if self.surface[i][j + 1] == 9:
                            supply = True
                    if 0 <= i + 1 < self.__n and 0 <= j + 1 < self.__m:
                        if self.surface[i + 1][j + 1] == 1:
                            neib_num += 1
                        if self.surface[i + 1][j + 1] == 9:
                            supply = True

                    if supply:
                        if self.surface[i][j] == 0:
                            if neib_num >= 1:
                                sur[i][j] = 1
                        else:
                            if neib_num >= 4:
                                sur[i][j] = 0
                    else:
                        if self.surface[i][j] == 0:
                            if neib_num == 3:
                                sur[i][j] = 1
                        else:
                            if not neib_num in [2,3]:
                                sur[i][j] = 0
        self.surface = sur
        self.s += 1
    
    def __clear_supply(self):
        for i in range(self.__n):
            for j in range(self.__m):
                if self.surface[i][j] == 9:
                    self.surface[i][j] = 0 

n = 40
m = 40

root = tk.Tk()
root.geometry('{}x{}'.format(20 * m, 20 * n))
canva = tk.Canvas(root, width = 20 * m, height = 20 * n)

s = Sim(canva, n, m, 20 * n, 20 * m)

s.draw()

canva.pack()
root.mainloop()