import checker_board_terminal as cbt
from checker_board_terminal import CheckerBoard
from pyfiglet import Figlet
from colorama import init, Fore, Back, Style
import msvcrt
import os
import re
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

pickMessage = 'Pick piece to move : '

i = 0


def banner(text):
    fig = Figlet(font='slant')
    print(fig.renderText(text))
    return True


def rules():
    rule = ('\n'
            '                                    Rules\n'
            '==================================================================================\n'
            '\n'
            '- X pieces always go first\n'
            '- Moves\n'
            '    * Capturing moves\n'
            '        ~ Capturing moves occur when a player "jumps" an opposing piece.\n'
            '            This is also done on the diagonal and can only happen when the\n'
            '            square behind (on the same diagonal) is also open.\n'
            '            This means that you may not jump an opposing piece around a corner.\n'
            '        ~ Forced Captures: When a player is in a position to make a capturing move,\n'
            '            he must make a capturing move. When he has more than one capturing\n'
            '            move to choose from he may take whichever move suits him.\n'
            '    * Non-capturing moves\n'
            '        ~ Non-capturing moves are simply a diagonal move forward from one\n'
            '            square to an adjacent square.\n'
            '    * Kinging move\n'
            '        ~ When a checker achieves the opponent\'s edge of the board\n'
            '            (called the "king\'s row") it is crowned with another checker.\n'
            '            This signifies that the checker has been made a king.\n'
            '            The king now gains an added ability to move backward.\n'
            '            The king may now also jump in either direction or even in\n'
            '            both directions in one turn (if he makes multiple jumps).\n'
            '        ~ If the player gets an uncrowned checker on the king\'s row\n'
            '            because of a capturing move then he must stop to be crowned\n'
            '            even if another capture seems to be available.\n'
            '            He may then use his new king on his next move.\n'
            '\n'
            '----------------------------------------------------------------------------------\n')
    # print(rules)
    return rule


def instructions():
    instruction = ('\n'
                   '                                   Instructions\n'
                   '==================================================================================\n'
                   '\n'
                   '- Player who is using the X pieces will go first.\n'
                   '- Move paths will be shown via asterisks (*).\n'
                   '- The player will select the piece they would like to move.\n'
                   '    * This is done by selecting the coordinates of the piece.\n'
                   '    * First you choose 1-8 along the left or right.\n'
                   '    * Then you choose 1-8 on the top or bottom.\n'
                   '    * Enter your selection as 3,4 or 6,3.\n'
                   '- If any capture moves are possible, the game will list those moves and you will\n'
                   '    select which move you would like to make.\n'
                   '- If a player’s piece lands on the King’s row it has to stop to be Kinged and\n'
                   '    the turn passes to the next player.\n'
                   '- Once either player has no more moves or pieces, the other player wins.\n'
                   '\n'
                   '----------------------------------------------------------------------------------\n')
    # print(instructions)
    return instruction


def menuSelection():
    # inputFormat = re.compile("[0-9][,./]")
    selection = input('Would you like to [S]tart a new game, see the [R]ules, [I]nstructions, or [E]xit? ').lower()

    return selection


def displayBoard():
    board.printCheckerBoard()


def displayBoardReverse():
    board.reverseBoard()
    board.actualBoardReversal()
    board.printCheckerBoard()


def menu():
    banner('Checkers!')
    selection = menuSelection()
    while True:
        if selection == 's':
            # displayBoard()
            # pickedPiece = getLocation(pick)
            # return pickedPiece
            whileVar = False
            return whileVar
        elif selection == 'r':
            # rules()
            # selection = menuSelection()
            whileVar = False
            return whileVar
        elif selection == 'i':
            # instructions()
            # selection = menuSelection()
            whileVar = False
            return whileVar
        elif selection == 'e':
            # quit()
            whileVar = False
            return whileVar
        else:
            print('Please choose "S", "R", "I" or "E".')
            selection = menuSelection()


def getLocation(location, testInput):
    # move = input(location)
    move = testInput
    moveCheck = re.compile('^\d{1}([\W]{1})\d{1}$')
    moveMatch = re.fullmatch(moveCheck, move)
    if moveMatch is None:
        return False
    else:
        return move


def convertMoveToInt(move):
    for chars in move:
        if chars in ' .,/<>?\|':
            moveInt = move.split(chars)
    # print('MoveInt ' + str(moveInt))
    moveInt = list(map(int, moveInt))
    return moveInt


def removeOuterBracket(coord):
    for singleCoord in coord:
        return singleCoord


