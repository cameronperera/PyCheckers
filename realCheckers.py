from checker_board_terminal import CheckerBoard
import checker_board_terminal as cbt
import os
import re
import msvcrt
from pyfiglet import Figlet
from colorama import init
import time

init(autoreset=True, convert=True)

board = CheckerBoard()
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
i = 0
pickMessage = 'Pick piece to move : '


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


def menuSelection():
    selection = input('Would you like to [S]tart a new game, see the [R]ules, [I]nstructions, or [E]xit? ').lower()
    return selection


def displayBoard():
    board.printCheckerBoard()


def displayBoardReverse():
    board.reverseBoardView()
    board.actualBoardReversal()
    board.printCheckerBoard()


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


def checkIfMoveIsValid(possibleMoves):
    legal_moves = []
    for coords in possibleMoves:
        checkedPiece = board.pieceType(coords)
        if checkedPiece == emptyCell:
            legal_moves.append(coords)
    return legal_moves


def calculateAvailableMoves(selectedPieceCal):
    available_moves = [[sum(x) for x in zip(selectedPieceCal, moveLeftUp)],
                       [sum(x) for x in zip(selectedPieceCal, moveRightUp)]]
    return available_moves


def calculateKingMoves(selectedPiece):
    upMoves = calculateAvailableMoves(selectedPiece)
    downMoves = [[sum(x) for x in zip(selectedPiece, moveLeftDown)],
                 [sum(x) for x in zip(selectedPiece, moveRightDown)]]
    for coord in downMoves:
        upMoves.append(coord)
    return upMoves


def endLocationCheck(endLocation):
    legalJumps = []
    for coord in endLocation:
        piece_type = board.pieceType(coord)
        if piece_type == emptyCell:
            legalJumps.append(coord)
    return legalJumps


def checkKingsRow(playerTurn):
    if playerTurn == 0:
        pieceType = redPiece
        kingPiece = kingRedPiece
    if playerTurn == 1:
        pieceType = whitePiece
        kingPiece = kingWhitePiece

    y = 0
    kingBoard = board.__iter__()
    for cell in kingBoard[1]:
        if cell == pieceType:
            board.updateBoard([1, y], kingPiece)
            return True
        y += 1


def checkIfGameOver(playerTurn):
    if playerTurn == 1:
        otherPieceType = whitePiece
        otherKingPiece = kingWhitePiece
    else:
        otherPieceType = redPiece
        otherKingPiece = kingRedPiece

    for row in board.__iter__():
        for cell in row:
            if cell == otherPieceType or cell == otherKingPiece:
                return False
    return True


def checkForLegalMoves(playerTurn):
    if playerTurn == 0:
        pieceType = redPiece
        kingPiece = kingRedPiece
    if playerTurn == 1:
        pieceType = whitePiece
        kingPiece = kingWhitePiece

    x = 0
    y = 0
    for row in board.__iter__():
        for cell in row:
            if cell == pieceType:
                availableMoves = calculateAvailableMoves([x, y])
                legalMoves = checkIfMoveIsValid(availableMoves)
                if legalMoves == []:
                    pass
                else:
                    return True
            if cell == kingPiece:
                availableMoves = calculateAvailableMoves([x, y])
                legalMoves = checkIfMoveIsValid(availableMoves)
                if legalMoves == []:
                    pass
                else:
                    return True
            if y == 9:
                y = 0
            else:
                y += 1
        x += 1
    return False


def scanBoard(playerTurn):
    if playerTurn == 0:
        piece_type = redPiece
        kingPiece = kingRedPiece
    if playerTurn == 1:
        piece_type = whitePiece
        kingPiece = kingWhitePiece

    scanDict = {}
    key = 1
    x = 0
    y = 0
    for row in board.__iter__():
        for cell in row:
            if cell == piece_type:
                available_moves = listAvailableMoves(piece_type, [x, y])
                jump_moves = checkIfCaptureMove(piece_type, available_moves)
                if jump_moves == []:
                    pass
                else:
                    endLocation = calculateCaptureMove([x, y], jump_moves)
                    checkEndLocation = endLocationCheck(endLocation)
                    if checkEndLocation != []:
                        scanDict.update({key: [[x, y], checkEndLocation]})
                        key += 1

            if cell == kingPiece:
                available_moves = listAvailableMoves(kingPiece, [x, y])
                jump_moves = checkIfCaptureMove(kingPiece, available_moves)
                if jump_moves == []:
                    pass
                else:
                    endLocation = calculateCaptureMove([x, y], jump_moves)
                    checkEndLocation = endLocationCheck(endLocation)
                    if checkEndLocation != []:
                        scanDict.update({key: [[x, y], checkEndLocation]})
                        key += 1
            if y == 9:
                y = 0
            else:
                y += 1
        x += 1
    return scanDict


