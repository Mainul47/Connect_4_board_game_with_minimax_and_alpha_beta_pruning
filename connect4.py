import numpy as np
import pygame
import sys
import math
import random

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
ROW_COUNTER = 6
COLUMN_COUNTER = 7
PLAYER = 0
AI = 1
P_PIECE =1
AI_PIECE = 2
w_length = 4
##Create the 6*7 board for connect4
def c_board():
    board = np.zeros((ROW_COUNTER,COLUMN_COUNTER))
    return board

def drop(board, row, selection, piece):
    board[row][selection] = piece

#if 0, still open
def valid_location(board, selection):
    return  board[ROW_COUNTER - 1][selection] == 0

def get_open_row(board,selection):
    for row in range(ROW_COUNTER):
        if board[row][selection] == 0:
            return row
#will flip the board so first the bottom row will fill
def p_board(board):
    print(np.flip(board,0))

def evaluate(window, piece):
    sco = 0
    opposite = P_PIECE
    if piece == P_PIECE:
        opposite = AI_PIECE

    if window.count(piece) ==4:
        sco +=100

    elif window.count(piece) == 3 and window.count(0) ==1:
        sco += 5

    elif window.count(piece) == 2 and window.count(0) == 2:
        sco += 2

    elif window.count(opposite) == 3 and window.count(0) == 1:
        sco -= 4

    return sco

def win(board, piece):
    #checking horizontal for win
    for col in range(COLUMN_COUNTER-3):
        for rows in range(ROW_COUNTER):
            if board [rows][col] == piece and board [rows][col + 1] == piece and board [rows][col+2] == piece and board[rows][col+3] == piece:
                return True

    #checking vertical for win
    for col in range(COLUMN_COUNTER):
        for rows in range(ROW_COUNTER-3):
            if board [rows][col] == piece and board [rows+1][col] == piece and board [rows+2][col] == piece and board[rows+3][col] == piece:
                return True


    #checking upper diagonal
    for col in range(COLUMN_COUNTER-3):
        for rows in range(ROW_COUNTER-3):
            if board [rows][col] == piece and board [rows+1][col+1] == piece and board [rows+2][col+2] == piece and board[rows+3][col+3] == piece:
                return True
    #checking lower diagonal
    for col in range(COLUMN_COUNTER-3):
        for rows in range(3,ROW_COUNTER):
            if board [rows][col] == piece and board [rows-1][col+1] == piece and board [rows-2][col+2] == piece and board[rows-3][col+3] == piece:
                return True
def d_board(board):
    for c in range(COLUMN_COUNTER):
        for r in range(ROW_COUNTER):
            pygame.draw.rect(screen,WHITE,(c*SQUARE,r*SQUARE+SQUARE, SQUARE,SQUARE))
            pygame.draw.circle(screen,BLACK, (int(c*SQUARE+SQUARE/2),int(r*SQUARE+SQUARE+SQUARE/2)),RADIUS)
    for c in range(COLUMN_COUNTER):
        for r in range(ROW_COUNTER):
            if board[r][c] == P_PIECE:
                pygame.draw.circle(screen,RED, (int(c*SQUARE+SQUARE/2),height-int(r*SQUARE+SQUARE/2)),RADIUS)
            if board[r][c] == AI_PIECE:
                pygame.draw.circle(screen,BLUE, (int(c*SQUARE+SQUARE/2),height-int(r*SQUARE+SQUARE/2)),RADIUS)
    pygame.display.update()