# possibly no longer need this function
# def checkPieceType(selectedPiece):
#     if board[selectedPiece[0]][selectedPiece[1]] == whitePiece:
#         return whitePiece
#     elif board[selectedPiece[0]][selectedPiece[1]] == redPiece:
#         return redPiece
#     else:
#         return emptyCell


def checkIfMoveIsValid(possibleMoves, pieceType):
    legalMoves = []
    # otherPiece = otherPieceCheck(pieceType)
    for coords in possibleMoves:
        checkedPiece = board.pieceType(coords)
        # if checkedPiece != redPiece and checkedPiece != whitePiece and checkedPiece != emptyCell:
        #     pass
        # elif checkedPiece == pieceType:
        #     pass
        # elif checkedPiece == otherPiece:
        #     pass
        # else:
        if checkedPiece == emptyCell:
            legalMoves.append(coords)
    # print('legalMoves ' + str(legalMoves))
    return legalMoves


def checkIfMoveIsValidKing(possibleMoves, pieceType, testBoard):
    legalMoves = []
    # otherPiece = otherPieceCheck(pieceType)
    for coords in possibleMoves:
        checkedPiece = testBoard.pieceType(coords)
        # print('checkedPiece ' + str(checkedPiece))
        # if checkedPiece != redPiece and checkedPiece != whitePiece and checkedPiece != emptyCell and checkedPiece != kingRedPiece and checkedPiece != kingWhitePiece:
        #     # this checks if it is a valid play area
        #     print('first if statement')
        #     pass
        # elif checkedPiece == pieceType:
        #     print('second if statement')
        #     pass
        # elif checkedPiece == otherPiece:
        #     print('third if statement')
        #     pass
        # else:
        if checkedPiece == emptyCell:
            legalMoves.append(coords)
    # print('legalMoves ' + str(legalMoves))
    return legalMoves


def calculateAvailableMoves(selectedPiece):
    availableMoves = [[sum(x) for x in zip(selectedPiece, moveLeftUp)],
                      [sum(x) for x in zip(selectedPiece, moveRightUp)]]
    return availableMoves


def calculateKingMoves(selectedPiece):
    upMoves = calculateAvailableMoves(selectedPiece)
    downMoves = [[sum(x) for x in zip(selectedPiece, moveLeftDown)],
                    [sum(x) for x in zip(selectedPiece, moveRightDown)]]
    for coord in downMoves:
        upMoves.append(coord)
    return upMoves


def endLocationCheck(endLocation, testBoard):
    legalJumps = []
    for coord in endLocation:
        # print('coord ' + str(coord))
        pieceType = testBoard.pieceType(coord)
        if pieceType == emptyCell:
            legalJumps.append(coord)
            # return True
    return legalJumps


def checkKingsRow(playerTurn, testBoard):
    if playerTurn == 0:
        pieceType = redPiece
        kingPiece = kingRedPiece
    if playerTurn == 1:
        pieceType = whitePiece
        kingPiece = kingWhitePiece

    y = 0
    board = testBoard.__iter__()
    for cell in board[1]:
        if cell == pieceType:
            testBoard.updateBoard([1, y], kingPiece)
        y += 1
    return testBoard


def checkIfGameOver(playerTurn, testBoard):
    if playerTurn == 0:
        otherPieceType = whitePiece
        otherKingPiece = kingWhitePiece
    if playerTurn == 1:
        otherPieceType = redPiece
        otherKingPiece = kingRedPiece

    for row in testBoard.__iter__():
        for cell in row:
            if cell == otherPieceType or cell == otherKingPiece:
                return False
    return True


def checkForLegalMoves(playerTurn, testBoard):
    if playerTurn == 0:
        pieceType = redPiece
        kingPiece = kingRedPiece
    if playerTurn == 1:
        pieceType = whitePiece
        kingPiece = kingWhitePiece

    x = 0
    y = 0
    for row in testBoard.__iter__():
        for cell in row:
            if cell == pieceType:
                availableMoves = calculateAvailableMoves([x, y])
                legalMoves = checkIfMoveIsValidKing(availableMoves, pieceType, testBoard)
                # print('legalMoves ' + str(legalMoves))
                if legalMoves == []:
                    pass
                else:
                    return True
            if cell == kingPiece:
                availableMoves = calculateAvailableMoves([x, y])
                legalMoves = checkIfMoveIsValidKing(availableMoves, kingPiece, testBoard)
                # print('legalMoves ' + str(legalMoves))
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

