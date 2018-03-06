from checker_board_terminal import CheckerBoard
import checker_board_terminal as cbt
from colorama import init
import time
import utility as ut
import logic as lg


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




ut.clear()
while True:
    board = board.resetBoard()

    flow = ut.menu()
    flowControl = True
    chainCheck = True
    typeOfGame = ut.gameType()

    if typeOfGame == 'PvP':
        ut.clear()
        lg.displayBoard(board)
        while flowControl is True:
            if flow == 'start':
                gameOver = lg.checkIfGameOver(i, board)
                if gameOver is False:
                    jumpMoves = lg.scanBoard(i, board)
                    if jumpMoves != {}:
                        ut.playerTurnPrint(i)
                        print('There are possible capture moves, please select one.')
                        selectedPiece = ut.getLocation(pickMessage)
                        if selectedPiece is False:
                            pass
                        else:
                            selectedPiece = ut.convertMoveToInt(selectedPiece)
                            pieceType = board.pieceType(selectedPiece)
                            control = ut.playerControl(pieceType, i)
                            if control is not True:
                                ut.clear()
                                lg.displayBoard(board)
                                print(control)
                                pass
                            else:
                                checkSelectedPiece = lg.checkIfSelectionIsCaptureMove(jumpMoves, selectedPiece)
                                if checkSelectedPiece is False:
                                    ut.clear()
                                    lg.displayBoard(board)
                                    print('Please select a capture move. ')
                                    pass
                                else:
                                    lg.markValidMoveOnBoardCaptureMoves(jumpMoves, selectedPiece, board)
                                    ut.clear()
                                    lg.displayBoard(board)
                                    selectedJump = lg.outputPossibleCaptureMoves(jumpMoves, selectedPiece, board)
                                    lg.removePaths(board)
                                    lg.jumpPiece(selectedPiece, selectedJump, pieceType, board)
                                    kingCheck = lg.checkKingsRow(i, board)
                                    if kingCheck is True:
                                        ut.clear()
                                        lg.displayBoard(board)
                                        ut.pressAnyKey()
                                        ut.clear()
                                        lg.displayBoardReverse(board)
                                        i = ut.changeValueOfI(i)
                                        chainCheck = True
                                        pass
                                    else:
                                        while chainCheck is True:
                                            lg.displayBoard(board)
                                            jumpMove = lg.chainJumpScan(selectedJump, pieceType, board)
                                            if jumpMove == {}:
                                                chainCheck = False
                                                pass
                                            else:
                                                lg.markValidMoveOnBoardCaptureMoves(jumpMove, selectedJump, board)
                                                ut.clear()
                                                lg.displayBoard(board)
                                                nextJump = lg.outputPossibleCaptureMoves(jumpMove, selectedJump, board)
                                                lg.removePaths(board)
                                                lg.jumpPiece(selectedJump, nextJump, pieceType, board)
                                                selectedJump = nextJump
                                                kingCheck = lg.checkKingsRow(i, board)
                                                if kingCheck is True:
                                                    chainCheck = False
                                        ut.clear()
                                        lg.displayBoard(board)
                                        ut.pressAnyKey()
                                        ut.clear()
                                        lg.displayBoardReverse(board)
                                        i = ut.changeValueOfI(i)
                                        chainCheck = True
                    else:
                        legalMovesCheck = lg.checkForLegalMoves(i, board)
                        if legalMovesCheck is True:
                            ut.playerTurnPrint(i)
                            selectedPiece = ut.getLocation(pickMessage)
                            if selectedPiece is False:
                                ut.clear()
                                lg.displayBoard(board)
                                pass
                            else:
                                selectedPiece = ut.convertMoveToInt(selectedPiece)
                                pieceType = board.pieceType(selectedPiece)
                                control = ut.playerControl(pieceType, i)
                                if control is not True:
                                    ut.clear()
                                    lg.displayBoard(board)
                                    print(control)
                                    pass
                                else:
                                    availableMoves = lg.listAvailableMoves(pieceType, selectedPiece, board)
                                    legalMoves = lg.checkIfMoveIsValid(availableMoves, board)
                                    if legalMoves == []:
                                        ut.clear()
                                        lg.displayBoard(board)
                                        print('Please pick a movable piece.')
                                        pass
                                    else:
                                        lg.markValidMovesOnBoard(legalMoves, board)
                                        ut.clear()
                                        lg.displayBoard(board)
                                        moveDict = lg.moveSelectionInput(legalMoves)
                                        moveSelection = lg.outputPossibleMoves(moveDict, board)
                                        selectedMove = ut.passSelectedMovePiece(moveDict, moveSelection)
                                        lg.removePaths(board)
                                        lg.moveSelectedPiece(selectedPiece, pieceType, selectedMove, board)
                                        kingCheck = lg.checkKingsRow(i, board)
                                        ut.clear()
                                        lg.displayBoard(board)
                                        ut.pressAnyKey()
                                        ut.clear()
                                        lg.displayBoardReverse(board)
                                        i = ut.changeValueOfI(i)
                                        chainCheck = True
                        else:
                            i = ut.changeValueOfI(i)
                            ut.banner('No more moves')
                            ut.banner('You lose')
                            ut.pressAnyKey()
                            break
                else:
                    i = ut.changeValueOfI(i)
                    ut.clear()
                    lg.displayBoard(board)
                    num = ut.getPlayerNumber(i)
                    player = 'Player %s' % num
                    ut.banner('Congratulations')
                    ut.banner(player)
                    ut.banner('You Win!!!')
                    time.sleep(3)
                    ut.clear()
                    break

if __name__ == '__main__':
    main()
