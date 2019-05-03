import pygame, socket, time, pickle

pygame.init()

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)

display_width = 800
display_height = 600

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height))

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("10.113.4.4", 5555))


def message_display(txt,x,y):
    font = pygame.font.SysFont("comicsans", 50)
    if x == 500:
        label = font.render(str(txt), 1, BLUE)
    else:
        label = font.render(str(txt), 1, RED)
    gameDisplay.blit(label, (x,y))

def recieve_data():
    data = clientsocket.recv(1024)
    data = pickle.loads(data)

    return data

def draw_paddles(x,y,p):
    if p == 1:
        pygame.draw.rect(gameDisplay, RED, [x, y, 10, 60])
    if p == 2:
        pygame.draw.rect(gameDisplay, BLUE, [x, y, 10, 60])

def draw_ball(x,y):
    pygame.draw.circle(gameDisplay, BLACK, [int(x),int(y)], 5)

def main():
    game_finished = False
    key_up = False
    key_down = False
    while game_finished == False:
        clock.tick(120)
        info = recieve_data()
        gameDisplay.fill(WHITE)
        draw_paddles(10, info[0], 1)
        draw_paddles(display_width-20, info[1], 2)
        draw_ball(info[3], info[2])

        message_display(info[4], 300, 50)
        message_display(info[5], 500, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    key_up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    key_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    key_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    key_down = False

        arr = [key_up, key_down]
        data_arr = pickle.dumps(arr)
        clientsocket.send(data_arr)

    #info = [player_1_y, player_2_y, ball_y, ball_x, score_1, score_2]

main()