def chainJumpScan(jump_piece, piece_type):
    jumpDict = {}
    key = 1
    jump_pieceType = board.pieceType(jump_piece)
    if jump_pieceType == piece_type:
        available_moves = listAvailableMoves(piece_type, jump_piece)
        checkedJumpMove = checkIfCaptureMove(piece_type, available_moves)
        calculateJumpMove = calculateCaptureMove(jump_piece, checkedJumpMove)
        jumpMove = endLocationCheck(calculateJumpMove)
        if jumpMove != []:
            jumpDict.update({key: [jump_piece, jumpMove]})
            key += 1
    return jumpDict


def checkIfCaptureMove(piece_type, available_moves):
    jump_moves = []
    otherPiece = otherPieceCheck(piece_type)
    for coords in available_moves:
        coordsType = board.pieceType(coords)
        if coordsType == otherPiece[0] or coordsType == otherPiece[1]:
            jump_moves.append(coords)
    return jump_moves


def calculateCaptureMove(selectedPiece, jumpPiece):
    jumpedLocation = []
    for coords in jumpPiece:
        increaseAmount = [(coords[0] - selectedPiece[0])*2, (coords[1] - selectedPiece[1])*2]
        jumpedLocationCalc = [(selectedPiece[0] + increaseAmount[0]), (selectedPiece[1] + increaseAmount[1])]
        jumpedLocation.append(jumpedLocationCalc)
    return jumpedLocation


