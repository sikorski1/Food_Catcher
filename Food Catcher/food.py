import pygame


class Food(pygame.sprite.Sprite):
    def __init__(self, type, pos, speed):
        super().__init__()
        if type == "apple":
            self.image = pygame.image.load("graphics/apple.png")
            self.type = "apple"
        elif type == "banana":
            self.image = pygame.image.load("graphics/banana.png")
            self.type = "banana"
        elif type == "pear":
            self.image = pygame.image.load("graphics/pear.png")
            self.type = "pear"
        else:
            self.image = pygame.image.load("graphics/bomb.png")
            self.type = "bomb"
        self.rect = self.image.get_rect(bottomleft=(pos))
        self.speed = speed

    def food_movement(self):
        self.rect.y += self.speed

    def food_killer(self):
        if self.rect.y >= 1000:
            self.kill()

    def update(self):
        self.food_movement()
        self.food_killer()
