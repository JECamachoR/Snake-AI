from snake import *
import pygame_menu
import sys
import numpy as np

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
            self.field.update_grid(self.snake,self.fruits)


COLORS = {
} # The colors used to display the game

def snake_vision_color(n):
    if abs(n) < 10e-3:
        return (100,100,100)
    elif n > 0:
        return (0,int(min(n*250, 250)),0)
    else:
        return (int(min(abs(n)*250, 250)),0,0)

def get_dir_value(array):
    c = len(array)
    for val in array:
        if np.abs(val) > 1e-3:
            n = val * (c / array.shape[0])
            return n
        c -= 1
    return 0
def snake_vision(game, field, i):
    view_dirs = [
        np.array([0,1])
    ]
    shift = game.CENTER - game.snake.head()
    grid = np.roll(game.field.grid, shift=(shift[0], shift[1]), axis=(0,1))

    field.grid[2,1] = get_dir_value(grid[game.CENTER[0]+1:, game.CENTER[1]])    # ABAJO 1
    field.grid[0,1] = get_dir_value(np.flip(grid[:game.CENTER[0], game.CENTER[1]]))      # ARRIBA 1
    field.grid[1,0] = get_dir_value(np.flip(grid[game.CENTER[0], :game.CENTER[1]]))      # IZQUIERDA
    field.grid[1,2] = get_dir_value(grid[game.CENTER[0], game.CENTER[1]+1:])    # DERECHA
    field.grid[0,0] = get_dir_value(grid[i[0]])                                 # SUPERIOR IZQUIERDA 3
    field.grid[2,2] = get_dir_value(grid[i[1]])                                 # INFERIOR DERECHA 1
    field.grid[0,2] = get_dir_value(grid[i[2]])                                 # SUPERIOR DERECHA 3
    field.grid[2,0] = get_dir_value(grid[i[3]])                                 # INFERIOR IZQUIERDA 1
    field.grid[1,1] = -2

def main():
    # Initializes game values
    def play():
        def draw_window(win, game, snake_view):
            win.fill((0,0,0))
            game.draw(win, GRID_SPACE=SQUARE_WIDTH)
            if NGRIDS > 1:
                pygame.draw.rect(win, (200,200,200), (GRID_WIDTH+1, 1, SQUARE_WIDTH - 2, WIN_HEIGHT - 2))
                snake_view.draw(win, GRID_SPACE=GRID_WIDTH//3, colors=snake_vision_color, offset_x=GRID_WIDTH+SQUARE_WIDTH)
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
        i = np.diag_indices(min(game.ROWS, game.COLS))
        i_1 = (np.flip(i[0][:game.CENTER[0]]), np.flip(i[1][:game.CENTER[1]]))      # SUPERIOR IZQUIERDA
        i_2 = (i[0][game.CENTER[0]+1:], i[0][game.CENTER[1]+1:])                    # INFERIOR DERECHA
        i = (i[0], np.flip(i[1]))
        i_3 = (np.flip(i[0][:game.CENTER[0]]), np.flip(i[1][:game.CENTER[1]]))      # INFERIOR IZQUIERDA
        i_4 = (i[0][game.CENTER[0]+1:], i[1][game.CENTER[1]+1:])                    # SUPERIOR DERECHA
        i = [i_1, i_2, i_3, i_4]
        while run:
            clock.tick(2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False    
                    pygame.quit()
                    quit()

            run = game.iteration()
            if NGRIDS == 2:
                snake_vision(game, snake_view, i)
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