def scanBoard(playerTurn, testBoard):
    if playerTurn == 0:
        pieceType = redPiece
        kingPiece = kingRedPiece
    if playerTurn == 1:
        pieceType = whitePiece
        kingPiece = kingWhitePiece

    scanDict = {}
    key = 1
    x = 0
    y = 0
    for row in testBoard.__iter__():
        for cell in row:
            if cell == pieceType:
                # print('cell ' + str(cell))
                availableMoves = listAvailableMoves(pieceType, [x, y])
                # print('availableMoves ' + str(availableMoves))
                jumpMoves = checkIfCaptureMove(pieceType, availableMoves, testBoard)
                # print('jumpMoves ' + str(jumpMoves))
                if jumpMoves == []:
                    # print('Please pick a movable piece.')
                    pass
                else:
                    endLocation = calculateCaptureMove([x, y], jumpMoves)
                    # print('endLocation ' + str(endLocation))
                    checkEndLocation = endLocationCheck(endLocation, testBoard)
                    # print('checkEndLocation ' + str(checkEndLocation))
                    if checkEndLocation != []:
                        formatCheckEndLocation = removeOuterBracket(checkEndLocation)
                        possibleChainJump = listAvailableMoves(pieceType, formatCheckEndLocation)
                        # print('possibleChainJump ' + str(possibleChainJump))
                        chainJump = checkIfCaptureMove(pieceType, possibleChainJump, testBoard)
                        # print('chainJump ' + str(chainJump))
                        formatCheckEndLocation = removeOuterBracket(checkEndLocation)
                        chainEndLocation = calculateCaptureMove(formatCheckEndLocation, chainJump)
                        checkChainEndLocation = endLocationCheck(chainEndLocation, testBoard)
                        # print('checkChainEndLocation ' + str(checkChainEndLocation))
                        # if checkChainEndLocation != []:
                        #     checkEndLocation = removeOuterBracket(checkEndLocation)
                        #     checkChainEndLocation = removeOuterBracket(checkChainEndLocation)
                        #     scanDict.update({key: [[x, y], (checkEndLocation, checkChainEndLocation)]})
                        #     key += 1
                        # else:
                        scanDict.update({key: [[x, y], checkEndLocation]})
                        key += 1

            if cell == kingPiece:
                # print('cell ' + str(cell))
                # print('if cell = kingPiece entered')
                availableMoves = listAvailableMoves(kingPiece, [x, y])
                # print('availableMoves ' + str(availableMoves))
                jumpMoves = checkIfCaptureMove(kingPiece, availableMoves, testBoard)
                # print('jumpMoves ' + str(jumpMoves))
                if jumpMoves == []:
                    # print('jumpMoves King check entered')
                    pass
                else:
                    endLocation = calculateCaptureMove([x, y], jumpMoves)
                    # print('endLocation ' + str(endLocation))
                    checkEndLocation = endLocationCheck(endLocation, testBoard)
                    # print('checkEndLocation ' + str(checkEndLocation))
                    if checkEndLocation != []:
                        scanDict.update({key: [[x, y], checkEndLocation]})
                        key += 1

            if y == 9:
                y = 0
            else:
                y += 1
        x += 1
    # print(scanDict)
    return scanDict
    # testBoard.printCheckerBoard()
    # print(scanDict)
    # if scanDict != {}:
    #     return True


def chainJumpScan(jumpPiece, pieceType, testBoard):
    jumpDict = {}
    key = 1
    availableMoves = listAvailableMoves(pieceType, jumpPiece)
    # print(availableMoves)
    jumpMove = checkIfCaptureMove(pieceType, availableMoves, testBoard)
    # print('jumpMove ' + str(jumpMove))
    jumpMove = calculateCaptureMove(jumpPiece, jumpMove)
    # print('jumpMove ' + str(jumpMove))
    jumpMove = endLocationCheck(jumpMove, testBoard)
    # print('jumpMove ' + str(jumpMove))
    # for moves in jumpMove:
    if jumpMove != []:
        jumpDict.update({key: [jumpPiece, jumpMove]})
        key += 1
    return jumpDict


def checkIfCaptureMove(pieceType, availableMoves, testBoard):
    jumpMoves = []
    otherPiece = otherPieceCheck(pieceType)
    # print('otherPiece[0] ' + str(otherPiece[0]))
    # print('otherPiece[1] ' + str(otherPiece[1]))
    # print(type(otherPiece))
    for coords in availableMoves:
        coordsType = testBoard.pieceType(coords)
        # print('coordsType ' + str(coordsType))
        if coordsType == otherPiece[0] or coordsType == otherPiece[1]:
            jumpMoves.append(coords)
    return jumpMoves


