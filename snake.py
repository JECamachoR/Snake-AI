import pygame
import time
import random
import numpy as np

WIN_WIDTH, WIN_HEIGHT = 800, 720
GRID_WIDTH = 400
ROWS = 15
GRID_SPACE = GRID_WIDTH // ROWS

class Snake:
    """
    Snake Object
    """
    def __init__(self, x, y, body_color = (255,0,0), head_color = (255,0,255)):
        """
        Initializes the Snake Object on a given coordinate
        """
        # Position is a list of tuples where each tuple
        # is a coordinate of the position of a certain
        # block in the field
        self.positions = np.array([np.array([x, y])])
        self.direction = np.array([0, 1])
        # dir is an array of [x,y] values for the direction 
        # of the snake's movement
        self.vel = 1
        self.body_color = body_color
        self.head_color = head_color
        self.eaten = False
    
    def head(self):
        # Returns the position of the head
        return self.positions[-1]

    def move(self):
        # Funcion that moves the snake in a particular direction
        new_head = np.array([self.positions[-1] + self.direction*self.vel])
        if not self.eaten:
            self.positions[:-1] = self.positions[1:]
            self.positions[-1] = new_head
        else:
            self.eaten = False
            self.positions = np.concatenate((self.positions, new_head))
        self.positions = np.mod(self.positions, ROWS)

    def bite(self):
        return np.unique(self.positions, axis=0).shape != self.positions.shape
    
    def eat(self):
        self.eaten = True

class Fruit:
    """
    Fruits the snake can eat
    """
    def __init__(self, grid):
        x, y = random.sample(grid, 1)[0]
        grid.remove((x,y))
        self.position = np.array([x, y])

class Field():
    COLORS = {
        -1: (255, 0, 0),
        -2: (255, 0, 255),
        0: (50,50,50),
        1: (0,255,0)
    }
    available_grid = set(
        (i,j)
        for i in range(ROWS)
        for j in range(ROWS)
    )
    available_grid.remove((5,5))
    def __init__(self):
        self.grid = np.zeros((ROWS, ROWS), dtype=np.int8)

    def empty_grid(self):
        self.grid = np.zeros((ROWS, ROWS), dtype=np.int8)

    def update_grid(self, snake=None, fruits=None):
        self.empty_grid()
        self.available_grid = set(
            (i,j)
            for i in range(ROWS)
            for j in range(ROWS)
        )
        for pos in snake.positions[:-1]:
            self.grid[pos[0], pos[1]] = -1
            if (pos[0], pos[1]) in self.available_grid:
                self.available_grid.remove((pos[0], pos[1]))
        pos = snake.head()
        self.grid[pos[0], pos[1]] = -2
        if (pos[0], pos[1]) in self.available_grid: 
            self.available_grid.remove((pos[0], pos[1]))
        for fruit in fruits:
            self.grid[fruit.position[0], fruit.position[1]] = 1
            if (fruit.position[0], fruit.position[1]) in self.available_grid:
                self.available_grid.remove((fruit.position[0], fruit.position[1]))

    def draw(self, win, offset_x = 0, offset_y = 0):
        x, y = 0, 0
        for row in range(ROWS):
            pos_x = x * GRID_SPACE + offset_x
            for col in range(ROWS):
                pos_y = y * GRID_SPACE + offset_y
                pygame.draw.rect(win, self.COLORS[self.grid[x,y]], (
                    pos_x + 2,
                    pos_y + 2,
                    GRID_SPACE - 2,
                    GRID_SPACE -2
                ))
                y+=1
            x+=1
            y=0
