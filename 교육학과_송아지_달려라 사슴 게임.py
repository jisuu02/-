import pygame
import sys
import random

pygame.init() # 파이게임 초기화
pygame.display.set_caption('달려라 사슴') # 게임 이름 설정
SCREEN_HEIGHT = 450 # 게임판 세로 길이
SCREEN_WIDTH = 800 # 게임판 가로 길이
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 게임판 설정

# 이미지 불러오기

# 사슴 이미지
RUNNING = [pygame.image.load("deer1.png"), pygame.image.load("deer2.png")] # 달리는 사슴 이미지
JUMPING = pygame.image.load("deer3.png") # 점프하는 사슴 이미지
DUCKING = [pygame.image.load("deer4.png"), pygame.image.load("deer5.png")] #엎드린 사슴 이미지

# 장애물 이미지
OBSTACLE = [pygame.image.load("plant.jpg"),pygame.image.load("stone.jpg"),pygame.image.load("mountain.png")] # 장애물 이미지
TREE = [pygame.image.load("cactus.png"),pygame.image.load("tree1.jpg"),pygame.image.load("tree2.jpg")] # 나무 이미지

BIRD = [pygame.image.load("bird1.png"),pygame.image.load("bird2.png")] # 새 이미지

# 배경 이미지
BG = pygame.image.load("bg.png")


# 사슴 관련 코드
class Deer:
    X_POS = 80 # 사슴 X 위치
    Y_POS = 310 # 사슴 Y 위치
    Y_POS_DUCK = 340 # 엎드린 사슴 Y 위치
    JUMP_VEL = 8.5 # 점프한 사슴 위치

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.deer_duck = False # 초기에 엎드림은 거짓
        self.deer_run = True # 초기에 달리는 것은 참
        self.deer_jump = False # 초기에 점프는 거짓

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.deer_rect = self.image.get_rect()
        self.deer_rect.x = self.X_POS
        self.deer_rect.y = self.Y_POS

    def update(self, userInput):
        if self.deer_duck:
            self.duck()
        if self.deer_run:
            self.run()
        if self.deer_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.deer_jump: # 위쪽 방향키 누른 경우
            self.deer_duck = False # 엎드리기는 거짓
            self.deer_run = False # 달리기는 거짓
            self.deer_jump = True # 점프는 참
        elif userInput[pygame.K_DOWN] and not self.deer_jump: # 아래쪽 방향키 누른 경우
            self.deer_duck = True # 엎드리기는 참
            self.deer_run = False # 달리기는 거짓
            self.deer_jump = False # 점프는 거짓
        elif not (self.deer_jump or userInput[pygame.K_DOWN]): # 아무것도 누르지 않은 경우
            self.deer_duck = False # 엎드리기는 거짓
            self.deer_run = True # 달리기는 참
            self.deer_jump = False # 점프는 거짓

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.deer_rect = self.image.get_rect()
        self.deer_rect.x = self.X_POS
        self.deer_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.deer_rect = self.image.get_rect()
        self.deer_rect.x = self.X_POS
        self.deer_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.deer_jump:
            self.deer_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.deer_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.deer_rect.x, self.deer_rect.y))

# 장애물 관련 코드
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

# 장애물 관련 코드
class Cactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class Tree(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

# 새 관련 코드
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Deer()
    game_speed = 20 # 게임 속도
    x_pos_bg = 0 # 배경 x 위치
    y_pos_bg = 405 # 배경 y 위치
    points = 0 # 점수 설정
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    # 점수 설정
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0: # 점수를 100으로 나눈 나머지가 0일 경우
            test_sound1 = pygame.mixer.Sound('shot.mp3') # 효과음 넣기
            test_sound1.play() # 효과음 재생
            game_speed += 1 # 게임 속도 1만큼 증가

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (700, 40) # 점수 중앙 위치 설정
        SCREEN.blit(text, textRect) # 게임 화면에 점수 표시

    # 배경 설정
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Cactus(OBSTACLE))
            elif random.randint(0, 2) == 1:
                obstacles.append(Tree(TREE))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.deer_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font(None, 30)

        # 게임 시작 초기 화면
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0)) # 시작을 위해 아무 키나 누르기
        # 게임 종료 화면
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0)) # 재시작을 위해 아무 키나 누르기
            score = font.render("Score: " + str(points), True, (0, 0, 0)) # 게임 점수
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50) # 점수판 중앙 위치 설정
            SCREEN.blit(score, scoreRect) # 게임판에 점수판 표시
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # 텍스트 중앙 위치 설
        SCREEN.blit(text, textRect) # 게임판에 텍스프 효시
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # X버튼 눌렀을 경우
                run = False
            if event.type == pygame.KEYDOWN: # 키보드 버튼 눌렀을 경우
                main()


menu(death_count=0)
