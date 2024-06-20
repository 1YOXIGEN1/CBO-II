import pygame
import os
import random
import sys
from Image_button import Button

class Game:
    def __init__(self):
        pygame.init()

        # Настройки экрана
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = int(self.SCREEN_WIDTH * 0.8)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("СВО II")

        # Частота кадров
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.GRAVITY = 0.75
        self.TILE_SIZE = 40

        self.moving_left = False
        self.moving_right = False
        self.shoot = False
        self.paused = False

        # Загрузка изображений
        try:
            self.bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
            self.bg = pygame.image.load('img/backgraund/0.png').convert_alpha()
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            return

        self.back_gr = (144, 201, 120)
        self.red_line = (255, 0, 0)

        # Группы спрайтов
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        # Создание игроков и врагов
        self.player = self.Soldier(self, 'player', 200, 720, 1.5, 5, 30)
        self.enemy = self.Soldier(self, 'enemy', 400, 680, 1.5, 5, 30)
        self.enemy2 = self.Soldier(self, 'enemy', 600, 680, 1.5, 5, 30)
        self.enemy_group.add(self.enemy)
        self.enemy_group.add(self.enemy2)

        self.bg_music()

    def draw_back_graund(self):
        self.screen.fill(self.back_gr)
        pygame.draw.line(self.screen, self.red_line, (0, 690), (self.SCREEN_WIDTH, 690))
        self.screen.blit(self.bg, (0, 0))

    def bg_music(self):
        try:
            pygame.mixer.music.load('sound/Muz.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except pygame.error as e:
            print(f"Ошибка загрузки музыки: {e}")

    def sound_shoot(self):
        try:
            sound_shoot = pygame.mixer.Sound('sound/shoot.mp3')
            sound_shoot.set_volume(0.2)
            sound_shoot.play()
        except pygame.error as e:
            print(f"Ошибка загрузки звука: {e}")

    class Soldier(pygame.sprite.Sprite):
        def __init__(self, game, char_type, x, y, scale, speed, ammo):
            pygame.sprite.Sprite.__init__(self)
            self.game = game
            self.alive = True
            self.char_type = char_type
            self.speed = speed
            self.ammo = ammo
            self.start_ammo = ammo
            self.shoot_cooldown = 0
            self.health = 100
            self.max_health = self.health
            self.direction = 1
            self.speed_y = 0
            self.jump = False
            self.in_air = True
            self.flip = False
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

            # переменные для ии
            self.move_counter = 0
            self.vision = pygame.Rect(0, 0, 150, 20)
            self.idling = False
            self.idling_counter = 0

            # загрузка всех изображений для персонажей
            animation_types = ['Idle', 'run', 'jump', 'death']
            for animation in animation_types:
                # обновляем временный список изображений
                temp_list = []
                # считываем кол-во изображений в папке
                num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            self.update_animation()
            self.check_alive()
            # обновляем перезарядку
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1

        def move(self, moving_left, moving_right):
            # обновляем перемещение
            dx = 0
            dy = 0

            # перемещение при движении влево или вправо
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1

            # прыжок
            if self.jump == True and self.in_air == False:
                self.speed_y = -11
                self.jump = False
                self.in_air = True

            # сила гравитации
            self.speed_y += self.game.GRAVITY
            if self.speed_y > 10:
                self.speed_y
            dy += self.speed_y

            # ограничение по полу
            if self.rect.bottom + dy > 735:
                dy = 735 - self.rect.bottom
                self.in_air = False

            # обновление положения модельки
            self.rect.x += dx
            self.rect.y += dy

        def shoot(self):
            if self.shoot_cooldown == 0 and self.ammo > 0:
                self.shoot_cooldown = 20
                bullet = self.game.Bullet(self.game, self.rect.centerx + (0.75 * self.rect.size[0] * self.direction),
                                     self.rect.centery - 10, self.direction)
                self.game.bullet_group.add(bullet)
                self.ammo -= 1

        def ai(self):
            if self.alive and self.game.player.alive:
                if self.idling == False and random.randint(1, 200) == 1:
                    self.update_action(0)  # стойка
                    self.idling = True
                    self.idling_counter = 50
                # если игрок находится в поле зрения врага
                if self.vision.colliderect(self.game.player.rect):
                    self.update_action(0)  # стойка
                    self.shoot()
                    self.game.sound_shoot()
                else:
                    if self.idling == False:
                        if self.direction == 1:
                            ai_moving_right = True
                        else:
                            ai_moving_right = False
                        ai_moving_left = not ai_moving_right
                        self.move(ai_moving_left, ai_moving_right)
                        self.update_action(1)  # бег
                        self.move_counter += 1
                        # обновление зрения ии во время бега
                        self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                        if self.move_counter > self.game.TILE_SIZE:
                            self.direction *= -1
                            self.move_counter *= -1
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False

        def update_animation(self):
            # обновление анимации
            ANIMATION_COOLDOWN = 100
            # обновление изображения в зависимости от текущего кадра
            self.image = self.animation_list[self.action][self.frame_index]
            # проверка на необходимость обновления кадра
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            # возвращение к началу, если анимация закончилась
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

        def update_action(self, new_action):
            # проверка на новую анимацию
            if new_action != self.action:
                self.action = new_action
                # обновление настроек анимации
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def check_alive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(3)

        def draw(self):
            self.game.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, game, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.game = game
            self.speed = 10
            self.image = self.game.bullet_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction

        def update(self):
            self.rect.x += (self.direction * self.speed)
            if self.rect.right < 0 or self.rect.left > self.game.SCREEN_WIDTH:
                self.kill()

            # столкновение с персонажами
            if pygame.sprite.spritecollide(self.game.player, self.game.bullet_group, False):
                if self.game.player.alive:
                    self.game.player.health -= 5
                    self.kill()
            for enemy in self.game.enemy_group:
                if pygame.sprite.spritecollide(enemy, self.game.bullet_group, False):
                    if enemy.alive:
                        enemy.health -= 25
                        self.kill()

    def game_menu(self):
        from Main_menu import play_music




        esc_sound = pygame.mixer.Sound('soun/Button 4.wav')

        play2_button = Button(self.SCREEN_WIDTH / 2 - (252 / 2), 270, 252, 74, "", 'image/продолжить 1.png',
                              'image/продолжить 3.png', 'soun/Button 4.wav')
        exit2_button = Button(self.SCREEN_WIDTH / 2 - (252 / 2), 370, 252, 74, "", 'image/выход 3.png', 'image/выход 2.png',
                              'soun/Button 4.wav')

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.draw_back_graund()

            bord_rect = self.bg.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2))
            self.screen.blit(self.bg, bord_rect)

            font = pygame.font.Font(None, 72)
            text_surface = font.render("CBO II ПАУЗА", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH / 2, 220))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():

                from Main_menu import main_menu
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == play2_button:
                    self.paused = False

                if event.type == pygame.USEREVENT and event.button == exit2_button:
                    running = False
                    play_music()
                    main_menu()
                if event.type == pygame.USEREVENT and event.button == play2_button:
                    self.paused = False
                    running = False


                for btn in [play2_button, exit2_button]:
                    btn.handel_event(event)
            for btn in [play2_button, exit2_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.screen)

            pygame.display.flip()

    def run(self):
        run = True
        while run:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.moving_left = True
                    if event.key == pygame.K_d:
                        self.moving_right = True
                    if event.key == pygame.K_SPACE:
                        self.shoot = True
                        self.sound_shoot()
                    if event.key == pygame.K_w and self.player.alive:
                        self.player.jump = True
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
                        self.game_menu()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.moving_left = False
                    if event.key == pygame.K_d:
                        self.moving_right = False
                    if event.key == pygame.K_SPACE:
                        self.shoot = False

            if not self.paused:
                self.draw_back_graund()

                self.player.update()
                self.player.draw()

                for enemy in self.enemy_group:
                    enemy.ai()
                    enemy.update()
                    enemy.draw()

                self.bullet_group.update()
                self.bullet_group.draw(self.screen)

                if self.player.alive:
                    if self.shoot:
                        self.player.shoot()
                    if self.player.in_air:
                        self.player.update_action(2)  # прыжок
                    elif self.moving_left or self.moving_right:
                        self.player.update_action(1)  # бег
                    else:
                        self.player.update_action(0)  # стойка
                    self.player.move(self.moving_left, self.moving_right)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()