def score(board, piece):

    sc = 0

    #for center
    centr = [int(i) for i in list(board[:,COLUMN_COUNTER//2])]
    centr_count = centr.count(piece)
    sc+= centr_count * 3

    # for horizontal
    for row in range(ROW_COUNTER):
        row_arr = [int(i) for i in list(board[row,:])]
        for col in range(COLUMN_COUNTER-3):
            window = row_arr[col:col+w_length]
            sc+= evaluate(window,piece)

    
    #for vertical
    for col in range(COLUMN_COUNTER):
        col_arr = [int(i) for i in list(board[:,col])]
        for row in range(ROW_COUNTER-3):
            window = col_arr[row:row+w_length]
            sc+= evaluate(window,piece)


    #for diagonal
    for row in range(ROW_COUNTER-3):
        for col in range(COLUMN_COUNTER-3):
            window = [board [row+i][col +i ] for i in range(w_length)]
            sc+= evaluate(window,piece)



    for row in range(ROW_COUNTER-3):
        for col in range(COLUMN_COUNTER-3):
            window = [board [row+3 -i][col +i ] for i in range(w_length)]
            sc+= evaluate(window,piece)

    return sc




def best_move(board, piece):
    v_location = location(board)
    b_sc = -100
    b_col = random.choice(v_location)

    for col in v_location:
        row = get_open_row(board,col)
        temp = board.copy()
        drop(temp,row,col,piece)
        sc = score(temp,piece)

        if sc > b_sc:
            b_sc = sc
            b_col = col
    
    return b_col
        

def check_terminalnode(board):
    if win(board, P_PIECE) or win(board, AI_PIECE) or len (location(board)) == 0 :
        return True
    else:
        return False


######################################################
#       PSEUDO CODE
#
# function  minimax(node, depth, maximizingPlayer) is
#     if depth = 0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer then
#         value := −∞
#         for each child of node do
#             value := max(value, minimax(child, depth − 1, FALSE))
#         return value
#     else (* minimizing player *)
#         value := +∞
#         for each child of node do
#             value := min(value, minimax(child, depth − 1, TRUE))
#         return value



# function alphabeta(node, depth, α, β, maximizingPlayer) is
#     if depth = 0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer then
#         value := −∞
#         for each child of node do
#             value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
#             if value ≥ β then
#                 break (* β cutoff *)
#             α := max(α, value)
#         return value
#     else
#         value := +∞
#         for each child of node do
#             value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
#             if value ≤ α then
#                 break (* α cutoff *)
#             β := min(β, value)
#         return value
####################################################

def minmax(board,depth,alpha, beta, maximizingPlayer):
    valid_location = location(board)
    terminal = check_terminalnode(board)
    if depth == 0 or terminal:
        if terminal:
            if win(board, AI_PIECE):
                return (None,9999999999999)
            elif win(board, P_PIECE):
                return (None,-99999999999)
            else: #game is finished
                return (None,0)
        else:
            return (None,score(board,AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_open_row(board,col)
            board_copy = board.copy()
            drop(board_copy,row,col,AI_PIECE)
            new_score = minmax(board_copy,depth-1, alpha ,beta, False)[1]
            if new_score > value:
                value = new_score
                column= col
            alpha = max(alpha, value)
            if alpha>= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_open_row(board,col)
            board_copy = board.copy()
            drop(board_copy,row,col,P_PIECE)
            new_score = minmax(board_copy,depth-1,alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column= col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column , value        


def location(board):
    v_location = []
    for col in range (COLUMN_COUNTER):
        if valid_location(board,col):
            v_location.append(col)
    return v_location




board = c_board()
p_board(board)
# will turn true if someone get 4 in a row
finish = False
turn = 0

pygame.init()
SQUARE = 100
width = COLUMN_COUNTER * SQUARE
height = (ROW_COUNTER+1)*SQUARE
size = (width, height)
RADIUS = int(SQUARE/2 - 5)
screen = pygame.display.set_mode(size)
d_board(board)
pygame.display.update()

myfont = pygame.font.SysFont('Helvetica', 70)
turn = random.randint(PLAYER,AI)

while not finish:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,WHITE,(0,0,width, SQUARE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen,RED , (posx, int(SQUARE/2)),RADIUS)
            
        pygame.display.update()


        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)

            #Player 
            if turn == PLAYER:
               posx = event.pos[0]
               selection = int(math.floor(posx/SQUARE))
               
               if valid_location(board,selection):
                    row = get_open_row(board,selection)
                    drop(board,row,selection,P_PIECE)
                    if win(board,P_PIECE):
                        label = myfont.render("Player 1 is the winner!!",P_PIECE ,RED)
                        screen.blit(label,(40,10))
                        finish = True
                    turn+=1
                    #will alternate between players
                    turn = turn%2
                    p_board(board)
                    d_board(board)
                        
    #AI
    if turn == AI and not finish:
        # getting a random location on AI
        #selection = random.randint(0,COLUMN_COUNTER-1)
        #selection = best_move(board, AI_PIECE)
        selection, minmax_score = minmax(board,5,-math.inf, math.inf, True)


        if valid_location(board,selection):
            pygame.time.wait(100)
            row = get_open_row(board,selection)
            drop(board,row,selection,AI_PIECE)
            if win(board,AI_PIECE):
                label = myfont.render("AI is the winner", AI_PIECE , BLUE)
                screen.blit(label,(40,10))
                finish = True

            p_board(board)
            d_board(board)
            turn+=1
            #will alternate between players
            turn = turn%2

    if finish:
        pygame.time.wait(1000)
