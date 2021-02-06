from snake import *
import os
import neat

pygame.font.init()
STAT_FONT = pygame.font.SysFont("arial", 50)

try:
    with open("AI_HIGH_SCORE.txt", "r") as f:
        GLOBAL_HIGH_SCORE = int(f.read())
except FileNotFoundError:
    GLOBAL_HIGH_SCORE = 0
except ValueError:
    GLOBAL_HIGH_SCORE = 0
ROWS, COLS = 15,15
HIGH_SCORE = 0
CENTER = ROWS // 2 + 1 if ROWS % 2 == 1 else ROWS // 2
GEN = 0
ALIVE = 0
game = 0    
# SQUARE_WIDTH = min(WIN_HEIGHT // ROWS, WIN_WIDTH // COLS)
# GRID_WIDTH = WIN_WIDTH // NGRIDS
# WIN_WIDTH += SQUARE_WIDTH
WIN_HEIGHT, WIN_WIDTH = 825, 1500
GRID_WIDTH = WIN_WIDTH // 10

class TrainingGame(Game):

    def __init__(self, rows, cols, genome, config):
        self.ROWS = rows
        self.COLS = cols
        self.score = 0
        self.moves_since_point = 0
        self.HIGH_SCORE = self.get_high_score("AI_HIGH_SCORE.txt")
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
        self.genome = genome
        self.genome.fitness = 0
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)

    def iteration(self):
        # Gets input from controller (be it the player or AI to be implemented)
        self.get_input()
        # Given the input calculate the movement of the snake
        self.snake.move()
        # If the snakes bites itself save high_score and end game
        head = self.snake.head()
        if self.snake.bite() or head[0] >= self.ROWS or head[1] >= self.COLS or (head < 0).any():
            self.save_high_score()
            self.genome.fitness -= 500
            return False
        # Check if fruit has been eaten
        if abs(head[0] - self.fruit.position[0]) < 1 and abs(head[1] - self.fruit.position[1]) < 1:
            self.fruit = Fruit(self.field.available_positions)
            self.snake.eat()
            self.score += 1
            # Add fitness for eating fruit
            self.genome.fitness += 100 * self.score
            self.moves_since_point = 0
        else:
            self.moves_since_point += 1
        if self.moves_since_point > (self.score + 2) * self.ROWS:
            self.genome.fitness -= (self.score)* self.ROWS + 1
            return False
        
        # Add fitness for being alive
        self.genome.fitness += 5
        try:
            return self.field.update_grid(self.snake, self.fruit)
        except:
            return True

    def get_input(self):
        """def snake_vision_2(game, field):
        pos = game.snake.positions - game.snake.head()
        vert = pos[pos[:,1] == 0][:,0]
        horz = pos[pos[:,0] == 0][:,1]
        diag_1 = pos[np.where(pos[:,0] == pos[:,1]), 0]
        diag_2 = pos[np.where(pos[:,0] ==-pos[:,1]), 0]
        ds = [
            -diag_1[diag_1 < 0],    # NORTH WEST
            -vert[vert < 0],        # NORTH
            -diag_2[diag_2 < 0],    # NORTH EAST
            -horz[horz < 0],        # WEST
            np.array([0.5]),        # CENTER
            horz[horz > 0],         # EAST
            diag_2[diag_2 > 0],     # SOUTH WEST
            vert[vert > 0],         # SOUTH
            diag_1[diag_1 > 0]      # SOUTH EAST
        ]
        field.grid = np.array([d.min() if len(d)>0 else 0 for d in ds]).reshape(field.grid.shape)
        i_xy = np.nonzero(field.grid)
        field.grid[i_xy] = -1 / (field.grid[i_xy])
        # Up til here there are 8 inputs
        dist = game.fruit.position - game.snake.head()
        dist = max(game.ROWS, game.COLS) * dist/np.linalg.norm(dist)
        head = game.snake.head() +1
        y_dist, x_dist = head[0] / game.ROWS, head[1] / game.COLS
        """
        pos = self.snake.positions - self.snake.head()
        vert = pos[pos[:,1] == 0][:,0]
        horz = pos[pos[:,0] == 0][:,1]
        diag_1 = pos[np.where(pos[:,0] == pos[:,1]), 0]
        diag_2 = pos[np.where(pos[:,0] ==-pos[:,1]), 0]
        ds = [
            -diag_1[diag_1 < 0],    # NORTH WEST
            -vert[vert < 0],        # NORTH
            -diag_2[diag_2 < 0],    # NORTH EAST
            -horz[horz < 0],        # WEST
            horz[horz > 0],         # EAST
            diag_2[diag_2 > 0],     # SOUTH WEST
            vert[vert > 0],         # SOUTH
            diag_1[diag_1 > 0]      # SOUTH EAST
        ]
        selfception = [-1/d.min() if len(d)>0 else 0 for d in ds]
        fruit_smell = self.fruit.position - self.snake.head()
        fruit_smell = list(max(self.ROWS, self.COLS) * fruit_smell/np.linalg.norm(fruit_smell))
        head = self.snake.head()
        head_pos = [head[0] / self.ROWS, head[1] / self.COLS]

        # Up til here there are 8 inputs
        output = self.net.activate(
            selfception + fruit_smell + head_pos
        )
        o = output.index(max(output))

        # THE REAL ONE
        if o == 0:
            if self.snake.direction[1] != -1:
                self.snake.direction[1] = 1
                self.snake.direction[0] = 0
        elif o == 1:
            if self.snake.direction[0] != 1:
                self.snake.direction[0] = -1
                self.snake.direction[1] = 0
        elif o == 2:
            if self.snake.direction[1] != 1:
                self.snake.direction[1] = -1
                self.snake.direction[0] = 0
        elif o == 3:
            if self.snake.direction[0] != -1:
                self.snake.direction[0] = 1
                self.snake.direction[1] = 0

