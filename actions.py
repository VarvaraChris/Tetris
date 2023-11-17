import pygame
from field import Grid
from random import choice
from figures import LFigure, JFigure, IFigure, SFigure, TFigure, ZFigure, OFigure
from random import choice, randrange

class Abyss:
    def __init__(self):
        self.cell_size = 37
        self.color = (0, 0, 0)
    def get_position_abyss(self):
        return (randrange(10), randrange(4, 20))

class Game:
    def __init__(self):
        self.grid = Grid()
        self.abyss = Abyss()
        self.figures = [LFigure(), JFigure(), IFigure(), SFigure(), TFigure(), ZFigure(), OFigure()]
        self.current_figure = self.get_random_figure()
        self.next_figure = self.get_random_figure()
        self.position_abyss = self.get_random_abyss()
        self.count_abysses = 0
        self.things_of_abyss = 0
        self.game_over = False
        self.score = 0
    
    def get_random_abyss(self):
        position = self.abyss.get_position_abyss()
        while self.grid.is_empty(position[0], position[1]) == False:
            position = self.abyss.get_position_abyss()
        return position
    
    def draw_abyss(self, game_screen, position):
        cell_rect = pygame.Rect(position[0] * self.abyss.cell_size, position[1] * self.abyss.cell_size, self.abyss.cell_size - 1, self.abyss.cell_size - 1)
        pygame.draw.rect(game_screen, self.abyss.color, cell_rect)
        self.grid.grid[self.position_abyss[1]][self.position_abyss[0]] = 8

    def is_abyss(self):
        cells = self.current_figure.get_cell_positions()
        for cell in cells:
            if self.grid.grid[cell[1]][cell[0]] == 8:
                return True
        return False
    

    def get_record(self):
        with open('record.txt') as f:
            return int(f.readline())
    
    def set_record(self, record, score):
        rec = max(self.get_record(), score)
        with open('record.txt', 'w') as f:
            f.write(str(rec))

    def update_score(self, cleared_rows, things_of_abyss):
        if cleared_rows == 1:
            self.score += 100
        elif cleared_rows == 2:
            self.score += 300
        elif cleared_rows == 3:
            self.score += 500
        self.score += things_of_abyss


    def get_random_figure(self):
        if len(self.figures) == 0:
            self.figures = [LFigure(), JFigure(), IFigure(), SFigure(), TFigure(), ZFigure(), OFigure()]
        figure = choice(self.figures)
        self.figures.remove(figure)
        return figure
    
    def draw(self, game_screen, screen):
        self.board = game_screen
        self.grid.draw(game_screen)
        self.current_figure.draw(game_screen, 0, 0)
        self.next_figure.draw(screen, 465, 350)
        self.draw_abyss(game_screen, self.position_abyss)

    def reset(self):
        self.figures = [LFigure(), JFigure(), IFigure(), SFigure(), TFigure(), ZFigure(), OFigure()]
        for row in range(self.grid.num_rows):
            for col in range(self.grid.num_cols):
                self.grid.grid[row][col] = 0
        self.current_figure = self.get_random_figure()
        self.position_abyss = self.get_random_abyss()
        self.score = 0
    
    def stop(self):
        self.count_abysses +=1
        cells = self.current_figure.get_cell_positions()
        for cell in cells:
            self.grid.grid[cell[1]][cell[0]] = self.current_figure.color

        self.current_figure = self.next_figure
        self.next_figure = self.get_random_figure()
        self.grid.grid[self.position_abyss[1]][self.position_abyss[0]] = 0
        self.position_abyss = self.get_random_abyss()

        cleared_rows = self.grid.clear_row()
        self.update_score(cleared_rows, 0)

        if self.count_abysses == 5:
            self.things_of_abyss += 1
            self.count_abysses = 0
            self.update_score(0, self.things_of_abyss * 5)

        if self.is_overlay() == True:
            self.game_over = True


    def figure_inside(self):
        cells = self.current_figure.get_cell_positions()
        for cell in cells:
            if self.grid.is_inside(cell[0], cell[1]) == False:
                return False
        return True
    
    def is_overlay(self):
        cells = self.current_figure.get_cell_positions()
        for cell in cells:
            if self.grid.is_empty(cell[0], cell[1]) == False:
                return True
        return False
    

    def move_left(self):
        self.current_figure.move(-1, 0)
        if self.figure_inside() == False:
            self.current_figure.move(1, 0)
        elif self.is_overlay() == True:
            if self.is_abyss() == True:
                self.update_score(0, -3)
                self.current_figure = self.next_figure
                self.next_figure = self.get_random_figure()
            else:
                self.current_figure.move(1, 0)

    def move_right(self):
        self.current_figure.move(1, 0)
        if self.figure_inside() == False:
            self.current_figure.move(-1, 0)
        elif self.is_overlay() == True:
            if self.is_abyss() == True:
                self.update_score(0, -3)
                self.current_figure = self.next_figure
                self.next_figure = self.get_random_figure()
            else:
                self.current_figure.move(-1, 0)

    def move_down(self):
        self.current_figure.move(0, 1)
        if self.figure_inside() == False:
            self.current_figure.move(0, -1)
            self.stop()
        elif self.is_overlay() == True:
            if self.is_abyss() == True:
                self.update_score(0, -3)
                self.current_figure = self.next_figure
                self.next_figure = self.get_random_figure()
            else:
                self.current_figure.move(0, -1)
                self.stop()

    def rotate(self):
        self.current_figure.rotate()
        if self.figure_inside() == False:
            self.current_figure.reverse_rotation()
        elif self.is_overlay() == True:
            if self.is_abyss() == True:
                self.update_score(0, -3)
                self.current_figure = self.next_figure
                self.next_figure = self.get_random_figure()
            else:
                self.current_figure.reverse_rotation()

    