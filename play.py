from snake import *

def draw_window(win, field, snake_view=None):
    field.draw(win)
    snake_view.draw(win, offset_x=GRID_WIDTH)
    pygame.display.update()

def main():
    # Initializes the screen
    center = ROWS // 2 + 1 if ROWS % 2 == 1 else ROWS // 2
    n_fruits = 5
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    win.fill((0,0,0))
    pygame.draw.line(win, (150, 150, 150), (GRID_WIDTH, 0), (GRID_WIDTH, GRID_WIDTH))
    field = Field()
    snake = Snake(5,5)
    snake_view = Field()
    fruits = [Fruit(field.available_grid) for i in range(n_fruits)]
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(5)
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

        field.update_grid(snake, fruits)
        for x in range(ROWS):
            n_x = (x-snake_head[0] -center) %ROWS
            for y in range(ROWS):
                n_y = (y-snake_head[1] - center) % ROWS
                snake_view.grid[n_x, n_y] = field.grid[x,y]

        draw_window(win, field, snake_view)

if __name__ == "__main__":
    main()