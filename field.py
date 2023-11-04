import pygame
from random import choice

class Colors:
    green = (50, 153, 50)
    red = (255, 50, 50)
    orange = (255, 102, 0)
    yellow = (255, 204, 0)
    purple = (128, 128, 255)
    blue_green = (51, 153, 102)
    blue = (0, 204, 255)
    magenta = (255,0,230)
    yellow = (255,255,0)
    lime = (180,255,100)
    @classmethod
    def get_cell_colors(cls):
        return [(0, 0, 0), cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.blue_green, cls.blue, (0, 0, 0), cls.magenta, cls.yellow, cls.lime]
    
    
class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 37
        self.colors = Colors.get_cell_colors()
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
    
    def is_inside(self, x, y):
        if x >= 0 and x < self.num_cols and y >= 0 and y < self.num_rows:
            return True
        return False
    
    def is_empty(self, x, y):
        return self.grid[y][x] == 0
    
    def is_row_full(self, row):
        for col in range(self.num_cols):
            if self.grid[row][col] == 0:
                return False
        return True
    
    def clear_row(self):
        filled = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                for col in range(self.num_cols):
                    self.grid[row][col] = 0
                filled += 1
            elif filled > 0:
                for col in range(self.num_cols):
                    self.grid[row + filled][col] = self.grid[row][col]
                    self.grid[row][col] = 0
        return filled
    
    def drop_cells(self):
        for col in range(self.num_cols):
            read_row = self.num_rows - 1
            write_row = self.num_rows - 1

            # Двигаемся снизу вверх по каждому столбцу
            while read_row >= 0:
            # Если текущий элемент не пустой
                if self.grid[read_row][col] != 0 and self.grid[read_row][col] != 8:
                    # Перемещаем блок вниз, если возможно
                    self.grid[write_row][col] = self.grid[read_row][col]
                    if write_row != read_row:
                        self.grid[read_row][col] = 0
                    write_row -= 1
                read_row -= 1

    def draw(self, game_screen):
        for row in range(self.num_rows):
           for col in range(self.num_cols):
                cell_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                cell_value = self.grid[row][col]
                pygame.draw.rect(game_screen, (26, 31, 40), cell_rect, 1)
                if cell_value != 0:
                    cell_rect1 = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                    pygame.draw.rect(game_screen, self.colors[cell_value], cell_rect1)