def display(win, games):
    win.fill((0,0,0))
    x, y = 0,0
    # for i in range(len(fields)):
    #     fields[i].draw(win, offset_x=fields[i].off[0]*GRID_WIDTH, offset_y=fields[i].off[1]*GRID_WIDTH)
    for game in games:
        game.draw(win, offset_x =game.off_x*GRID_WIDTH, offset_y=game.off_y*GRID_WIDTH, GRID_SPACE=GRID_WIDTH//ROWS)
    for i in range(10):
        x = (i+1) * GRID_WIDTH
        pygame.draw.line(win, (200,200,200),(x,0), (x, GRID_WIDTH*5))
    for j in range(5):
        y = (j+1) * GRID_WIDTH
        pygame.draw.line(win, (200,200,200),(0,y), (WIN_WIDTH,y))
    text = STAT_FONT.render(f"Global HS {GLOBAL_HIGH_SCORE}, HS {HIGH_SCORE}, GEN {GEN}, ALIVE {ALIVE}", 1,(255,255,255))
    win.blit(text, (10, 10 + GRID_WIDTH*5))
    pygame.display.update()

def train(genomes, config):
    global HIGH_SCORE, GEN, ALIVE, GLOBAL_HIGH_SCORE
    HIGH_SCORE = 0
    best = None
    run = True
    games = []
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    for _, g in genomes:
        games.append(TrainingGame(ROWS, COLS, g, config))
    offs = []
    for i in range(10):
        for j in range(5):
            offs.append((i,j))
    for i, game in enumerate(games):
        game.off_x = offs[i%len(offs)][0]
        game.off_y = offs[i%len(offs)][1]
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
        if GEN % 5 == 0:
            clock.tick(12)
        if HIGH_SCORE > 5:
            clock.tick(8)
        games_ended = []
        for game in games:
            if not game.iteration():
                games_ended.append(game)
            if game.score > HIGH_SCORE:
                HIGH_SCORE = game.score
                best = game
        for game in games_ended:
            games.remove(game)
            games_ended.remove(game)
        ALIVE = len(games)
        if ALIVE < 50:
            n = ALIVE
        else:
            n=50
        display(win, games[:n])
        if len(games) == 0:
            run = False
    if HIGH_SCORE > GLOBAL_HIGH_SCORE:
        GLOBAL_HIGH_SCORE = HIGH_SCORE
    GEN += 1
        
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(train, 1000)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)