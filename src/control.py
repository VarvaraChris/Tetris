import pygame, sys
from actions import Game
from random import choice
from button import Button
import os

pygame.init()

images = os.listdir('image')

#display surface
screen = pygame.display.set_mode((780, 800))
game_screen = pygame.Surface((370, 740))
game_bg = pygame.image.load('image/'+choice(images)).convert()
bg = pygame.image.load('background/bg.jpg').convert()

pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game = Game()
button = Button()

font = pygame.font.Font('font/TakashimuraRegular.ttf', 60) #шрифт по умолчанию
score = font.render("Score", True, (0, 0, 0))
next = font.render("Next figure", True, (0, 0, 0))
record = font.render("Record", True, (0, 0, 0))
movement = pygame.USEREVENT
pygame.time.set_timer(movement, 200) #событие, которое повторяется каждые 200 мс

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #выход из игры
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_over(pygame.mouse.get_pos()) and button.count_press > 0:
                button.count_press -= 1
                game.grid.drop_cells()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.set_record(game.get_record, game.score)
                game.game_over = False
                game.reset()
                button.count_press = 5
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == movement and game.game_over == False:
            game.move_down()

    cur_score = font.render(str(game.score), True, (0, 0, 0))
    cur_record = font.render(str(game.get_record()), True, (0, 0, 0))

    screen.blit(bg, (0, 0))
    screen.blit(game_screen, (50, 30))
    game_screen.blit(game_bg, (0, 0))

    screen.blit(record, (560, 60))
    screen.blit(cur_record, (570, 130))

    screen.blit(next, (515, 220))

    screen.blit(score, (570, 485))
    screen.blit(cur_score, (580, 555))
    
    button.draw(screen)
    game.draw(game_screen, screen)

    #обновляет часть экрана или весь экран, чтобы отобразить изменения, сделанные в игровом коде
    pygame.display.update()
    #цикл while выполняется 60 раз в секунду(60 кадров/сек)
    clock.tick(60)
