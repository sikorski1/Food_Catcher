import pygame
from sys import exit
from player import Player
from food import Food
from random import choice, randint
import time


class Game:
    def __init__(self):
        self.background = pygame.image.load("graphics/backgroundx100.png")
        self.player_sprite = Player((screen_width / 2, screen_height), 4, screen_width)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.food = pygame.sprite.Group()
        self.score = 0
        self.font = pygame.font.Font("font/Pixeled.ttf", 20)
        self.eating_animation = False
        self.bomb_animation = False
        self.HP_image = pygame.image.load("graphics/player1.png").convert_alpha()
        self.HP_image = pygame.transform.scale(self.HP_image, (30, 30))
        self.HP = 3

        self.FOODSPAWNER = pygame.USEREVENT + 1
        pygame.time.set_timer(self.FOODSPAWNER, randint(2400, 3000))

        self.t0 = time.time()
        self.t1 = 0

        self.score_sound = pygame.mixer.Sound("sound/score_sound.mp3")
        self.score_sound.set_volume(0.1)
        self.bomb_explosion = pygame.mixer.Sound("sound/bomb_explosion.wav")
        self.bomb_explosion.set_volume(0.1)
        self.food_dropped = pygame.mixer.Sound("sound/food_dropped.wav")
        self.food_dropped.set_volume(0.1)

    def display_background(self):
        screen.blit(self.background, (0, 0))

    def food_setup(self):
        self.food.add(Food(choice(["apple", "apple", "banana", "banana", "pear", "pear", "bomb"]),
                           (randint(0, screen_width - 40), -100), 3))

    def eating(self):
        if self.food:
            for food in self.food.sprites():
                if pygame.sprite.spritecollide(food, self.player, False):
                    if abs(food.rect.bottom - self.player_sprite.rect.top) < 50:
                        if food.type == "bomb":
                            self.HP -= 1
                            self.bomb_animation = True
                            self.bomb_explosion.play()
                            food.kill()
                        else:
                            self.score += 100
                            self.eating_animation = True
                            self.score_sound.play()
                            food.kill()

                elif food.type != "bomb" and food.rect.center[1] >= 800:
                    self.HP -= 1
                    self.food_dropped.play()
                    food.kill()

    def animation(self):
        if self.eating_animation:
            self.player_sprite.image = self.player_sprite.player_eating
            self.player_sprite.current_sprite += 0.1
            if self.player_sprite.current_sprite > 2:
                self.player_sprite.image = self.player_sprite.player_standing
                self.player_sprite.current_sprite = 0
                self.eating_animation = False
        if self.bomb_animation:
            self.player_sprite.image = self.player_sprite.player_bomb
            self.player_sprite.current_sprite += 0.1
            if self.player_sprite.current_sprite > 2:
                self.player_sprite.image = self.player_sprite.player_standing
                self.player_sprite.current_sprite = 0
                self.bomb_animation = False

    def display_score(self):
        score_surf = self.font.render("Score: {}".format(self.score), True, "White")
        score_rect = score_surf.get_rect(midtop=(screen_width / 2, 5))
        screen.blit(score_surf, score_rect)

    def HP_setup(self):
        for i in range(self.HP):
            rect = self.HP_image.get_rect(topleft=(15 + (self.HP_image.get_size()[0] + 20) * i, 23))
            screen.blit(self.HP_image, rect)

    def game_over(self):
        if self.HP <= 0:
            self.game_reset()

    def game_changes(self):
        self.t1 = time.time()
        dt = self.t1 - self.t0
        if 9.95 <= abs(dt) <= 10.05:
            pygame.time.set_timer(self.FOODSPAWNER, randint(1200, 2400))
        elif 19.95 <= abs(dt) <= 20.05:
            pygame.time.set_timer(self.FOODSPAWNER, randint(1000, 1800))
        elif 29.95 <= abs(dt) <= 30.05:
            pygame.time.set_timer(self.FOODSPAWNER, randint(800, 1200))
        elif 39.95 <= abs(dt) <= 40.05:
            pygame.time.set_timer(self.FOODSPAWNER, randint(600, 1000))
        elif 49.95 <= abs(dt) <= 50.05:
            pygame.time.set_timer(self.FOODSPAWNER, randint(500, 800))
        elif 59.95 <= abs(dt) <= 60.05:
            pygame.time.set_timer(self.FOODSPAWNER, randint(500, 600))

    def game_reset(self):
        self.HP = 3
        self.score = 0
        pygame.time.set_timer(self.FOODSPAWNER, randint(2400, 3000))
        self.food.empty()
        self.t0 = self.t1

    def run(self):
        self.display_background()
        self.player.draw(screen)
        self.food.draw(screen)
        self.HP_setup()
        self.player.update()
        self.animation()
        self.food.update()
        self.eating()
        self.display_score()
        self.game_over()
        self.game_changes()


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()

    screen_width, screen_height = 600, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Food Catcher")
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == game.FOODSPAWNER:
                game.food_setup()
        game.run()

        pygame.display.update()
        clock.tick(120)
