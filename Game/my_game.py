import pygame
import sprite
from pygame import *
import sys
import random
from random import randint

pygame.init()
pygame.mixer.init()

#Параметры окна
win_width = 800
win_height = 530
window = display.set_mode((win_width, win_height))

#Фоновое изображение и звук выстрела
background = transform.scale(image.load('all_sprites/background.png'), (win_width, win_height))
shoot_sound = pygame.mixer.Sound('all_sprites/shoot_sound.mp3')

#Название иггры
pygame.display.set_caption('Space battle')


#Родительский класс
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#Класс игрока
class Player(GameSprite):
    #метод движения игрока с запретами выхода за пределы окна
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            if self.rect.y > 0:
                self.rect.y -= self.speed

        if keys[K_DOWN]:
            if self.rect.y < win_height - self.rect.height:
                self.rect.y += self.speed

        if keys[K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed

        if keys[K_RIGHT]:
            if self.rect.x < win_width - self.rect.width:
                self.rect.x += self.speed

    #метод для выстрела из правой турели
    def right_fire(self):
        bullet = Bullet('all_sprites/bullet.png', self.rect.right - 50, self.rect.top,
                        50, 50, 15)
        bullets.add(bullet)
        shoot_sound.play()

    #метод для выстрела из левой турели
    def left_fire(self):
        bullet = Bullet('all_sprites/bullet.png', self.rect.left - 10, self.rect.top,
                        50, 50, 15)
        bullets.add(bullet)
        shoot_sound.play()

#Класс врага
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.direction = random.choice(['right', 'left']) #список для рандомизации движения врагов

#Движения врага
    def move(self):
        if self.rect.x < 0:
            self.direction = 'right'
        if self.rect.x > win_width - 120:
            self.direction = 'left'

        if self.direction == 'right':
            self.rect.x += self.speed
        if self.direction == 'left':
            self.rect.x -= self.speed

    def update(self):
        self.move()

#Класс пуль
class Bullet(GameSprite):
    def update(self, *args, **kwargs):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


#Генерация новых врагов
def handle_enemy_spawn():
    if len(enemies) < 5:
        new_enemy_x = random.randint(0, win_width - 120)
        new_enemy_y = random.randint(0, win_height - 400)
        new_enemy = Enemy('all_sprites/enemy.png', new_enemy_x, new_enemy_y, 120, 120, 5)
        enemies.add(new_enemy)

#Игрок
ship = Player('all_sprites/ship.png', 340, 400,
              120, 120, 10)

#Враг
enemy = Enemy('all_sprites/enemy.png', 340, 0,
              120, 120, 5)

#Группы врагов и пуль
bullets = sprite.Group()
enemies = sprite.Group()


#Основной цикл игры
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q: #выстрел из левой турели
            ship.left_fire()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w: #выстрел из правой турели
            ship.right_fire()
    window.blit(background, (0, 0))

    #Генерация новых врагов при столкновении с пулямий
    colliding_enemies = sprite.groupcollide(enemies, bullets, True, True)
    for enemy in colliding_enemies.keys():
        handle_enemy_spawn()

    handle_enemy_spawn()

    enemies.update()
    enemies.draw(window)

    bullets.update()
    bullets.draw(window)

    ship.move()
    ship.reset()

    display.update()
    pygame.time.delay(35)

pygame.quit()
