import random
# DISPLAYS THE TIC TAC TOE BOARD 

def display_board(board):
    print(' '+board[1]+' | '+board[2]+' | '+board[3])
    print('---|---|---')
    print(' '+board[4]+' | '+board[5]+' | '+board[6])
    print('---|---|---')
    print(' '+board[7]+' | '+board[8]+' | '+board[9])
    

def player_input():
# DECIDES IF PLAYER1/PLAYER2 WILL BE X/O
    choose_XO= input('Player 1 choose X or O ')
    
    while choose_XO not in['X','O','x','o']:
        print('Please choose X or O')
        choose_XO= input('Player 1 choose X or O ')
        
    player1= choose_XO
    
    if player1 in ['X','x']:
        print(f'Player 1 is X. Player 2 is O')    
        return ("X","O")
    else:
        print(f'Player 1 is O. Player 2 is X')    
        return ('O','X')
   

def place_marker(board, marker, position):
# USES THE INPUT FROM PLAYER1/PLAYER2'S CHOICES AND UPDATES THE BOARD
    
    board[position]=marker
    return board

def win_check(board, mark):
# CHECKS AND DECIDES WHO WINS
    if [mark]*3 in [board[1:4],board[4:7],board[7:10],board[1:8:3],board[2:9:3],board[3:10:3],board[1:10:4],board[3:8:2]]:#ROWS#COLOUMS#OBLIQUE ROW
        return mark
    else:
        pass
        
# RANDOMLY CHOOSES WHICH PLAYER WILL GO FIRST
def choose_first():
    if random.randint(1,2)==1:
        print('Player 1 goes first')
        return 1
    else:
        print('Player 2 goes first')
        return 2

def space_check(board,position):
#CHECKS IF SPACE IF AVAILABLE     
    return board[position] == ' '

def full_board_check(board):
# IF BOARD IS FULL, GAME ENDS
    return ' ' in board

def player_choice(board):
# OBTAINS THE PLAYER'S CHOICE AND INPUTS IT IN PLACE_MARKER()
    while True:
        choice= input('Enter a number from 1-9: ')
        if choice.isdigit():
            choice=int(choice)
            if 1 <= choice <= 9:
                if space_check(board,choice):
                    return int(choice)
        else:
            print('Error: Not a number.  Please enter a number from 1-9 or in an available space')
            continue
        if not 1<= choice <=9:
            print('Error: Not in range.  Please enter a number from 1-9 or in an available space')
            continue
        elif not space_check(board,choice):
            print('Error:No space available.  Please enter a number for an available space')
            continue
        else:
            print('error')
            
def replay():
# ASKS THE PLAYERS IF THEY WANT TO REPLAY THE GAME
    replay=input('Do you want to play again? Y/N')
    while replay not in ['Y','y','N','n']:
        replay = input('Enter Y or N')
    if replay in ['Y','y']:
        return True
    else:
        return False
    
print('TIC TAC TOE: PYTHON |REMASTERED|')

while True:
#     GAME START
    inpo= ['.',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    x=player_input()
    game_on=True
    enter=input('Press enter to start')
    while game_on:
#         TURN ONE
        display_board(inpo)
        inpo=place_marker(inpo,x[0],player_choice(inpo))
        if not full_board_check(inpo):
            print('DRAW')
            break
        if win_check(inpo,x[0])==x[0]:
            print(f'{x[0].upper()} Wins!')
            break
#         TURN TWO
        display_board(inpo)
        inpo=place_marker(inpo,x[1],player_choice(inpo))
        if not full_board_check(inpo):
            print('DRAW')
            break
        if win_check(inpo,x[1])==x[1]:
            print(f'{x[1].upper()} Wins!')
            break
    display_board(inpo)
    if replay():
        continue
    else:
        break
    

    

 
