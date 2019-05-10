import pygame, socket, time, pickle

pygame.init()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ip_address, 5555))


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
    bounce = False
    while game_finished == False:
        #set FPS
        clock.tick(120)
        #Collect Game information. ex)Paddle position, Score, Ball position
        info = recieve_data()
        #draw background
        gameDisplay.fill(WHITE)
        #draw paddles/ball
        draw_paddles(10, info[0], 1)
        draw_paddles(display_width-20, info[1], 2)
        draw_ball(info[3], info[2])
        #draw score
        message_display(info[4], 300, 50)
        message_display(info[5], 500, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_finished = True
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
                    

        #send key press to server
        data_arr = pickle.dumps([key_up, key_down])
        clientsocket.send(data_arr)

    
        if (info[4] == 11 or info[5] == 11):
            #game_finished = True
            end = pickle.dumps("END")
            clientsocket.send(end)
    #info = [player_1_y, player_2_y, ball_y, ball_x, score_1, score_2]

def menu():
    run = True
    message = "Click to find a Pong game!"
    while run:
        clock.tick(60)
        gameDisplay.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(message, 1, (255,0,0))
        gameDisplay.blit(text, (155, display_height / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    message = main()

while True:
    menu()
