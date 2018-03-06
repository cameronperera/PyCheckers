import os
import msvcrt
import re
from pyfiglet import Figlet
import checker_board_terminal as cbt


emptyCell = cbt.emptyCell
whitePiece = cbt.whitePiece
redPiece = cbt.redPiece
number = cbt.number
blankSpace = cbt.blankSpace
pathPiece = cbt.pathPiece
kingWhitePiece = cbt.kingWhitePiece
kingRedPiece = cbt.kingRedPiece

moveLeftDown = [1, -1]
moveRightDown = [1, 1]
moveLeftUp = [-1, -1]
moveRightUp = [-1, 1]

def banner(text):
    fig = Figlet(font='slant')
    print(fig.renderText(text))

def rules():
    rule = ('\n'
            '									Rules\n'
            '==================================================================================\n'
            '\n'
            '- X pieces always go first\n'
            '- Moves\n'
            '	* Capturing moves\n'
            '		~ Capturing moves occur when a player "jumps" an opposing piece.\n'
            '			This is also done on the diagonal and can only happen when the\n'
            '			square behind (on the same diagonal) is also open.\n'
            '			This means that you may not jump an opposing piece around a corner.\n'
            '		~ Forced Captures: When a player is in a position to make a capturing move,\n'
            '			he must make a capturing move. When he has more than one capturing\n'
            '			move to choose from he may take whichever move suits him.\n'
            '	* Non-capturing moves\n'
            '		~ Non-capturing moves are simply a diagonal move forward from one\n'
            '			square to an adjacent square.\n'
            '	* Kinging move\n'
            '		~ When a checker achieves the opponent\'s edge of the board\n'
            '			(called the "king\'s row") it is crowned with another checker.\n'
            '			This signifies that the checker has been made a king.\n'
            '			The king now gains an added ability to move backward.\n'
            '			The king may now also jump in either direction or even in\n'
            '			both directions in one turn (if he makes multiple jumps).\n'
            '		~ If the player gets an uncrowned checker on the king\'s row\n'
            '			because of a capturing move then he must stop to be crowned\n'
            '			even if another capture seems to be available.\n'
            '			He may then use his new king on his next move.\n'
            '\n'
            '----------------------------------------------------------------------------------\n')
    print(rule)

def instructions():
    instruction = ('\n'
                   '								   Instructions\n'
                   '==================================================================================\n'
                   '\n'
                   '- Player who is using the X pieces will go first.\n'
                   '- Move paths will be shown via asterisks (*).\n'
                   '- The player will select the piece they would like to move.\n'
                   '	* This is done by selecting the coordinates of the piece.\n'
                   '	* First you choose 1-8 along the left or right.\n'
                   '	* Then you choose 1-8 on the top or bottom.\n'
                   '	* Enter your selection as 3,4 or 6,3.\n'
                   '- If any capture moves are possible, the game will list those moves and you will\n'
                   '	select which move you would like to make.\n'
                   '- If a player’s piece lands on the King’s row it has to stop to be Kinged and\n'
                   '	the turn passes to the next player.\n'
                   '- Once either player has no more moves or pieces, the other player wins.\n'
                   '\n'
                   '----------------------------------------------------------------------------------\n')
    print(instruction)

def clear():
    osName = os.name
    if osName == 'nt':
        clearMessage = 'cls'
    else:
        clearMessage = 'clear'
    os.system(clearMessage)

def playerControl(piece_type, i):
    if i == 0:
        if piece_type == redPiece or piece_type == kingRedPiece:
            return True
        else:
            return 'Please choose a red piece to move. '
    if i == 1:
        if piece_type == whitePiece or piece_type == kingWhitePiece:
            return True
        else:
            return 'Please choose a white piece to move. '

def getPlayerNumber(i):
    if i == 0:
        return '1'
    else:
        return '2'

def gameType():
    gameSelection = input('Would you like to play Pv[P] or Pv[C]? ').lower()
    whileVar = True
    while whileVar:
        if gameSelection == 'p':
            return 'PvP'
        elif gameSelection == 'c':
            print('Not implemented yet')
            gameSelection = input('Would you like to play Pv[P] or Pv[C]? ').lower()

def changeValueOfI(i):
    if i == 0:
        return 1
    else:
        return 0

def playerTurnPrint(i):
    if i == 1:
        print("Player 2's turn")
    else:
        print("Player 1's turn")

def pressAnyKey():
    print('Your move is complete')
    print('Press any key to continue')
    cont = msvcrt.getch()
    if cont == '?':
        print(cont)
        return cont
    pass

def menuSelection():
    selection = input('Would you like to [S]tart a new game, see the [R]ules, [I]nstructions, or [E]xit? ').lower()
    return selection

def menu():
    banner('<<< Checkers! >>>')
    selection = menuSelection()
    while True:
        if selection == 's':
            return 'start'
        elif selection == 'r':
            clear()
            rules()
            selection = menuSelection()
        elif selection == 'i':
            clear()
            instructions()
            selection = menuSelection()
        elif selection == 'e':
            clear()
            quit()
        else:
            print('Please choose "S", "R", "I" or "E".')
            selection = menuSelection()

def getLocation(location):
    move = input(location)
    moveCheck = re.compile('^\d{1}([\W]{1})\d{1}$')
    moveMatch = re.match(moveCheck, move)
    if moveMatch is None:
        return False
    else:
        return move

def convertMoveToInt(move):
    for chars in move:
        if chars in ' .,/<>?\|':
            moveInt = move.split(chars)
    moveInt = list(map(int, moveInt))
    return moveInt

def removeOuterBracket(coord):
    for singleCoord in coord:
        return singleCoord

def displayPossibleMoves(jump_dict):
    for key, moves in jump_dict.items():
        print(str(key) + ' : ' + str(moves))

def passSelectedMovePiece(move_Dict, move_selection):
    for key, value in move_Dict.items():
        if key == move_selection:
            return value