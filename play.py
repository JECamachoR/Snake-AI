from snake import *
import sys
import numpy as np
import math
class HumanGame(Game):
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if self.snake.direction[0] != -1:
                self.snake.direction[0] = 1
                self.snake.direction[1] = 0
        elif keys[pygame.K_LEFT]:
            if self.snake.direction[1] != 1:
                self.snake.direction[1] = -1
                self.snake.direction[0] = 0
        elif keys[pygame.K_UP]:
            if self.snake.direction[0] != 1:
                self.snake.direction[0] = -1
                self.snake.direction[1] = 0
        elif keys[pygame.K_RIGHT]:
            if self.snake.direction[1] != -1:
                self.snake.direction[1] = 1
                self.snake.direction[0] = 0
        if keys[pygame.K_SPACE]:
            self.snake.move()
            self.field.update_grid(self.snake,self.fruit)


COLORS = {
} # The colors used to display the game

def snake_vision_color(n):
    if abs(n) < 10e-3:
        return (100,100,100)
    elif n > 0:
        return (0,int(min(n*250, 250)),0)
    else:
        return (int(min(abs(n)*250, 250)),0,0)

def snake_vision_2(game, field):
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

def main():
    # Initializes game values
    def play():
        def draw_window(win, game, snake_view):
            win.fill((0,0,0))
            game.draw(win, GRID_SPACE=SQUARE_WIDTH)
            dist = game.fruit.position-game.snake.head()
            direc = (GRID_WIDTH/2)*dist/np.linalg.norm(dist)
            if NGRIDS > 1:
                pygame.draw.rect(win, (200,200,200), (GRID_WIDTH+1, 1, SQUARE_WIDTH - 2, WIN_HEIGHT - 2))
                snake_view.draw(
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
                head = game.snake.head() +1
                y_dist, x_dist = head[0] / game.ROWS, head[1] / game.COLS

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
        game = HumanGame(
            rows=ROWS,
            cols=COLS
        )
        if NGRIDS > 1:
            snake_view = Field(3, 3)
        else:
            snake_view = None
        run = True
        while run:
            clock.tick(4)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False    
                    pygame.quit()
                    quit()

            run = game.iteration()
            if NGRIDS == 2:
                snake_vision_2(game, snake_view)
            draw_window(win, game, snake_view)
        clock.tick(1)

    pygame.font.init()
    STAT_FONT = pygame.font.SysFont("arial", 50)
    SCORE = 0
    WIN_HEIGHT = 600
    if len(sys.argv) > 1:
        try:
            NGRIDS = int(sys.argv[1])
            COLS, ROWS = int(sys.argv[2]), int(sys.argv[3])
        except:
            print("Usage: play.py NGRIDS COLS ROWS")
    else:
        NGRIDS = 2
        COLS, ROWS = 9,9
    WIN_WIDTH = int((COLS / ROWS) * WIN_HEIGHT * NGRIDS)
    SQUARE_WIDTH = min(WIN_HEIGHT // ROWS, WIN_WIDTH // COLS)
    GRID_WIDTH = WIN_WIDTH // NGRIDS
    WIN_WIDTH += SQUARE_WIDTH
    play()

if __name__ == "__main__":
    main()