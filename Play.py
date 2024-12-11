import pygame,sys,random

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((423,768))
clock = pygame.time.Clock()

#Chèn âm thanh
flap_sound = pygame.mixer.Sound('C:/DACN1/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('C:/DACN1/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('C:/DACN1/sound/sfx_point.wav')
score_sound_countdown = 100

#chèn nền game
background = pygame.image.load('C:/DACN1/assets/background.png').convert()
background = pygame.transform.scale2x(background).convert()

#chèn sàn
San = pygame.image.load('C:/DACN1/assets/floor.png').convert()
San = pygame.transform.scale2x(San).convert()
Vi_tri_san_x = 0
def Ve_San():
    screen.blit(San,(Vi_tri_san_x,650))
    screen.blit(San,(Vi_tri_san_x+423,650))

#tạo ống
pipe_surface = pygame.image.load('C:/DACN1/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [200,300,400]
#tạo thời gian tạo ống
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe,1200)

def Tao_ong():
    ramdon_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,ramdon_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,ramdon_pipe_pos-650))
    return bottom_pipe,top_pipe
def di_ong(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def Ve_ong(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 :
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

#chèn chim
bird_down = pygame.transform.scale2x(pygame.image.load('C:/DACN1/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('C:/DACN1/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('C:/DACN1/assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,325))
gravity = 0.3 
bird_movement = 0
#tạo delay cho chim
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)

def Va_cham(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3 ,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

game_active = False

#tạo màn hình kết thúc
game_font = pygame.font.Font('C:/DACN1/04B_19.ttf',35)
game_over_surface = pygame.transform.scale2x(pygame.image.load('C:/DACN1/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))

#tạo biến
score = 0
high_score = 0

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement =-10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(Tao_ong())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird,bird_rect = bird_animation()
    screen.blit(background,(0,0))
    if game_active:
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect) 
        game_active = Va_cham(pipe_list)
        #ống
        pipe_list = di_ong(pipe_list)
        Ve_ong(pipe_list)

        score += 0.01        
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else: 
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)

        score_display('game_over')
    #sàn
    Vi_tri_san_x -= 1
    Ve_San()
    if Vi_tri_san_x <= -423 :
        Vi_tri_san_x = 0
    pygame.display.update()
    clock.tick(120)
