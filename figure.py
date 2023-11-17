from field import Colors
import pygame
from random import choice
           
class Figure:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 37
        self.rotation_state = 0
        self.x = 3
        self.y = 0
        self.color = choice([1, 2, 3, 4, 5, 6, 7, 9, 10, 11])
        self.colors = Colors.get_cell_colors()
	
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def get_cell_positions(self):
        cells = self.cells[self.rotation_state]
        moved_cells = []
        for cell in cells:
            position = cell[0]+ self.x, cell[1] + self.y
            moved_cells.append(position)
        return moved_cells
    
    def draw(self, game_screen, offset_x, offset_y):
        cells = self.get_cell_positions()
        for cell in cells:
            cell_rect = pygame.Rect(cell[0] * self.cell_size + offset_x,
                                    cell[1] * self.cell_size + offset_y,
                                    self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(game_screen, self.colors[self.color], cell_rect)
    
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0 

    def reverse_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1