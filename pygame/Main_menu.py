import pygame
import sys
from Image_button import Button
from main import Game


pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("СВО II - Menu")
background_images = [
    pygame.image.load('image/Задник меню.png'),
    pygame.image.load('image/Задник меню 2.png'),
    pygame.image.load('image/Задник меню 3.png'),
    pygame.image.load('image/Задник меню 4.png')
]
background_positions = [0, WIDTH, WIDTH * 2, WIDTH * 3]

def draw_moving_background():
    global background_positions

    speed = 1
    for i in range(4):
        screen.blit(background_images[i], (background_positions[i], 0))
        background_positions[i] -= speed

    for i in range(4):
        if background_positions[i] <= -WIDTH:
            background_positions[i] = background_positions[(i - 1) % 4] + WIDTH

bord2 = pygame.image.load('image/граница ползунка.png')
bord2_WIDTH = 310
bord2_HEIGHT = 33
bord2 = pygame.transform.scale(bord2, (bord2_WIDTH, bord2_HEIGHT))

exit_WIDTH = 1000
exit_HEIGHT = 800
exit_bg = pygame.image.load('image/Задник выход.png')
bord_WIDTH = 500
bord_HEIGHT = 600
bord1_WIDTH = 500
bord1_HEIGHT = 600
bord1 = pygame.image.load('image/граница 2.png')
bord = pygame.image.load('image/граница.png')
bord = pygame.transform.scale(bord, (bord_WIDTH, bord_HEIGHT))