def calculateRemovePiece(selectedPiece, selectedJump):
    adjustmentCoord = [(selectedJump[0] - selectedPiece[0])//2, (selectedJump[1] - selectedPiece[1])//2]
    removePiece = [(selectedPiece[0] + adjustmentCoord[0]), (selectedPiece[1] + adjustmentCoord[1])]
    return removePiece


def otherPieceCheck(pieceType):
    if pieceType == redPiece or pieceType == kingRedPiece:
        otherPiece = whitePiece
        otherKingPiece = kingWhitePiece
    else:
        otherPiece = redPiece
        otherKingPiece = kingRedPiece
    return otherPiece, otherKingPiece


def listAvailableMoves(selectedPieceType, selected_Piece):
    if selectedPieceType == whitePiece or selectedPieceType == redPiece:
        availableMoves = calculateAvailableMoves(selected_Piece)
        return availableMoves
    elif selectedPieceType == kingRedPiece or selectedPieceType == kingWhitePiece:
        availableMoves = calculateKingMoves(selected_Piece)
        return availableMoves
    else:
        clear()
        displayBoard()
        print('Please pick a movable piece.')
        return False


def moveSelectedPiece(selected_piece, piece_type, pickedMove, newMoveBoard):
    newMoveBoard.updateBoard(pickedMove, piece_type)
    newMoveBoard.updateBoard(selected_piece, emptyCell)


def jumpPiece(selectedPiece, jumpMove, pieceType):
    removedPiece = calculateRemovePiece(selectedPiece, jumpMove)
    board.updateBoard(jumpMove, pieceType)
    board.updateBoard(removedPiece, emptyCell)
    board.updateBoard(selectedPiece, emptyCell)


def markValidMovesOnBoard(validMoves):
    for coords in validMoves:
        board.updateBoard(coords, pathPiece)


def markValidMoveOnBoardCaptureMoves(jumpDict, selectedPiece):
    for key, value in jumpDict.items():
        if value[0] == selectedPiece:
            for pathCoord in value[1]:
                board.updateBoard(pathCoord, pathPiece)


def moveSelectionInput(validMoves):
    inputDict = {}
    key = 1
    for coords in validMoves:
        inputDict.update({key: coords})
        key += 1
    return inputDict


def clear():
    osName = os.name
    if osName == 'nt':
        clear = 'cls'
    else:
        clear = 'clear'
    os.system(clear)
    # pass


def checkMoveSelection(outputDict, selection):
    for key, value in outputDict.items():
        if selection == key:
            return True
    clear()
    displayBoard()
    print('Please select one of the below options.')
    return False


def checkIfSelectionIsCaptureMove(jumpMoves, selectedPiece):
    for key, value in jumpMoves.items():
        if value[0] == selectedPiece:
            return True
    return False


def getJumpLocationBySelection(selection, jump_dict):
    for key, value in jump_dict.items():
        if selection == key:
            return value


def outputPossibleMoves(outputDict):
    while True:
        try:
            print('Below are you possible moves:')
            if len(outputDict) < 2:
                displayPossibleMoves(outputDict)
                selection = input('Only one move available. Please press Enter.')
                if selection == '':
                    return 1
                else:
                    clear()
                    displayBoard()
                    print('Please press Enter')
                pass
            else:
                displayPossibleMoves(outputDict)
                selection = input('Choose move number: ')
                selection = int(selection)
                checkMoveIsValid = checkMoveSelection(outputDict, selection)
                if checkMoveIsValid is True:
                    return selection
                else:
                    pass
        except ValueError:
            clear()
            displayBoard()
            print('Please enter a number.')
            pass


def outputPossibleCaptureMoves(jumpMoves, selectedPiece):
    jump_dict = {}
    counter = 1
    print('Below are you possible moves:')
    for key, value in jumpMoves.items():
        if value[0] == selectedPiece:
            for coords in value[1:]:
                for singleCoord in coords:
                    jump_dict.update({counter: singleCoord})
                    counter += 1
    while True:
        try:
            if len(jump_dict) < 2:
                displayPossibleMoves(jump_dict)
                selection = input('Only one move available. Please press Enter.')
                if selection == '':
                    jumpSelection = getJumpLocationBySelection(1, jump_dict)
                    return jumpSelection
                else:
                    clear()
                    displayBoard()
                    print('Please press Enter')
                pass
            else:
                displayPossibleMoves(jump_dict)
                selection = input('Choose move number: ')
                selection = int(selection)
                checkMoveIsValid = checkMoveSelection(jump_dict, selection)
                if checkMoveIsValid is True:
                    jumpSelection = getJumpLocationBySelection(selection, jump_dict)
                    return jumpSelection
                else:
                    pass
        except ValueError:
            clear()
            displayBoard()
            print('Please enter a number.')
            pass


def displayPossibleMoves(jump_dict):
    for key, moves in jump_dict.items():
        print(str(key) + ' : ' + str(moves))


def passSelectedMovePiece(move_Dict, move_selection):
    for key, value in move_Dict.items():
        if key == move_selection:
            return value


def removePaths():
    x = 0
    y = 0
    for row in board.__iter__():
        for cell in row:
            if cell == pathPiece:
                board.updateBoard([x, y], emptyCell)
            if y == 9:
                y = 0
            else:
                y += 1
        x += 1


def playerControl(piece_type):
    global i

    if i == 0:
        if piece_type == redPiece or pieceType == kingRedPiece:
            return True
        else:
            # clear()
            # displayBoard()
            # print('Please choose a red piece to move. ')
            return 'Please choose a red piece to move. '
    if i == 1:
        if piece_type == whitePiece or pieceType == kingWhitePiece:
            return True
        else:
            # clear()
            # displayBoard()
            # print('Please choose a white piece to move. ')
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


def valueOfI(i):
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
    # anyKey = input('Press any key to continue')
    if cont == '?':
        print(cont)
        return cont
    pass


# board.updateBoard([4, 3], emptyCell)
# board.updateBoard([5, 4], kingRedPiece)
# board.updateBoard([2, 1], emptyCell)
# board.updateBoard([2, 5], emptyCell)
# board.updateBoard([1, 2], emptyCell)
# board.updateBoard([6, 3], emptyCell)


clear()
while True:
    board = board.resetBoard(board)
    # board.updateBoard([2, 1], emptyCell)
    # board.updateBoard([1, 2], emptyCell)
    # board.updateBoard([3, 2], emptyCell)
    # board.updateBoard([2, 3], emptyCell)
    # board.updateBoard([1, 4], emptyCell)
    # board.updateBoard([3, 4], emptyCell)
    # board.updateBoard([2, 5], emptyCell)
    # board.updateBoard([1, 6], emptyCell)
    # board.updateBoard([3, 6], emptyCell)
    # board.updateBoard([2, 7], emptyCell)
    # board.updateBoard([1, 8], emptyCell)
    # board.updateBoard([3, 8], emptyCell)
    # board.updateBoard([5, 4], whitePiece)
    # board.updateBoard([5, 6], whitePiece)
    flow = menu()
    flowControl = True
    chainCheck = True
    typeOfGame = gameType()

    if typeOfGame == 'PvP':
        clear()
        displayBoard()
        while flowControl is True:
            if flow == 'start':
                gameOver = checkIfGameOver(i)
                if gameOver is False:
                    jumpMoves = scanBoard(i)
                    if jumpMoves != {}:
                        playerTurnPrint(i)
                        print('There are possible capture moves, please select one.')
                        selectedPiece = getLocation(pickMessage)
                        if selectedPiece is False:
                            pass
                        else:
                            selectedPiece = convertMoveToInt(selectedPiece)
                            pieceType = board.pieceType(selectedPiece)
                            control = playerControl(pieceType)
                            if control is not True:
                                clear()
                                displayBoard()
                                print(control)
                                pass
                            else:
                                checkSelectedPiece = checkIfSelectionIsCaptureMove(jumpMoves, selectedPiece)
                                if checkSelectedPiece is False:
                                    clear()
                                    displayBoard()
                                    print('Please select a capture move. ')
                                    pass
                                else:
                                    markValidMoveOnBoardCaptureMoves(jumpMoves, selectedPiece)
                                    clear()
                                    displayBoard()
                                    selectedJump = outputPossibleCaptureMoves(jumpMoves, selectedPiece)
                                    removePaths()
                                    jumpPiece(selectedPiece, selectedJump, pieceType)
                                    kingCheck = checkKingsRow(i)
                                    if kingCheck is True:
                                        clear()
                                        displayBoard()
                                        pressAnyKey()
                                        clear()
                                        displayBoardReverse()
                                        i = valueOfI(i)
                                        chainCheck = True
                                        pass
                                    else:
                                        while chainCheck is True:
                                            displayBoard()
                                            jumpMove = chainJumpScan(selectedJump, pieceType)
                                            if jumpMove == {}:
                                                chainCheck = False
                                                pass
                                            else:
                                                markValidMoveOnBoardCaptureMoves(jumpMove, selectedJump)
                                                clear()
                                                displayBoard()
                                                nextJump = outputPossibleCaptureMoves(jumpMove, selectedJump)
                                                removePaths()
                                                jumpPiece(selectedJump, nextJump, pieceType)
                                                selectedJump = nextJump
                                                kingCheck = checkKingsRow(i)
                                                if kingCheck is True:
                                                    chainCheck = False
                                        clear()
                                        displayBoard()
                                        pressAnyKey()
                                        clear()
                                        displayBoardReverse()
                                        i = valueOfI(i)
                                        chainCheck = True
                    else:
                        legalMovesCheck = checkForLegalMoves(i)
                        if legalMovesCheck is True:
                            playerTurnPrint(i)
                            selectedPiece = getLocation(pickMessage)
                            if selectedPiece is False:
                                clear()
                                displayBoard()
                                pass
                            else:
                                selectedPiece = convertMoveToInt(selectedPiece)
                                pieceType = board.pieceType(selectedPiece)
                                control = playerControl(pieceType)
                                if control is not True:
                                    clear()
                                    displayBoard()
                                    print(control)
                                    pass
                                else:
                                    availableMoves = listAvailableMoves(pieceType, selectedPiece)
                                    legalMoves = checkIfMoveIsValid(availableMoves)
                                    if legalMoves == []:
                                        clear()
                                        displayBoard()
                                        print('Please pick a movable piece.')
                                        pass
                                    else:
                                        markValidMovesOnBoard(legalMoves)
                                        clear()
                                        displayBoard()
                                        moveDict = moveSelectionInput(legalMoves)
                                        moveSelection = outputPossibleMoves(moveDict)
                                        selectedMove = passSelectedMovePiece(moveDict, moveSelection)
                                        removePaths()
                                        moveSelectedPiece(selectedPiece, pieceType, selectedMove, board)
                                        kingCheck = checkKingsRow(i)
                                        clear()
                                        displayBoard()
                                        pressAnyKey()
                                        clear()
                                        displayBoardReverse()
                                        i = valueOfI(i)
                                        chainCheck = True
                        else:
                            i = valueOfI(i)
                            banner('No more moves')
                            banner('You lose')
                            pressAnyKey()
                            # board = board.resetBoard(board)
                            break
                else:
                    i = valueOfI(i)
                    clear()
                    displayBoard()
                    num = getPlayerNumber(i)
                    player = 'Player %s' % num
                    banner('Congratulations')
                    banner(player)
                    banner('You Win!!!')
                    time.sleep(3)
                    clear()
                    # board = board.resetBoard(board)
                    break

if __name__ == '__main__':
    main()
