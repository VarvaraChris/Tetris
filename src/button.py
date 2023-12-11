import pygame

class Button:
    def __init__(self):
        self.width = 200
        self.height = 65
        self.x = 555
        self.y = 665
        self.shadow_color = (26, 31, 40)
        self.color = (50, 153, 50)
        self.hover_color = (51, 153, 102)
        self.text_color = (0, 0, 0)
        self.count_press = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.shadow_color, (self.x + 5, self.y + 5, self.width, self.height))
        if self.is_over(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        font = pygame.font.Font('font/TakashimuraRegular.ttf', 50)
        text_surface = font.render(f'Gravity: {self.count_press}', True, self.text_color)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) / 2, self.y + (self.height - text_surface.get_height()) / 2))

    def is_over(self, pos):
        return self.rect.collidepoint(pos)