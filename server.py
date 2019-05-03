import socket, time, pickle, random, math, pygame

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("10.113.4.4", 5555))
serversocket.listen(2)
arr = [400,400,400,400,0,0]
connection = []
speed = 20

ball_speed = 8.0
direction = random.randrange(-45, 45)

#create sound channel
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

def create_sounds():
    sounds = []
    paddle = []

    sounds.append(pygame.mixer.Sound('hit0.wav'))
    sounds.append(pygame.mixer.Sound('hit1.wav'))
    sounds.append(pygame.mixer.Sound('hit2.wav'))
    sounds.append(pygame.mixer.Sound('hit3.wav'))
    sounds.append(pygame.mixer.Sound('hit4.wav'))

    paddle.append(pygame.mixer.Sound('hit_paddle.wav'))

    return sounds, paddle

sound_bounce, sound_paddle = create_sounds()

def process_positions(array, player_1, player_2):
    #info[0] = key_up
    #info[1] = key_down
    global direction, ball_speed, sound_bounce, sound_paddle
    direction_radians = math.radians(direction)

    '''PADDLE MOVING'''
    if player_1[0] == True and array[0] > 0:
        array[0]-= speed

    if player_1[1] == True and array[0] < 540:
        array[0]+= speed

    if player_2[0] == True and array[1] > 0:
        array[1]-= speed

    if player_2[1] == True and array[1] < 540:
        array[1]+= speed

    '''PADDLE MOVING'''

    '''BALL MOVING'''
    array[2] -= ball_speed * math.cos(direction_radians)
    array[3] += ball_speed * math.sin(direction_radians)

    if array[2] >= 595 or array[2] <= 0:
        direction = (180 - direction) % 360
        ball_speed *= 1.1
        sound_bounce[random.randrange(len(sound_bounce))].play()

    if array[3] >= 795 or array[3] <= 0:
        if array[3] > 795:
            array[4] += 1
        else:
            array[5] += 1
            
        array[2] = 350.0
        array[3] = random.randrange(50, 750)
        ball_speed = 8.0
        direction = random.randrange(-45, 45)

        if random.randrange(2) == 0:
            direction += 180
            array[2] = 50

    '''BALL MOVING'''


    '''PADDLE DETECTION'''
    if array[3]<20 and (array[0]<array[2] and array[0]+60>array[2]):
        direction = (360 - direction) % 360
        ball_speed *= 1.1
        sound_paddle[0].play()

    if array[3]>780 and (array[1]<array[2] and array[1]+60>array[2]):
        direction = (360 - direction) % 360
        ball_speed *= 1.1
        sound_paddle[0].play()

    #info = [player_1_y, player_2_y, ball_y, ball_x, score_1, score_2]

    return array

def waiting_for_connections():
    while len(connection)<2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)

def recieve_information():
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))

    return player_1_info, player_2_info





while True:
    waiting_for_connections()

    data_arr = pickle.dumps(arr)
    print(data_arr)
    connection[0].send(data_arr)
    connection[1].send(data_arr)

    player1, player2 = recieve_information()

    arr = process_positions(arr,player1, player2)