from snake import *
import sys
import numpy as np
import math
import pickle
import neat

class AIGame(Game):
    def __init__(self, rows, cols, genome_name, config_path="config-feedforward.txt"):
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
        self.snake.direction = np.array([1,0])
        self.field = Field(rows=rows, cols=cols)
        self.fruit = Fruit(positions=self.field.available_positions)
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
        # Unpickle saved winner
        genome_path = genome_name + ".pkl"
        with open(genome_path, "rb") as f:
            genome = pickle.load(f)
        self.field.update_grid(self.snake, self.fruit)
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.snake_view = Field(3,3)

    def get_input(self):
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
        # fruit_smell = list(max(self.ROWS, self.COLS) * fruit_smell/np.linalg.norm(fruit_smell))
        head = self.snake.head()
        head_pos = [head[0] / self.ROWS, head[1] / self.COLS]

        # Up til here there are 8 inputs
        output = self.net.activate(
            selfception + fruit_smell.tolist() + head_pos #+ self.snake.direction.tolist()
        )
        o = output.index(max(output))

        # THE REAL ONE
        if o == 0:
            self.snake.direction[1] = 1
            self.snake.direction[0] = 0
        elif o == 1:
            self.snake.direction[0] = -1
            self.snake.direction[1] = 0
        elif o == 2:
            self.snake.direction[1] = -1
            self.snake.direction[0] = 0
        elif o == 3:
            self.snake.direction[0] = 1
            self.snake.direction[1] = 0
        
        n = 0
        m = 0
        self.snake_view.grid = np.array(selfception[:4] + [-2] + selfception[4:]).reshape((3,3))
        self.fruit_smell = fruit_smell/np.linalg.norm(fruit_smell)
        self.head_pos = head_pos

def snake_vision_color(n):
        if abs(n) < 10e-3:
            return (100,100,100)
        elif n > 0:
            return (0,int(min(n*250, 250)),0)
        else:
            return (int(min(abs(n)*250, 250)),0,0)

def main():
    # Initializes game values
    def play():
        def draw_window(win, game):
            win.fill((0,0,0))
            game.draw(win, GRID_SPACE=SQUARE_WIDTH)
            direc = (GRID_WIDTH/2)* game.fruit_smell[0], (GRID_WIDTH/2)* game.fruit_smell[1]
            pygame.draw.rect(win, (200,200,200), (GRID_WIDTH+1, 1, SQUARE_WIDTH - 2, WIN_HEIGHT - 2))
            game.snake_view.draw(
                win, 
                GRID_SPACE=GRID_WIDTH//3, 
                colors=snake_vision_color, 
                offset_x=GRID_WIDTH+SQUARE_WIDTH
            )
            pygame.draw.line(
                win, 
                (0,255,0), 
                (SQUARE_WIDTH + 3*GRID_WIDTH/2, SQUARE_WIDTH*game.COLS/2), 
                (direc[1] + SQUARE_WIDTH + 3*GRID_WIDTH/2, SQUARE_WIDTH*game.COLS/2 + direc[0]),
                width=3
            )
            y_dist, x_dist = game.head_pos

            text = STAT_FONT.render(f"{x_dist:2f}, {y_dist:2f}", 1, (255,255,255))
            win.blit(text, (10+GRID_WIDTH+SQUARE_WIDTH, 10))


            text = STAT_FONT.render(f"HIGH SCORE: {game.HIGH_SCORE}", 1,(255,255,255))
            win.blit(text, (10,10))
            text = STAT_FONT.render(f"Score: {game.score}", 1,(255,255,255))
            win.blit(text, (10,10+text.get_height()))
            pygame.display.update()
        
        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        clock = pygame.time.Clock()
        #Initialize the game object
        game = AIGame(
            rows=ROWS,
            cols=COLS,
            genome_name=GENOME_NAME
        )
        run = True
        while run:
            clock.tick(8)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False    
                    pygame.quit()
                    quit()

            run = game.iteration()
            draw_window(win, game)
        game.save_high_score(path="AI_HIGH_SCORE.txt")
        clock.tick(1)

    if len(sys.argv) > 1:
        GENOME_NAME = sys.argv[1]
        COLS, ROWS = int(sys.argv[2]), int(sys.argv[3])
    else:
        GENOME_NAME = "juan"
        COLS, ROWS = 15,15
    
    pygame.font.init()
    STAT_FONT = pygame.font.SysFont("arial", 50)
    WIN_HEIGHT = 600
    WIN_WIDTH = int((COLS / ROWS) * WIN_HEIGHT * 2)
    SQUARE_WIDTH = min(WIN_HEIGHT // ROWS, WIN_WIDTH // COLS)
    GRID_WIDTH = WIN_WIDTH // 2
    WIN_WIDTH += SQUARE_WIDTH
    while True:
        SCORE = 0
        play()

if __name__ == "__main__":
    main()