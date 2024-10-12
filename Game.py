from pygame import *

# Завантаження об'єктів
image_player_right = 'player_right.png'
image_player_left = 'player_left.png'
image_level1 = 'level_1.png'
background = transform.scale(image.load(image_level1), (8000, 600))

window = display.set_mode((1000, 600))
display.set_caption("Super Mario in Python!")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (60, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

pits = [(2395, 2405), (2970, 3050)]

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.is_jumping = False
        self.jump_count = 12
        self.gravity = 0.5
        self.velocity_y = 0
        self.direction = "right"
        self.falling = False
    
    def update(self, shift_x):
        keys = key.get_pressed()
        
        if keys[K_LEFT] and self.rect.x > 50:
            self.rect.x -= self.speed
            self.direction = "left"
        
        if keys[K_RIGHT] and self.rect.x < 900:
            self.rect.x += self.speed
            self.direction = "right"

        if self.direction == "right":
            self.image = transform.scale(image.load(image_player_right), (60, 65))
        elif self.direction == "left":
            self.image = transform.scale(image.load(image_player_left), (60, 65))

        if not self.is_jumping:
            if keys[K_UP]:
                self.is_jumping = True
                self.velocity_y = -11
        else:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.rect.y >= 470:
                self.rect.y = 470
                self.is_jumping = False

        for pit in pits:
            if pit[0] <= self.rect.x - shift_x[0] <= pit[1] and self.rect.y == 470:
                self.falling = True
                self.velocity_y = 0
                break

        if self.falling:
            self.rect.y += self.gravity * 10
            if self.rect.y > 600:
                return True

        if keys[K_LEFT] or keys[K_RIGHT]:
            shift_x[0] += self.speed if keys[K_LEFT] else -self.speed
        
        return False

# Створення об'єктів
player = Player(image_player_right, 100, 470, 4)

shift_x = [0]

# Ігровий цикл
game = True
clock = time.Clock()
finish = False
game_over = False

font.init()
font = font.Font('Mario.ttf', 35)
win = font.render('You win!', True, (0, 250, 0))
lose = font.render('You lose!', True, (250, 0, 0))

# Додано таймер
start_time = time.get_ticks()  # Час початку гри

# Оновлений ігровий цикл
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (shift_x[0], 0))
        game_over = player.update(shift_x)
        
        # Оновлення та відображення таймера, якщо гра не закінчена
        timer = (time.get_ticks() - start_time) // 1000  # Обчислення часу в секундах
        time_display = font.render(f'Time: {timer}', True, (255, 255, 255))  # Виведення часу
        window.blit(time_display, (10, 10))  # Виведення таймера у верхньому лівому куті

    if shift_x[0] > 0:
        shift_x[0] = 0
    elif shift_x[0] < -7000:
        shift_x[0] = -7000

    player.reset()

    if game_over:
        finish = True
        window.fill((0, 0, 0))
        window.blit(lose, (400, 300))
        # Таймер не буде відображатися, коли гра програна

    if player.rect.x - shift_x[0] >= 7050 and not game_over:
        finish = True
        window.fill((0, 0, 0))
        window.blit(win, (400, 300))
        # Таймер не буде відображатися, коли гра виграна

    display.update()

