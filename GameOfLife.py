# RULES Conway's Game of Life
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

import pygame
import random

pygame.init()

black = (0, 0, 0) # RGB
white = (255, 255, 255) # RGB

# 800 x 800
width, height = 800, 800
cell = 20
grid_width = width // cell
grid_height = height // cell
FPS = 60

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

# Function for random generation of automata
def gen(num):
    return set([(random.randrange(0, grid_height), random.randrange(0, grid_width)) for _ in range(num)])

# Grid drawing (col = columns generated with screen height and rig = rows for screen width)
def draw_grid(positions):
    for position in positions:
        col, rows = position
        top_left = (col * cell, rows * cell)
        pygame.draw.rect(screen, black, (*top_left, cell, cell))

    for rows in range(grid_height):
        pygame.draw.line(screen, black, (0, rows * cell), (width, rows * cell))

    for col in range(grid_width):
        pygame.draw.line(screen, black, (col * cell, 0), (col * cell, height))


def grid(positions):
    all_nearcells = set()
    new_positions = set()

    for position in positions:
        near_cells = calculate_nearcells(position)
        all_nearcells.update(near_cells)

        near_cells = list(filter(lambda x: x in positions, near_cells))

        if len(near_cells) in [2, 3]:
            new_positions.add(position)

    for position in all_nearcells:
        near_cells = calculate_nearcells(position)
        near_cells = list(filter(lambda x: x in positions, near_cells))

        if len(near_cells) == 3:
            new_positions.add(position)

    return new_positions

# Rules for living or dead automatons 
def calculate_nearcells(pos):
    x, y = pos
    near_cell = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > grid_width:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > grid_height:
                continue
            if dx == 0 and dy == 0:
                continue

            near_cell.append((x + dx, y + dy))

    return near_cell

# Recall all previous functions and insert functions for insertion and deletion of automata
def main():
    running = True
    playing = False
    count = 0
    update_freq = 120

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = grid(positions)

        pygame.display.set_caption("Active" if playing else "Inactive")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // cell
                rig = y // cell
                pos = (col, rig)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * grid_width)

        screen.fill(white)
        draw_grid(positions)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()
