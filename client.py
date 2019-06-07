"""
This is the client file and will send button press signals from both paddles to the server for calculations.
The client file recieves the positions of the ball and both players from the server.
The client file also draws everything on the screen.
"""

import pygame, socket, time, pickle

pygame.init()

#get host name of wifi computer is connected too
#hostname = socket.gethostname()
#ip_address = socket.gethostbyname(hostname)

#colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)

#window sizes
display_width = 800
display_height = 600

#Lets pygame know what window to draw things too
gameDisplay = pygame.display.set_mode((display_width, display_height))
#initalize clock for FPS
clock = pygame.time.Clock()

#create connection to server socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('10.113.5.26', 5555))

global message

#Draw images on the screen
def message_display(txt,x,y):
    font = pygame.font.SysFont("comicsans", 50)
    if x == 500:
        label = font.render(str(txt), 1, BLUE)
    else:
        label = font.render(str(txt), 1, RED)
    gameDisplay.blit(label, (x,y))

#recieve and unpickle data from server
def recieve_data():
    data = clientsocket.recv(1024)
    data = pickle.loads(data)

    return data

#draw paddles on screen
def draw_paddles(x,y,p):
    if p == 1:
        pygame.draw.rect(gameDisplay, RED, [x, y, 10, 60])
    if p == 2:
        pygame.draw.rect(gameDisplay, BLUE, [x, y, 10, 60])

#draw ball on screen
def draw_ball(x,y):
    pygame.draw.circle(gameDisplay, BLACK, [int(x),int(y)], 5)

#main game loop
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

        #wait for key press activity from client
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

        #reset game if score reaches 11
        if (info[4] == 11 or info[5] == 11):
            #game_finished = True
            end = pickle.dumps("END")
            clientsocket.send(end)
            game_finished == True
    #info = [player_1_y, player_2_y, ball_y, ball_x, score_1, score_2]

#main menu loop
def menu():
    run = True
    while run == True:
        clock.tick(60)
        gameDisplay.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        try:
            text = font.render(message, 1, (255,0,0))
        except:
            text = font.render("Click to play!", 1, (255,0,0))
        gameDisplay.blit(text, (155, display_height / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()
while True:
    menu()