def calculateCaptureMove(selectedPiece, jumpPiece):
    jumpedLocation = []
    for coords in jumpPiece:
        increaseAmount = [(coords[0] - selectedPiece[0])*2, (coords[1] - selectedPiece[1])*2]
        jumpedLocationCalc = [(selectedPiece[0] + increaseAmount[0]), (selectedPiece[1] + increaseAmount[1])]
        jumpedLocation.append(jumpedLocationCalc)
        # print('jumpedLocation ' + str(jumpedLocation))
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


def listAvailableMoves(selectedPieceType, selectedPiece):
    if selectedPieceType == whitePiece or selectedPieceType == redPiece:
        availableMoves = calculateAvailableMoves(selectedPiece)
        return availableMoves
    elif selectedPieceType == kingRedPiece or selectedPieceType == kingWhitePiece:
        availableMoves = calculateKingMoves(selectedPiece)
        return availableMoves
    else:
        clear()
        displayBoard()
        print('Please pick a movable piece.')
        return False


def moveSelectedPiece(selectedPiece, pieceType, pickedMove, newMoveBoard):
    newMoveBoard.updateBoard(pickedMove, pieceType)
    newMoveBoard.updateBoard(selectedPiece, emptyCell)


def jumpPiece(selectedPiece, jumpMove, pieceType, jumpBoard):
    removedPiece = calculateRemovePiece(selectedPiece, jumpMove)
    jumpBoard.updateBoard(jumpMove, pieceType)
    jumpBoard.updateBoard(removedPiece, emptyCell)
    jumpBoard.updateBoard(selectedPiece, emptyCell)


def markValidMovesOnBoard(validMoves, validBoard):
    for coords in validMoves:
        validBoard.updateBoard(coords, pathPiece)
    # testPathPiece = validBoard[coords[0]][coords[1]]
    return validBoard


def markValidMoveOnBoardCaptureMoves(jumpDict, selectedPiece, testBoard):
    for key, value in jumpDict.items():
        if value[0] == selectedPiece:
            for pathCoord in value[1]:
                # print('pathCoord ' + str(pathCoord))
                testBoard.updateBoard(pathCoord, pathPiece)


def moveSelectionInput(validMoves):
    inputDict = {}
    key = 1
    for coords in validMoves:
        inputDict.update({key: coords})
        key += 1
    return inputDict


def scanBoardEasy(playerTurn):
    # scannedCells = []
    scanDict = {}
    key = 1
    x = 0
    y = 0
    if playerTurn == 1:
        for row in board.__iter__():
            for cell in row:
                if cell == redPiece:
                    availableMoves = calculateAvailableMoves([x, y])
                    legalMoves = checkIfMoveIsValid(availableMoves, redPiece)
                    # print('legalMoves ' + str(legalMoves))
                    if legalMoves == []:
                        # print('Please pick a movable piece.')
                        pass
                    else:
                        scanDict.update({key: [[x, y], legalMoves]})
                        key += 1
                        # scannedCells.append(legalMoves)
                if y == 9:
                    y = 0
                else:
                    y += 1
            x += 1
    else:
        for row in board.__iter__():
            for cell in row:
                if cell == whitePiece:
                    availableMoves = calculateAvailableMoves([x, y])
                    legalMoves = checkIfMoveIsValid(availableMoves, whitePiece)
                    # print('legalMoves ' + str(legalMoves))
                    if legalMoves == []:
                        # print('Please pick a movable piece.')
                        pass
                    else:
                        scanDict.update({key: [[x, y], legalMoves]})
                        key += 1
                        # scannedCells.append(legalMoves)
                if y == 9:
                    y = 0
                else:
                    y += 1
            x += 1
    return scanDict# , scannedCells




# clear = lambda: os.system('cls')
def clear():
    osName = os.name
    if osName == 'nt':
        return osName
        # clear = 'cls'
    else:
        return osName
        # clear = 'clear'
    # os.system(clear)


def checkMoveSelection(outputDict, selection):
    for key, value in outputDict.items():
        if selection == key:
            return True
    return False
    # clear()
    # displayBoard()
    # print('Please select one of the below options.')
    # return False


def checkIfSelectionIsCaptureMove(jumpMoves, selectedPiece):
    for key, value in jumpMoves.items():
        if value[0] == selectedPiece:
            return True
    return False


def getJumpLocationBySelection(selection, jump_dict):
    for key, value in jump_dict.items():
        if selection == key:
            return value


