import pygame
import random
import numpy as np

class Game:
    """
    Game object which has one snake, one field and n number of fruits,
    it also saves information about the score
    """
    COLORS = {
        -1: (162, 64, 65),
        -2: (136, 30, 32),
        0: (50,50,50),
        1: (90,115,48)
    } # The colors used to display the game

    def __init__(self, rows=7, cols=7, n_fruits=1, colors=None, high_score_path="HIGH_SCORE.txt"):
        self.ROWS = rows
        self.COLS = cols
        if colors:
            self.COLORS = colors
        self.score = 0
        self.HIGH_SCORE = self.get_high_score()
        self.CENTER = np.array([
            rows // 2,
            cols // 2
        ])
        self.snake = Snake(        
            self.CENTER[0],                                     # x position
            self.CENTER[1],                                     # y position
            rows,                                               # number of rows
            cols                                                # number of columns
        )
        self.field = Field(rows=rows, cols=cols)
        self.fruit = Fruit(positions=self.field.available_positions)
        self.field.update_grid(self.snake, self.fruit)

    def iteration(self):
        # Gets input from controller (be it the player or AI to be implemented)
        self.get_input()
        # Given the input calculate the movement of the snake
        self.snake.move()
        # If the snakes bites itself save high_score and end game
        head = self.snake.head()
        if self.snake.bite() or head[0] >= self.ROWS or head[1] >= self.COLS or (head == -1).any():
            self.save_high_score()
            return False
        # Check if fruit has been eaten
        if abs(head[0] - self.fruit.position[0]) < 1 and abs(head[1] - self.fruit.position[1]) < 1:
            self.fruit = Fruit(self.field.available_positions)
            self.snake.eat()
            self.score += 1

        self.HIGH_SCORE = self.score if self.score > self.HIGH_SCORE else self.HIGH_SCORE
        self.field.update_grid(self.snake, self.fruit)
        return True

    def get_high_score(self, path="HIGH_SCORE.txt"):
        try:
            with open(path, "r") as f:
                return int(f.read())
        except FileNotFoundError or ValueError:
            return 0

    def save_high_score(self, path="HIGH_SCORE.txt"):
        with open(path, "w") as f:
            f.write(str(self.HIGH_SCORE))

    def colors(self, n):
        return self.COLORS[n]

    def draw(self, win, GRID_SPACE, offset_x=0, offset_y = 0):
        self.field.draw(win, GRID_SPACE, self.colors, offset_x, offset_y)

class Snake:
    """
    Snake Object
    """
    def __init__(self, x, y, rows, cols):
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
        self.eaten = False
        self.ROWS = rows
        self.COLS = cols
    
    def head(self):
        # Returns the position of the head
        return self.positions[-1]

    def move(self):
        # Funcion that moves the snake in a particular direction
        new_head = np.array([self.positions[-1] + self.direction])
        self.tail_left = tuple(self.positions[0,:])
        if not self.eaten:
            self.positions[:-1] = self.positions[1:]
            self.positions[-1] = new_head
        else:
            self.eaten = False
            self.positions = np.concatenate((self.positions, new_head))

    def bite(self):
        return np.unique(self.positions, axis=0).shape != self.positions.shape
    
    def eat(self):
        self.eaten = True

class Fruit:
    """
    Fruits the snake can eat
    """
    def __init__(self, positions=None, cols=None, rows=None):
        if not positions:
            if not cols or not rows:
                print("No columns, rows or set of valid positions given for Fruit instanciation")
            else:
                positions = set(
                    (i,j)
                    for i in range(rows)
                    for j in range(cols)
                )
        x, y = random.sample(positions, 1)[0]
        self.position = np.array([x, y])

class Field():
    def __init__(self, rows, cols):
        self.ROWS = rows
        self.COLS = cols
        self.grid = np.zeros((rows, cols))
        self.center = np.array([
            rows // 2 + 1 if rows % 2 == 1 else rows // 2, 
            cols // 2 + 1 if cols % 2 == 1 else cols // 2
        ])
        self.available_positions = set(
            (i,j)
            for i in range(self.ROWS)
            for j in range(self.COLS)
        )

    def update_grid(self, snake, fruit):
        try:
            self.available_positions.add(snake.tail_left)
            self.grid[snake.tail_left[0], snake.tail_left[1]] = 0
        except:
            return False
        for pos in snake.positions[:-1]:
            self.grid[pos[0], pos[1]] = -1
            if (pos[0], pos[1]) in self.available_positions:
                self.available_positions.remove((pos[0], pos[1]))
        
        pos = snake.head()
        self.grid[pos[0], pos[1]] = -2
        if (pos[0], pos[1]) in self.available_positions: 
            self.available_positions.remove((pos[0], pos[1]))
        self.grid[fruit.position[0], fruit.position[1]] = 1
        if (fruit.position[0], fruit.position[1]) in self.available_positions:
            self.available_positions.remove((fruit.position[0], fruit.position[1]))
        return True
    
    def empty_grid(self):
        self.grid = np.zeros((self.ROWS, self.COLS), dtype=np.int8)

    def draw(self, win, GRID_SPACE, colors, offset_x = 0, offset_y = 0):
        for row in range(self.ROWS):
            pos_y = row * GRID_SPACE + offset_y
            for col in range(self.COLS):
                pos_x = col * GRID_SPACE + offset_x
                pygame.draw.rect(win, colors(self.grid[row, col]), (
                    pos_x+1,
                    pos_y+1,
                    GRID_SPACE-1,
                    GRID_SPACE-1
                ))