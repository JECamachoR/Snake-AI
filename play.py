from snake import *
pygame.font.init()
STAT_FONT = pygame.font.SysFont("arial", 50)
SCORE = 0
with open("HIGH_SCORE.txt", "r") as f:
    HIGH_SCORE = f.read()
    if len(HIGH_SCORE) > 0:
        HIGH_SCORE = int(HIGH_SCORE)
    else:
        HIGH_SCORE = 0
#print(HIGH_SCORE)

def record_hs():
    if SCORE > HIGH_SCORE:
        with open("HIGH_SCORE.txt", "w") as f:
            f.write(str(SCORE))

def draw_window(win, field, snake_view=None):
    win.fill((0,0,0))
    pygame.draw.line(win, (150, 150, 150), (GRID_WIDTH, 0), (GRID_WIDTH, GRID_WIDTH))
    field.draw(win)
    snake_view.draw(win, offset_x=GRID_WIDTH)
    text = STAT_FONT.render(f"HIGH SCORE: {HIGH_SCORE}", 1,(255,255,255))
    win.blit(text, (10,10+GRID_WIDTH))
    text = STAT_FONT.render(f"Score: {SCORE}", 1,(255,255,255))
    win.blit(text, (10,10+GRID_WIDTH+text.get_height()))
    pygame.display.update()

def main():
    # Initializes the screen
    center = ROWS // 2 + 1 if ROWS % 2 == 1 else ROWS // 2
    n_fruits = 5
    global HIGH_SCORE, SCORE
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    field = Field()
    snake = Snake(5,5)
    snake_view = Field()
    fruits = [Fruit(field.available_grid) for i in range(n_fruits)]
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(8)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False    
                pygame.quit()
                quit()
        # Get the direction the snake should turn from keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if snake.direction[1] != -1:
                snake.direction[1] = 1
                snake.direction[0] = 0
        elif keys[pygame.K_LEFT]:
            if snake.direction[0] != 1:
                snake.direction[0] = -1
                snake.direction[1] = 0
        elif keys[pygame.K_UP]:
            if snake.direction[1] != 1:
                snake.direction[1] = -1
                snake.direction[0] = 0
        elif keys[pygame.K_RIGHT]:
            if snake.direction[0] != -1:
                snake.direction[0] = 1
                snake.direction[1] = 0

        snake.move()
        if snake.bite():
            record_hs()
            run = False
        snake_head = snake.head()
        rem = None
        a = np.abs(snake_head- fruits[0].position)
        d = np.sqrt(np.square(a[0]) + np.square(a[1]))
        
        for fruit in fruits:
            if abs(snake_head[0] - fruit.position[0]) < 1 and abs(snake_head[1] - fruit.position[1]) < 1:
                rem = fruit
        if rem:
            fruits.remove(rem)
            fruits.append(Fruit(field.available_grid))
            snake.eat()
            SCORE += 1

        field.update_grid(snake, fruits)
        for x in range(ROWS):
            n_x = (x - snake_head[0] - center) %ROWS
            for y in range(ROWS):
                n_y = (y - snake_head[1] - center) % ROWS
                snake_view.grid[n_x, n_y] = field.grid[x,y]

        draw_window(win, field, snake_view)

if __name__ == "__main__":
    main()