def outputPossibleMoves(outputDict, testSelection):
    whileVar = True
    while whileVar:
        # print('Below are you possible moves:')
        try:
            if len(outputDict) < 2:
                displayPossibleMoves(outputDict)
                # selection = input('Only one move available. Please press Enter.')
                selection = testSelection
                if selection == '':
                    return 1
                pass
            else:
                displayPossibleMoves(outputDict)
                # selection = input('Choose move number: ')
                selection = testSelection
                selection = int(selection)
                checkMoveIsValid = checkMoveSelection(outputDict, selection)
                if checkMoveIsValid is True:
                    return selection
                else:
                    # return False
                    pass
        except ValueError:
            # clear()
            # displayBoard()
            # print('Please enter a number.')
            # print('Enter failed test')
            return False
            pass


def outputPossibleCaptureMoves(jumpMoves, selectedPiece, testSelection):
    whileVar = True
    counter = 1
    # print('Below are you possible moves:')
    for key, value in jumpMoves.items():
        if value[0] == selectedPiece:
            for coords in value[1:]:
                # # print('coords ' + str(coords))
                # # print(type(coords))
                # if isinstance(coords, tuple):
                #     # print(str(counter) + ' : ' + str(coords[0]) + ', ' + str(coords[1]))
                #     jump_dict.update({counter: [coords[0], coords[1]]})
                #     # jump_dict.update({counter: coords})
                #     counter += 1
                # else:
                for singleCoord in coords:
                    jumpMoves.update({counter: singleCoord})
                    counter += 1
    while whileVar:
        try:
            # selection = input('Choose move number: ')
            # print('jump_dict ' + str(jump_dict))
            if len(jumpMoves) < 2:
                displayPossibleMoves(jumpMoves)
                selection = testSelection
                # selection = input('Only one move available. Please press Enter.')
                if selection == '':
                    jumpSelection = getJumpLocationBySelection(1, jumpMoves)
                    return jumpSelection
                else:
                    # clear()
                    # displayBoard()
                    print('Please press Enter')
                    return False
                pass
            else:
                displayPossibleMoves(jumpMoves)
                selection = testSelection
                # selection = input('Choose move number: ')
                selection = int(selection)
                checkMoveIsValid = checkMoveSelection(jumpMoves, selection)
                if checkMoveIsValid is True:
                    jumpSelection = getJumpLocationBySelection(selection, jumpMoves)
                    return jumpSelection
                else:
                    return False
                    pass
        except ValueError:
            # clear()
            # displayBoard()
            # print('Please enter a number.')
            return False
            pass


def displayPossibleMoves(jump_dict):
    for key, moves in jump_dict.items():
        # print(str(key) + ' : ' + str(moves))
        pass


# Possible Easy mode function
def outputSelectionPiece(selectDict):
    whileVar = True
    while whileVar:
        print('Please select a piece to move: ')
        for key, value in selectDict.items():
            print(str(key) + ' : ' + str(value[0]))
        selection = int(input('Which piece do you want to move? '))
        checkIfValidInput = checkMoveSelection(selectDict, selection)
        if checkIfValidInput:
            return selection
        else:
            pass


def passSelectedMovePiece(moveDict, moveSelection):
    for key, value in moveDict.items():
        if key == moveSelection:
            return value


def removePaths(removeBoard):
    x = 0
    y = 0
    for row in removeBoard.__iter__():
        for cell in row:
            if cell == pathPiece:
                removeBoard.updateBoard([x, y], emptyCell)
            if y == 9:
                y = 0
            else:
                y += 1
        x += 1


def playerControl(pieceType):
    i = 0
    # print('i = ' + str(i))
    # print('pieceType ' + str(pieceType))
    if i == 0:
        if pieceType == redPiece or pieceType == kingRedPiece:
            i = 1
            return True
        else:
            print('Please choose a red piece to move. ')
            return False

    if i == 1:
        if pieceType == whitePiece or pieceType == kingWhitePiece:
            i = 0
            return True
        else:
            print('Please choose a white piece to move. ')
            return False


def getPlayerNumber(i):
    if i == 0:
        return '1'
    else:
        return '2'


def gameType():
    gameSelection = input('Would you like to play [P]vP or Pv[C]? ').lower()
    whileVar = True
    while whileVar:
        if gameSelection == 'p':
            whileVar = False
            return 'PvP'
        elif gameSelection == 'c':
            print('Not implemented yet')
            gameSelection = input('Would you like to play [P]vP or Pv[C]? ').lower()


def pressAnyKey(key):
    anyKey = msvcrt.getch()
    # anyKey = key
    for char in anyKey:
        if char == 63:
            print('char ' + str(char))
            return char
        return char