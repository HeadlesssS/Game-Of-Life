import pygame as py
import random

py.init()

WHITE =(255,255,255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
CYAN = (20, 200, 180)       
ORANGE = (255, 140, 0)

WIDTH, HEIGHT = 1800, 1000
TILE_SIZE = 30
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = py.display.set_mode((WIDTH, HEIGHT),py.RESIZABLE)
clock = py.time.Clock()

def gen(num):
    return set(
        (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
        for _ in range(num)
    )

def drawGrid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        py.draw.rect(screen, GREY, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        py.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        py.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def adjustGrid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = neighbours(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    
    for position in all_neighbors:
        neighbors = neighbours(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)
    
    return new_positions

def neighbours(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
    
    return neighbors

def draw_help():
    font = py.font.SysFont("consolas", 28, bold=True)
    help_lines = [
        "GAME OF LIFE - CONTROLS",
        "",
        "[SPACE]  Start/Pause",
        "[C]      Clear grid",
        "[G]      Generate random cells",
        "[Click]  efw cell alive/dead"
    ]
    padding = 16
    line_height = font.get_height()
    box_width = max(font.size(line)[0] for line in help_lines) + 2 * padding
    box_height = len(help_lines) * line_height + 2 * padding
    s = py.Surface((box_width, box_height), py.SRCALPHA)
    s.fill((40, 40, 40, 200))
    screen.blit(s, (30, 30))
    for i, line in enumerate(help_lines):
        color = CYAN if i == 0 else ORANGE
        text = font.render(line, True, color)
        screen.blit(text, (30 + padding, 30 + padding + i * line_height))

def main():
    running = True
    playing = False
    count = 0
    update_freq = 40

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        
        if count >= update_freq:
            count = 0
            positions = adjustGrid(positions)

        py.display.set_caption("Playing" if playing else "Paused")

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            
            if event.type == py.MOUSEBUTTONDOWN:
                x, y = py.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    playing = not playing
                
                if event.key == py.K_c:
                    positions = set()
                    playing = False
                    count = 0
                
                if event.key == py.K_g:
                    positions = gen(random.randrange(4, 20) * GRID_WIDTH)
    
        screen.fill(WHITE)
        drawGrid(positions)
        
        if not playing:
            draw_help()
        py.display.update()


    py.quit()

if __name__ == "__main__":
    main()