def play_music():
    pygame.mixer.music.load('sound/Трек для меню.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

play_music()  # Начало воспроизведения музыки при запуске

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, slider_img, hover_img, fill_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.slider_img = pygame.image.load(slider_img)
        self.hover_img = pygame.image.load(hover_img)
        self.fill_color = fill_color
        self.grabbed = False
        self.hovered = False

        # Увеличенные размеры для ползунка
        self.slider_width = 20
        self.slider_height = 20

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.hovered = True
                if self.grabbed:
                    self.move_slider(event.pos[0])
            else:
                self.hovered = False

    def move_slider(self, x):
        if x < self.rect.left:
            x = self.rect.left
        elif x > self.rect.right:
            x = self.rect.right
        self.value = self.min_val + (self.max_val - self.min_val) * ((x - self.rect.left) / self.rect.width)
        pygame.mixer.music.set_volume(self.value)

    def draw(self, surface):
        # Заполнение желтой области
        fill_width = (self.value - self.min_val) / (self.max_val - self.min_val) * (self.rect.width - 20)
        fill_rect = pygame.Rect(self.rect.left + 10, self.rect.top + 10, fill_width, self.rect.height - 20)
        pygame.draw.rect(surface, self.fill_color, fill_rect)

        # Отрисовка ползунка
        if self.hovered:
            slider_img = self.hover_img
        else:
            slider_img = self.slider_img
        slider_img = pygame.transform.scale(slider_img, (self.slider_width, self.slider_height))
        slider_x = self.rect.left + fill_width + 10 - slider_img.get_width() // 2
        surface.blit(slider_img, (slider_x, self.rect.centery - slider_img.get_height() // 2))


def main_menu():
    esc_sound = pygame.mixer.Sound('soun/Button 4.wav')

    play_button = Button(WIDTH / 2 - (252 / 2), 270, 252, 74, "", 'image/кнопка 3.png', 'image/кнопка.png', 'soun/Button 4.wav')
    setting_button = Button(WIDTH / 2 - (252 / 2), 370, 252, 74, "", 'image/настроки 1.png', 'image/настройки 3.png', 'soun/Button 4.wav')
    exit_button = Button(WIDTH / 2 - (252 / 2), 470, 252, 74, "", 'image/выход 3.png', 'image/выход 2.png', 'soun/Button 4.wav')

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_moving_background()

        bord_rect = bord.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(bord, bord_rect)

        font = pygame.font.Font(None, 72)
        text_surface = font.render("CBO II", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 220))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [play_button, setting_button, exit_button]:
                btn.handel_event(event)
            if event.type == pygame.USEREVENT and event.button == setting_button:
                settings()
            if event.type == pygame.USEREVENT and event.button == exit_button:
                exit_menu()
            if event.type == pygame.USEREVENT and event.button == play_button:
                new_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_sound.play()
                    running = False
                    exit_menu()

        for btn in [play_button, setting_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

def settings():
    esc_sound = pygame.mixer.Sound('soun/Button 4.wav')

    video_button = Button(WIDTH / 2 - (252 / 2), 270, 252, 74, "", 'image/видео 1.png', 'image/видео 3.png', 'soun/Button 4.wav')
    audio_button = Button(WIDTH / 2 - (252 / 2), 370, 252, 74, "", 'image/аудио 1.png', 'image/аудио 3.png', 'soun/Button 4.wav')
    back_button = Button(WIDTH / 2 - (252 / 2), 470, 252, 74, "", 'image/назад 1.png', 'image/назад 3.png', 'soun/Button 4.wav')

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_moving_background()

        bord_rect = bord.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(bord, bord_rect)

        font = pygame.font.Font(None, 66)
        text_surface = font.render("НАСТРОЙКИ", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 220))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
                main_menu()

            if event.type == pygame.USEREVENT and event.button == audio_button:
                running = False
                audio_setting()

            if event.type == pygame.USEREVENT and event.button == video_button:
                running = False
                video_setting()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_sound.play()
                    running = False
                    main_menu()

            for btn in [video_button, audio_button, back_button]:
                btn.handel_event(event)

        for btn in [video_button, audio_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

def audio_setting():
    esc_sound = pygame.mixer.Sound('soun/Button 4.wav')
    back2_button = Button(WIDTH / 2 - 154, HEIGHT / 2 + 120, 140, 50, "", 'image/назад 1.png', 'image/назад 3.png','soun/Button 4.wav')
    apply_button = Button(WIDTH / 2 + 15, HEIGHT / 2 + 120, 140, 50, "", 'image/сохр 1.png', 'image/сохр 3.png','soun/Button 4.wav')
    volume_slider = Slider(WIDTH / 2 - 143.5, HEIGHT / 2 - 50, 268, 40, 0, 1, pygame.mixer.music.get_volume(), 'image/ползунок 1.png', 'image/ползунок 2.png', (255, 215, 0))
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_moving_background()

        bord_rect = bord.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(bord, bord_rect)

        bord2_rect = bord2.get_rect(center=(WIDTH / 2-10, HEIGHT / 2-30))  # Расположение второго изображения границы
        screen.blit(bord2, bord2_rect)

        font = pygame.font.Font(None, 38)
        text_surface = font.render("НАСТРОЙКИ АУДИО", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 220))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back2_button:
                running = False
                settings()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_sound.play()
                    running = False
                    settings()

            volume_slider.handle_event(event)


            for btn in [back2_button, apply_button]:
                btn.handel_event(event)
        for btn in [back2_button, apply_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        volume_slider.draw(screen)

        pygame.display.flip()

def video_setting():
    back3_button = Button(WIDTH / 2 - 154, HEIGHT / 2 + 120, 140, 50, "", 'image/назад 1.png', 'image/назад 3.png','soun/Button 4.wav')
    apply2_button = Button(WIDTH / 2 + 15, HEIGHT / 2 + 120, 140, 50, "", 'image/сохр 1.png', 'image/сохр 3.png','soun/Button 4.wav')
    esc_sound = pygame.mixer.Sound('soun/Button 4.wav')

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_moving_background()

        bord_rect = bord.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(bord, bord_rect)

        font = pygame.font.Font(None, 38)
        text_surface = font.render("НАСТРОЙКИ ВИДЕО", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 220))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back3_button:
                running = False
                settings()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_sound.play()
                    running = False
                    settings()
            for btn in [back3_button, apply2_button]:
                btn.handel_event(event)
        for btn in [back3_button, apply2_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

def exit_menu():
    pygame.mixer.music.stop()  # Остановка музыки при входе в меню выхода
    yes_button = Button(WIDTH / 2 - 180, HEIGHT / 2 - 50, 170, 50, "", 'image/да 1.png', 'image/да 3.png', 'soun/Button 4.wav')
    no_button = Button(WIDTH / 2 + 15, HEIGHT / 2 - 50, 170, 50, "", 'image/нет 1.png', 'image/нет 3.png', 'soun/Button 4.wav')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(exit_bg, (0, 0))

        bord1_rect = bord1.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        screen.blit(bord1, bord1_rect)

        font = pygame.font.Font(None, 32)
        text_surface = font.render("Вы точно хотите выйти из игры?", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 280))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [yes_button, no_button]:
                btn.handel_event(event)

            if event.type == pygame.USEREVENT and event.button == yes_button:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == no_button:
                running = False
                play_music()  # Возобновление музыки при возвращении в главное меню
                main_menu()

        for btn in [yes_button, no_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

def new_game():
    pygame.mixer.music.stop()
    game = Game()
    game.run()



main_menu()