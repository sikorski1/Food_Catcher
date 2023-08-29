import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, speed, border_x):
        super().__init__()
        self.player_standing = pygame.image.load("graphics/player1.png").convert_alpha()
        self.player_eating = pygame.image.load("graphics/player2.png").convert_alpha()
        self.player_bomb = pygame.image.load("graphics/player_bomb.png").convert_alpha()
        self.image = self.player_standing
        self.current_sprite = 0
        self.rect = self.image.get_rect(midbottom=(pos))
        self.speed = speed
        self.border_x = border_x

    def player_movement(self):
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_press[pygame.K_LEFT]:
            self.rect.x -= self.speed

    def player_border(self):
        if self.rect.right >= self.border_x:
            self.rect.right = self.border_x
        if self.rect.left <= 0:
            self.rect.left = 0

    def update(self):
        self.player_movement()
        self.player_border()
