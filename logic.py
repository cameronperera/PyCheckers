import utility as ut
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

def checkIfMoveIsValid(possibleMoves, board):
    legal_moves = []
    for coords in possibleMoves:
        checkedPiece = board.pieceType(coords)
        if checkedPiece == emptyCell:
            legal_moves.append(coords)
    return legal_moves

def calculateAvailableMoves(coords):
    available_moves = [[sum(x) for x in zip(coords, moveLeftUp)],
                       [sum(x) for x in zip(coords, moveRightUp)]]
    return available_moves

def calculateKingMoves(selectedPiece):
    upMoves = calculateAvailableMoves(selectedPiece)
    downMoves = [[sum(x) for x in zip(selectedPiece, moveLeftDown)],
                 [sum(x) for x in zip(selectedPiece, moveRightDown)]]
    for coord in downMoves:
        upMoves.append(coord)
    return upMoves

def endLocationCheck(endLocation, board):
    legalJumps = []
    for coord in endLocation:
        piece_type = board.pieceType(coord)
        if piece_type == emptyCell:
            legalJumps.append(coord)
    return legalJumps

def checkKingsRow(playerTurn, board):
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

def checkIfGameOver(playerTurn, board):
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

def checkForLegalMoves(playerTurn, board):
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
                legalMoves = checkIfMoveIsValid(availableMoves, board)
                if legalMoves == []:
                    pass
                else:
                    return True
            if cell == kingPiece:
                availableMoves = calculateAvailableMoves([x, y])
                legalMoves = checkIfMoveIsValid(availableMoves, board)
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

def scanBoard(playerTurn, board):
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
                available_moves = listAvailableMoves(piece_type, [x, y], board)
                jump_moves = checkIfCaptureMove(piece_type, available_moves, board)
                if jump_moves == []:
                    pass
                else:
                    endLocation = calculateCaptureMove([x, y], jump_moves)
                    checkEndLocation = endLocationCheck(endLocation, board)
                    if checkEndLocation != []:
                        scanDict.update({key: [[x, y], checkEndLocation]})
                        key += 1

            if cell == kingPiece:
                available_moves = listAvailableMoves(kingPiece, [x, y], board)
                jump_moves = checkIfCaptureMove(kingPiece, available_moves, board)
                if jump_moves == []:
                    pass
                else:
                    endLocation = calculateCaptureMove([x, y], jump_moves)
                    checkEndLocation = endLocationCheck(endLocation, board)
                    if checkEndLocation != []:
                        scanDict.update({key: [[x, y], checkEndLocation]})
                        key += 1
            if y == 9:
                y = 0
            else:
                y += 1
        x += 1
    return scanDict

def chainJumpScan(jump_piece, piece_type, board):
    jumpDict = {}
    key = 1
    jump_pieceType = board.pieceType(jump_piece)
    if jump_pieceType == piece_type:
        available_moves = listAvailableMoves(piece_type, jump_piece, board)
        checkedJumpMove = checkIfCaptureMove(piece_type, available_moves, board)
        calculateJumpMove = calculateCaptureMove(jump_piece, checkedJumpMove)
        jumpMove = endLocationCheck(calculateJumpMove, board)
        if jumpMove != []:
            jumpDict.update({key: [jump_piece, jumpMove]})
            key += 1
    return jumpDict

def checkIfCaptureMove(piece_type, available_moves, board):
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

def listAvailableMoves(selectedPieceType, selected_Piece, board):
    if selectedPieceType == whitePiece or selectedPieceType == redPiece:
        availableMoves = calculateAvailableMoves(selected_Piece)
        return availableMoves
    elif selectedPieceType == kingRedPiece or selectedPieceType == kingWhitePiece:
        availableMoves = calculateKingMoves(selected_Piece)
        return availableMoves
    else:
        ut.clear()
        displayBoard(board)
        print('Please pick a movable piece.')
        return False

def moveSelectedPiece(selected_piece, piece_type, pickedMove, newMoveBoard):
    newMoveBoard.updateBoard(pickedMove, piece_type)
    newMoveBoard.updateBoard(selected_piece, emptyCell)

def jumpPiece(selectedPiece, jumpMove, pieceType, board):
    removedPiece = calculateRemovePiece(selectedPiece, jumpMove)
    board.updateBoard(jumpMove, pieceType)
    board.updateBoard(removedPiece, emptyCell)
    board.updateBoard(selectedPiece, emptyCell)

def markValidMovesOnBoard(validMoves, board):
    for coords in validMoves:
        board.updateBoard(coords, pathPiece)

def markValidMoveOnBoardCaptureMoves(jumpDict, selectedPiece, board):
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

def checkMoveSelection(outputDict, selection, board):
    for key, value in outputDict.items():
        if selection == key:
            return True
    ut.clear()
    displayBoard(board)
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

def outputPossibleMoves(outputDict, board):
    while True:
        try:
            print('Below are you possible moves:')
            if len(outputDict) < 2:
                ut.displayPossibleMoves(outputDict)
                selection = input('Only one move available. Please press Enter.')
                if selection == '':
                    return 1
                else:
                    ut.clear()
                    displayBoard(board)
                    print('Please press Enter')
                pass
            else:
                ut.displayPossibleMoves(outputDict)
                selection = input('Choose move number: ')
                selection = int(selection)
                checkMoveIsValid = checkMoveSelection(outputDict, selection, board)
                if checkMoveIsValid is True:
                    return selection
                else:
                    pass
        except ValueError:
            ut.clear()
            displayBoard(board)
            print('Please enter a number.')
            pass

def outputPossibleCaptureMoves(jumpMoves, selectedPiece, board):
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
                ut.displayPossibleMoves(jump_dict)
                selection = input('Only one move available. Please press Enter.')
                if selection == '':
                    jumpSelection = getJumpLocationBySelection(1, jump_dict)
                    return jumpSelection
                else:
                    ut.clear()
                    displayBoard(board)
                    print('Please press Enter')
                pass
            else:
                ut.displayPossibleMoves(jump_dict)
                selection = input('Choose move number: ')
                selection = int(selection)
                checkMoveIsValid = checkMoveSelection(jump_dict, selection, board)
                if checkMoveIsValid is True:
                    jumpSelection = getJumpLocationBySelection(selection, jump_dict)
                    return jumpSelection
                else:
                    pass
        except ValueError:
            ut.clear()
            displayBoard(board)
            print('Please enter a number.')
            pass

def removePaths(board):
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

def displayBoard(board):
    board.printCheckerBoard()

def displayBoardReverse(board):
    board.reverseBoardView()
    board.actualBoardReversal()
    board.printCheckerBoard()