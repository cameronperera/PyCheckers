#!/usr/bin/python3
import checkers as ch
from checker_board_terminal import CheckerBoard
import checker_board_terminal as cbt
import unittest
from colorama import init, Fore, Back, Style
import utility as ut
import logic as lg

init(autoreset=True, convert=True)

START = '\033[4m'
END = '\033[0m'

emptyCell = (Back.BLACK + '   ' + Fore.RESET)
pinkCell = (Style.BRIGHT + Back.RED + '   ' + Fore.RESET)
whitePiece = (Back.BLACK + Fore.WHITE + START + ' O ' + END + Fore.RESET)
redPiece = (Back.BLACK + Style.BRIGHT + Fore.MAGENTA + START + ' X ' + END + Fore.RESET)
pathPiece = (Back.BLACK + Style.BRIGHT + Fore.GREEN + START + ' * ' + END + Fore.RESET)
kingRedPiece = cbt.kingRedPiece
kingWhitePiece = cbt.kingWhitePiece

currentLocation = 'Pick piece to move :'

testSelectedPiece = [6, 1]
rulesTest = ('\n'
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

testInstructions = ('\n'
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


class TestGame(unittest.TestCase):

    def setUp(self):
        self.board = CheckerBoard()
    # Utility Test
    def test_playerControl_0_RedPiece_Should_Return_True(self):
        result = ut.playerControl(redPiece, 0)
        self.assertTrue(result)

    def test_playerControl_0_kingRedPiece_Should_Return_True(self):
        result = ut.playerControl(kingRedPiece, 0)
        self.assertTrue(result)

    def test_playerControl_0_whitePiece_Should_Return_String(self):
        result = ut.playerControl(whitePiece, 0)
        expected = 'Please choose a red piece to move. '
        self.assertEqual(expected, result)

    def test_playerControl_0_kingWhitePiece_Should_Return_String(self):
        result = ut.playerControl(kingWhitePiece, 0)
        expected = 'Please choose a red piece to move. '
        self.assertEqual(expected, result)

    def test_playerControl_1_whitePiece_Should_Return_True(self):
        result = ut.playerControl(whitePiece, 1)
        self.assertTrue(result)

    def test_playerControl_1_kingWhitePiece_Should_Return_True(self):
        result = ut.playerControl(kingWhitePiece, 1)
        self.assertTrue(result)

    def test_playerControl_1_redPiece_Should_Return_String(self):
        result = ut.playerControl(redPiece, 1)
        expected = 'Please choose a white piece to move. '
        self.assertEqual(expected, result)

    def test_playerControl_1_kingRedPiece_Should_Return_String(self):
        result = ut.playerControl(kingRedPiece, 1)
        expected = 'Please choose a white piece to move. '
        self.assertEqual(expected, result)

    def test_playerControl_0_emptyCell_Should_Return_String(self):
        result = ut.playerControl(emptyCell, 0)
        expected = 'Please choose a red piece to move. '
        self.assertEqual(expected, result)

    def test_playerControl_1_emptyCell_Should_Return_String(self):
        result = ut.playerControl(emptyCell, 1)
        expected = 'Please choose a white piece to move. '
        self.assertEqual(expected, result)

    def test_iEqualZero_ShouldReturnOne(self):
        i = 0
        result = ut.changeValueOfI(i)
        self.assertEqual(1, result)

    def test_iEqualOne_ShouldReturnZero(self):
        i = 1
        result = ut.changeValueOfI(i)
        self.assertEqual(0, result)

    def test_ShouldRemoveExtraBrackets(self):
        coord = [[1, 2]]
        expected = [1, 2]
        result = ut.removeOuterBracket(coord)
        self.assertEqual(expected, result)

    def test_UserInputOne_ShouldReturnFirstItemInDictionary(self):
        testDict = {1: [5, 2], 2: [5, 4]}
        testOutput = 1
        pickedMove = ut.passSelectedMovePiece(testDict, testOutput)
        self.assertEqual(pickedMove, [5, 2])

    def test_UserInputTwo_ShouldReturnSecondItemInDictionary(self):
        testDict = {1: [5, 2], 2: [5, 4]}
        testOutput = 2
        pickedMove = ut.passSelectedMovePiece(testDict, testOutput)
        self.assertEqual(pickedMove, [5, 4])

    # Logic Test
    def test_ShouldReturnLegalMoves_FromFreshBoard_OneValid(self):
        testAvailableMoves = [[0, 5], [5, 2]]
        validMoves = lg.checkIfMoveIsValid(testAvailableMoves, self.board)
        self.assertEqual(validMoves, [[5, 2]])

    def test_ShouldReturnLegalMoves_FromFreshBoard_Empty(self):
        testAvailableMoves = [[0, 5], [1, 2]]
        validMoves = lg.checkIfMoveIsValid(testAvailableMoves, self.board)
        self.assertEqual(validMoves, [])

    def test_ShouldReturnLegalMoves_FromFreshBoard_BothValid(self):
        testAvailableMoves = [[5, 4], [5, 6]]
        validMoves = lg.checkIfMoveIsValid(testAvailableMoves, self.board)
        self.assertEqual(validMoves, [[5, 4], [5, 6]])



# class TestCheckers(unittest.TestCase):
#     # @unittest.skip(' ')
#     def test_clearScreen(self):
#         clearTest = ch.clear()
#         self.assertEqual(clearTest, 'nt')
#
#     @unittest.skip('I do not feel like running it!')
#     def test_banner(self):
#         banner = ch.banner('Checkers!')
#         self.assertEqual(banner, True)
#
#     @unittest.skip('I do not feel like running it!')
#     def test_menu(self):
#         menuScreen = ch.menu()
#         self.assertEqual(menuScreen, False)
#
#     @unittest.skip('I do not feel like running it!')
#     def test_rules(self):
#         rules = ch.rules()
#         self.assertEqual(rules, rulesTest)
#
#     @unittest.skip('I do not feel like running it!')
#     def test_instructions(self):
#         instructions = ch.instructions()
#         self.assertEqual(instructions, testInstructions)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_getLocationSpace(self):
#         testInput = '6 3'
#         move = ch.getLocation(currentLocation, testInput)
#         self.assertEqual(move, '6 3')
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_getLocationPeriod(self):
#         testInput = '6.3'
#         move = ch.getLocation(currentLocation, testInput)
#         self.assertEqual(move, '6.3')
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_getLocationNoSpace(self):
#         testInput = '63'
#         move = ch.getLocation(currentLocation, testInput)
#         self.assertEqual(move, False)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_getLocationComma(self):
#         testInput = '6,3'
#         move = ch.getLocation(currentLocation, testInput)
#         self.assertEqual(move, '6,3')
#
#     # @unittest.skip('I do not feel like running it!')
#     @unittest.skip
#     def test_getLocationLetter(self):
#         testInput = '6a3'
#         move = ch.getLocation(currentLocation, testInput)
#         self.assertEqual(move, False)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntComma(self):
#         moveInt = ch.convertMoveToInt('1,1')
#         self.assertEqual(moveInt, [1, 1])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntSpace(self):
#         moveInt = ch.convertMoveToInt('1 1')
#         self.assertEqual(moveInt, [1, 1])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntPeriod(self):
#         moveInt = ch.convertMoveToInt('1,1')
#         self.assertEqual(moveInt, [1, 1])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntForwardSlash(self):
#         moveInt = ch.convertMoveToInt('1/1')
#         self.assertEqual(moveInt, [1, 1])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntBackSlash(self):
#         moveInt = ch.convertMoveToInt('1\\1')
#         self.assertEqual(moveInt, [1, 1])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntPipe(self):
#         moveInt = ch.convertMoveToInt('1|1')
#         self.assertEqual(moveInt, [1, 1])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntQuestionMark(self):
#         moveInt = ch.convertMoveToInt('1?1')
#         self.assertEqual(moveInt, [1, 1])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntLessThan(self):
#         moveInt = ch.convertMoveToInt('1<1')
#         self.assertEqual(moveInt, [1, 1])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_convertMoveToIntGreaterThan(self):
#         moveInt = ch.convertMoveToInt('1>1')
#         self.assertEqual(moveInt, [1, 1])
#
#     @unittest.skip('No longer use function')
#     def test_checkPieceType(self):
#         selectedPiece = [6, 1]
#         checkedPiece = ch.checkPieceType(selectedPiece)
#         self.assertEqual(checkedPiece, redPiece)
#         return checkedPiece
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_listAvailableMoves(self):
#         selectedPieceType = redPiece
#         availableMoves = ch.listAvailableMoves(selectedPieceType, testSelectedPiece)
#         self.assertEqual(availableMoves, [[5, 0], [5, 2]])
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_checkIfMoveIsValid(self):
#         testAvailableMoves = [[0, 5], [5, 2]]
#         newBoard = CheckerBoard()
#         pieceType = newBoard.pieceType([6, 1])
#         validMoves = ch.checkIfMoveIsValid(testAvailableMoves, pieceType)
#         self.assertEqual(validMoves, [[5, 2]])
#         return validMoves
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_markValidMovesOnBoard(self):
#         newBoard = CheckerBoard()
#         endBoard = CheckerBoard()
#         endBoard.updateBoard([5, 2], pathPiece)
#         ch.markValidMovesOnBoard([[5, 2]], newBoard)
#         markedCells = newBoard.__eq__(endBoard)
#         self.assertEqual(markedCells, True)
#
#     @unittest.skip('I do not feel like running it!')
#     def test_markValidMoveOnBoardCaptureMoves(self):
#         jumpMoves = {1: [[6, 1], [[4, 3]]], 2: [[6, 3], [[4, 1]]], 3: [[6, 5], [[4, 7]]], 4: [[6, 7], [[4, 5]]]}
#         testSelectedPiece = [6, 1]
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 2], whitePiece)
#         startBoard.updateBoard([5, 6], whitePiece)
#         endBoard = CheckerBoard()
#         endBoard.updateBoard([5, 2], whitePiece)
#         endBoard.updateBoard([5, 6], whitePiece)
#         endBoard.updateBoard([4, 3], pathPiece)
#         ch.markValidMoveOnBoardCaptureMoves(jumpMoves, testSelectedPiece, startBoard)
#         # startBoard.printCheckerBoard()
#         # endBoard.printCheckerBoard()
#         matchedBoards = startBoard.__eq__(endBoard)
#         self.assertEqual(matchedBoards, True)
#
#     @unittest.skip('I do not feel like running it!')
#     def test_markValidMoveOnBoardCaptureMovesTwoCapturesForSinglePiece(self):
#         otherJumpMoves = {1: [[6, 3], [[4, 5]]], 2: [[6, 5], [[4, 3], [4, 7]]], 3: [[6, 7], [[4, 5]]]}
#         testSelectedPiece = [6, 5]
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], whitePiece)
#         startBoard.updateBoard([5, 6], whitePiece)
#         endBoard = CheckerBoard()
#         endBoard.updateBoard([5, 4], whitePiece)
#         endBoard.updateBoard([5, 6], whitePiece)
#         endBoard.updateBoard([4, 7], pathPiece)
#         endBoard.updateBoard([4, 3], pathPiece)
#         ch.markValidMoveOnBoardCaptureMoves(otherJumpMoves, testSelectedPiece, startBoard)
#         # startBoard.printCheckerBoard()
#         # endBoard.printCheckerBoard()
#         matchedBoards = startBoard.__eq__(endBoard)
#         self.assertEqual(matchedBoards, True)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_moveSelectionInput(self):
#         testDict = {1: [5, 2], 2: [5, 4]}
#         testValidMoves = [[5, 2], [5, 4]]
#         moveInput = ch.moveSelectionInput(testValidMoves)
#         self.assertEqual(moveInput, testDict)
#
#     # @unittest.skip('Passes but requires input')
#     def test_outputPossibleMoves(self):
#         testDict = {1: [5, 2], 2: [5, 4]}
#         testOutput = 1
#         returnedOutput = ch.outputPossibleMoves(testDict, testOutput)
#         self.assertEqual(returnedOutput, testOutput)
#
#     # @unittest.skip('Passes but requires input')
#     def test_outputPossibleMoves_BlankInput(self):
#         testDict = {1: [5, 2]}
#         testOutput = ''
#         returnedOutput = ch.outputPossibleMoves(testDict, testOutput)
#         self.assertEqual(returnedOutput, 1)
#
#     # @unittest.skip('Passes but requires input')
#     def test_outputPossibleMoves_BlankInputDictLenTwo(self):
#         testDict = {1: [5, 2], 2: [5, 4]}
#         testOutput = ''
#         returnedOutput = ch.outputPossibleMoves(testDict, testOutput)
#         self.assertEqual(returnedOutput, False)
#
#     # @unittest.skip('Passes but requires input')
#     def test_outputPossibleMoves_InvalidStringInput(self):
#         testDict = {1: [5, 2], 2: [5, 4]}
#         testOutput = 'a'
#         returnedOutput = ch.outputPossibleMoves(testDict, testOutput)
#         self.assertEqual(returnedOutput, False)
#
#     # @unittest.skip('Passes but requires input')
#     def test_outputPossibleCaptureMovesDict(self):
#         jumpMoves = {1: [[6, 3], [[4, 5]]], 2: [[6, 5], [[4, 3], [4, 7]]], 3: [[6, 7], [[4, 5]]]}
#         testSelectedPiece = [6, 3]
#         testOutput = [4, 5]
#         returnedOutput = ch.outputPossibleCaptureMoves(jumpMoves, testSelectedPiece, 1)
#         # print('returnedOutput ' + str(returnedOutput))
#         self.assertEqual(returnedOutput, testOutput)
#
#     # @unittest.skip('Passes but requires input')
#     def test_outputPossibleCaptureMoves_DictTwo(self):
#         jumpMoves = {1: [[6, 3], [[4, 5]]], 2: [[6, 5], [[4, 3], [4, 7]]], 3: [[6, 7], [[4, 5]]]}
#         testSelectedPiece = [6, 5]
#         testOutput = 1
#         returnedOutput = ch.outputPossibleCaptureMoves(jumpMoves, testSelectedPiece, testOutput)
#         self.assertEqual(returnedOutput, [4, 3])
#
#     # @unittest.skip('skip')
#     def test_checkIfSelectionIsCaptureMove(self):
#         jumpMoves = {1: [[6, 3], [[4, 5]]], 2: [[6, 5], [[4, 3], [4, 7]]], 3: [[6, 7], [[4, 5]]]}
#         testSelectedPiece = [6, 5]
#         selectionTest = ch.checkIfSelectionIsCaptureMove(jumpMoves, testSelectedPiece)
#         self.assertEqual(selectionTest, True)
#
#     # @unittest.skip('skip')
#     def test_checkIfSelectionIsCaptureMoveTwo(self):
#         jumpMoves = {1: [[6, 3], [[4, 5]]], 2: [[6, 5], [[4, 3], [4, 7]]], 3: [[6, 7], [[4, 5]]]}
#         testSelectedPiece = [6, 1]
#         selectionTest = ch.checkIfSelectionIsCaptureMove(jumpMoves, testSelectedPiece)
#         self.assertEqual(selectionTest, False)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_checkMoveSelection(self):
#         testDict = {1: [5, 2], 2: [5, 4]}
#         testOutput = 3
#         failedOutput = ch.checkMoveSelection(testDict, testOutput)
#         self.assertEqual(failedOutput, False)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_passSelectedMovePiece(self):
#         testDict = {1: [5, 2], 2: [5, 4]}
#         testOutput = 1
#         pickedMove = ch.passSelectedMovePiece(testDict, testOutput)
#         self.assertEqual(pickedMove, [5, 2])
#
#     def test_removePaths(self):
#         testDict = {1: [5, 2], 2: [5, 4]}
#         testCheckerBoard = CheckerBoard()
#         endCheckerBoard = CheckerBoard()
#         # endCheckerBoard.updateBoard([4, 5], pathPiece)
#         ch.removePaths(testCheckerBoard)
#         test = testCheckerBoard.__eq__(endCheckerBoard)
#         self.assertEqual(test, True)
#
#     # @unittest.skip('Screwing up my other test "scanBoard"')
#     def test_moveSelectedPiece(self):
#         selectedPiece = [6, 3]
#         pieceType = redPiece
#         pickedMove = [5, 4]
#         endBoard = CheckerBoard()
#         endBoard.updateBoard([5, 4], redPiece)
#         endBoard.updateBoard([6, 3], emptyCell)
#         moveBoard = CheckerBoard()
#         ch.moveSelectedPiece(selectedPiece, pieceType, pickedMove, moveBoard)
#         test = moveBoard.__eq__(endBoard)
#         self.assertEqual(test, True)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_playerControl(self):
#         playerTurn = ch.playerControl(redPiece)
#         self.assertEqual(playerTurn, True)
#
#     @unittest.skip('I do not feel like running it!')
#     def test_gameType(self):
#         gameType = ch.gameType()
#         self.assertEqual(gameType, 'PvP')
#
#     # @unittest.skip('Possible Easy Mode')
#     def test_scanBoardEasy(self):
#         i = 1
#         returnedArray = {1: [[6, 1], [[5, 2]]], 2: [[6, 3], [[5, 2], [5, 4]]], 3: [[6, 5], [[5, 4], [5, 6]]], 4: [[6, 7], [[5, 6], [5, 8]]]}
#         scannedBoard = ch.scanBoardEasy(i)
#         self.assertEqual(scannedBoard, returnedArray)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_scanBoard(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 2], whitePiece)
#         startBoard.updateBoard([5, 6], whitePiece)
#         # startBoard.printCheckerBoard()
#         i = 0
#         boardScanned = ch.scanBoard(i, startBoard)
#         foundJumps = {1: [[6, 1], [[4, 3]]], 2: [[6, 3], [[4, 1]]], 3: [[6, 5], [[4, 7]]], 4: [[6, 7], [[4, 5]]]}
#         self.assertEqual(boardScanned, foundJumps)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_scanBoard_TwoCaptureMovesForSinglePiece(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 6], whitePiece)
#         startBoard.updateBoard([5, 4], whitePiece)
#         startBoard.updateBoard([6, 7], emptyCell)
#         startBoard.updateBoard([6, 3], emptyCell)
#         i = 0
#         boardScanned = ch.scanBoard(i, startBoard)
#         foundJumps = {1: [[6, 5], [[4, 3], [4, 7]]]}
#         self.assertEqual(boardScanned, foundJumps)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_scanBoard_EndLocationIsSideNumbers(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 6], whitePiece)
#         startBoard.updateBoard([5, 8], whitePiece)
#         startBoard.updateBoard([6, 5], emptyCell)
#         i = 0
#         boardScanned = ch.scanBoard(i, startBoard)
#         foundJumps = {1: [[6, 7], [[4, 5]]]}
#         self.assertEqual(boardScanned, foundJumps)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_scanBoard_NoCaptureMoves(self):
#         startBoard = CheckerBoard()
#         i = 0
#         boardScanned = ch.scanBoard(i, startBoard)
#         foundJumps = {}
#         self.assertEqual(boardScanned, foundJumps)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_scanBoard_ReversedNoCaptureMoves(self):
#         startBoard = CheckerBoard()
#         startBoard.reverseBoardView()
#         startBoard.actualBoardReversal()
#         i = 1
#         boardScanned = ch.scanBoard(i, startBoard)
#         foundJumps = {}
#         self.assertEqual(boardScanned, foundJumps)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_scanBoard_ReversedCaptureMoves(self):
#         startBoard = CheckerBoard()
#         startBoard.reverseBoardView()
#         startBoard.actualBoardReversal()
#         startBoard.updateBoard([5, 2], redPiece)
#         startBoard.updateBoard([5, 6], redPiece)
#         i = 1
#         boardScanned = ch.scanBoard(i, startBoard)
#         foundJumps = {1: [[6, 1], [[4, 3]]], 2: [[6, 3], [[4, 1]]], 3: [[6, 5], [[4, 7]]], 4: [[6, 7], [[4, 5]]]}
#         self.assertEqual(boardScanned, foundJumps)
#
#     def test_checkIfCaptureMove(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], whitePiece)
#         startBoard.updateBoard([5, 2], whitePiece)
#         testSelectedPiece = [6, 3]
#         availableMoves = ch.listAvailableMoves(redPiece, testSelectedPiece)
#         jumpPiece = ch.checkIfCaptureMove(redPiece, availableMoves, startBoard)
#         self.assertEqual(jumpPiece, [[5, 2], [5, 4]])
#
#     def test_calculateCaptureMove(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], whitePiece)
#         testSelectedPiece = [6, 3]
#         jumpPiece = [[5, 4]]
#         endLocation = ch.calculateCaptureMove(testSelectedPiece, jumpPiece)
#         self.assertEqual(endLocation, [[4, 5]])
#
#     def test_calculateRemovePiece(self):
#         testSelectedPiece = [6, 3]
#         selectedJump = [4, 5]
#         testRemovePiece = [5, 4]
#         removePiece = ch.calculateRemovePiece(testSelectedPiece, selectedJump)
#         self.assertEqual(removePiece, testRemovePiece)
#
#     # @unittest.skip('I do not feel like running it!')
#     def test_jumpPiece(self):
#         endBoard = CheckerBoard()
#         endBoard.updateBoard([4, 5], redPiece)
#         endBoard.updateBoard([6, 3], emptyCell)
#         jumpBoard = CheckerBoard()
#         jumpBoard.updateBoard([5, 4], whitePiece)
#         selectedPiece = [6, 3]
#         jumpPiece = [4, 5]
#         ch.jumpPiece(selectedPiece, jumpPiece, redPiece, jumpBoard)
#         test = jumpBoard.__eq__(endBoard)
#         self.assertEqual(test, True)
#
#     def test_endLocationCheck(self):
#         endLocation = [[5, 0]]
#         testBoard = CheckerBoard()
#         test = ch.endLocationCheck(endLocation, testBoard)
#         self.assertEqual(test, [])
#
#     @unittest.skip('Not sure how to test')
#     def test_pressAnyKeyToContinue_Enter(self):
#         key = ''
#         anyKey = ch.pressAnyKey(key)
#         self.assertEqual(anyKey, 63)
#
#     @unittest.skip('Not sure how to test')
#     def test_pressAnyKeyToContinue_A(self):
#         key = 'a'
#         anyKey = ch.pressAnyKey(key)
#         self.assertEqual(anyKey, 'a')
#
#     @unittest.skip('Not sure how to test')
#     def test_pressAnyKeyToContinue_BackSlash(self):
#         key = '\\'
#         anyKey = ch.pressAnyKey(key)
#         self.assertEqual(anyKey, '\\')
#
#     # @unittest.skip('Not sure how to test')
#     def test_WinGame(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([2, 1], emptyCell)
#         startBoard.updateBoard([1, 2], emptyCell)
#         startBoard.updateBoard([3, 2], emptyCell)
#         startBoard.updateBoard([2, 3], emptyCell)
#         startBoard.updateBoard([1, 4], emptyCell)
#         startBoard.updateBoard([3, 4], emptyCell)
#         startBoard.updateBoard([2, 5], emptyCell)
#         startBoard.updateBoard([1, 6], emptyCell)
#         startBoard.updateBoard([3, 6], emptyCell)
#         startBoard.updateBoard([2, 7], emptyCell)
#         startBoard.updateBoard([1, 8], emptyCell)
#         startBoard.updateBoard([3, 8], emptyCell)
#         wonGame = ch.checkIfGameOver(0, startBoard)
#         self.assertEqual(wonGame, True)
#
#     # @unittest.skip('Not sure how to test')
#     def test_WinGame(self):
#         startBoard = CheckerBoard()
#         startBoard.reverseBoardView()
#         startBoard.updateBoard([1, 1], emptyCell)
#         startBoard.updateBoard([1, 3], emptyCell)
#         startBoard.updateBoard([2, 2], emptyCell)
#         startBoard.updateBoard([3, 3], emptyCell)
#         startBoard.updateBoard([3, 1], emptyCell)
#         startBoard.updateBoard([2, 4], emptyCell)
#         startBoard.updateBoard([1, 5], emptyCell)
#         startBoard.updateBoard([3, 5], emptyCell)
#         startBoard.updateBoard([2, 6], emptyCell)
#         startBoard.updateBoard([1, 7], emptyCell)
#         startBoard.updateBoard([3, 7], emptyCell)
#         startBoard.updateBoard([2, 8], emptyCell)
#         wonGame = ch.checkIfGameOver(1, startBoard)
#         self.assertEqual(wonGame, True)
#
#     def test_WinGame_ReturnsFalse(self):
#         startBoard = CheckerBoard()
#         game = ch.checkIfGameOver(0, startBoard)
#         self.assertEqual(game, False)
#
#     def test_WinGame_ReturnsFalsePlayer2Turn(self):
#         startBoard = CheckerBoard()
#         game = ch.checkIfGameOver(1, startBoard)
#         self.assertEqual(game, False)
#
#     # @unittest.skip('Not sure how to test')
#     def test_checkForLegalMoves_NoLegalMoves(self):
#         i = 1
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([2, 1], emptyCell)
#         startBoard.updateBoard([1, 2], emptyCell)
#         startBoard.updateBoard([3, 2], emptyCell)
#         startBoard.updateBoard([2, 3], emptyCell)
#         startBoard.updateBoard([1, 4], emptyCell)
#         startBoard.updateBoard([3, 4], emptyCell)
#         startBoard.updateBoard([2, 5], emptyCell)
#         startBoard.updateBoard([1, 6], emptyCell)
#         startBoard.updateBoard([3, 6], emptyCell)
#         startBoard.updateBoard([2, 7], emptyCell)
#         startBoard.updateBoard([1, 8], emptyCell)
#         startBoard.updateBoard([3, 8], emptyCell)
#         startBoard.reverseBoardView()
#         startBoard.updateBoard([4, 4], whitePiece)
#         # startBoard.printCheckerBoard()
#         legalMoves = ch.checkForLegalMoves(i, startBoard)
#         self.assertEqual(legalMoves, False)
#
#     def test_checkForLegalMoves_HasLegalMoves(self):
#         i = 1
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([2, 1], emptyCell)
#         startBoard.updateBoard([1, 2], emptyCell)
#         startBoard.updateBoard([3, 2], emptyCell)
#         startBoard.updateBoard([2, 3], emptyCell)
#         startBoard.updateBoard([1, 4], emptyCell)
#         startBoard.updateBoard([3, 4], emptyCell)
#         startBoard.updateBoard([2, 5], emptyCell)
#         startBoard.updateBoard([1, 6], emptyCell)
#         startBoard.updateBoard([3, 6], emptyCell)
#         startBoard.updateBoard([2, 7], emptyCell)
#         startBoard.updateBoard([1, 8], emptyCell)
#         startBoard.updateBoard([3, 8], emptyCell)
#         startBoard.reverseBoardView()
#         startBoard.updateBoard([4, 4], whitePiece)
#         startBoard.updateBoard([6, 4], whitePiece)
#         # startBoard.printCheckerBoard()
#         legalMoves = ch.checkForLegalMoves(i, startBoard)
#         self.assertEqual(legalMoves, True)
#
#     # @unittest.skip('Not sure how to test')
#     def test_checkForLegalMoves_FreshBoard(self):
#         i = 0
#         startBoard = CheckerBoard()
#         legalMoves = ch.checkForLegalMoves(i, startBoard)
#         self.assertEqual(legalMoves, True)
#
#     def test_checkForLegalMoves_KingPiece(self):
#         i = 1
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([2, 1], emptyCell)
#         startBoard.updateBoard([1, 2], emptyCell)
#         startBoard.updateBoard([3, 2], emptyCell)
#         startBoard.updateBoard([2, 3], emptyCell)
#         startBoard.updateBoard([1, 4], emptyCell)
#         startBoard.updateBoard([3, 4], emptyCell)
#         startBoard.updateBoard([2, 5], emptyCell)
#         startBoard.updateBoard([1, 6], emptyCell)
#         startBoard.updateBoard([3, 6], emptyCell)
#         startBoard.updateBoard([2, 7], emptyCell)
#         startBoard.updateBoard([1, 8], emptyCell)
#         startBoard.updateBoard([3, 8], emptyCell)
#         startBoard.reverseBoardView()
#         startBoard.updateBoard([4, 4], kingWhitePiece)
#         startBoard.updateBoard([5, 3], redPiece)
#         startBoard.updateBoard([5, 5], redPiece)
#         startBoard.updateBoard([6, 2], redPiece)
#         startBoard.updateBoard([6, 6], redPiece)
#         # startBoard.printCheckerBoard()
#         legalMoves = ch.checkForLegalMoves(i, startBoard)
#         self.assertEqual(legalMoves, False)
#
#     def test_getPlayerNumber(self):
#         i = 0
#         player = ch.getPlayerNumber(i)
#         self.assertEqual(player, '1')
#
#     def test_getPlayerNumber(self):
#         i = 1
#         player = ch.getPlayerNumber(i)
#         self.assertEqual(player, '2')
#
#     # Chain Jump Test
#
#     # Possibly check for jump moves only and not chains
#     # then if a chain jump is possible (via another scan)
#     # list indicate that as an option as well
#
#     def test_miniScan(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([4, 3], redPiece)
#         startBoard.updateBoard([2, 1], emptyCell)
#         jumpPiece = [4, 3]
#         test = ch.chainJumpScan(jumpPiece, redPiece, startBoard)
#         self.assertEqual(test, {1: [[4, 3], [[2, 1]]]})
#
#     def test_miniScanTwoEndLocations(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([4, 3], redPiece)
#         startBoard.updateBoard([2, 1], emptyCell)
#         startBoard.updateBoard([2, 5], emptyCell)
#         jumpPiece = [4, 3]
#         test = ch.chainJumpScan(jumpPiece, redPiece, startBoard)
#         self.assertEqual(test, {1: [[4, 3], [[2, 1], [2, 5]]]})
#
#     def test_miniScanNoJumps(self):
#         startBoard = CheckerBoard()
#         jumpPiece = [4, 3]
#         test = ch.chainJumpScan(jumpPiece, redPiece, startBoard)
#         self.assertEqual(test, {})
#
#     @unittest.skip('Another possible easy function')
#     def test_chainJumpEasy(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], whitePiece)
#         # startBoard.updateBoard([6, 3], emptyCell)
#         startBoard.updateBoard([2, 1], emptyCell)
#         # startBoard.printCheckerBoard()
#         endBoard = CheckerBoard()
#         endBoard.updateBoard([2, 1], redPiece)
#         endBoard.updateBoard([6, 3], emptyCell)
#         endBoard.updateBoard([6, 5], emptyCell)
#         endBoard.updateBoard([5, 4], emptyCell)
#         endBoard.updateBoard([3, 2], emptyCell)
#         # endBoard.printCheckerBoard()
#         test = ch.scanBoard(1, startBoard)
#         self.assertEqual(test, {1: [[6, 5], ([4, 3], [2, 1])]})
#
#     # @unittest.skip(' ')
#     def test_chainJump(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([4, 3], redPiece)
#         startBoard.updateBoard([2, 1], emptyCell)
#         test = ch.scanBoard(0, startBoard)
#         self.assertEqual(test, {1: [[4, 3], [[2, 1]]]})
#
#     # @unittest.skip(' ')
#     def test_markValidMovesOnBoardChainJump(self):
#         jumps = {1: [[6, 5], ([4, 3], [2, 1])]}
#         testSelectedPiece = [6, 5]
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], whitePiece)
#         startBoard.updateBoard([2, 1], emptyCell)
#         endBoard = CheckerBoard()
#         endBoard.updateBoard([2, 1], pathPiece)
#         # endBoard.updateBoard([6, 5], emptyCell)
#         endBoard.updateBoard([5, 4], whitePiece)
#         endBoard.updateBoard([3, 2], whitePiece)
#         endBoard.updateBoard([4, 3], pathPiece)
#         ch.markValidMoveOnBoardCaptureMoves(jumps, testSelectedPiece, startBoard)
#         # startBoard.printCheckerBoard()
#         # endBoard.printCheckerBoard()
#         test = startBoard.__eq__(endBoard)
#         self.assertEqual(test, True)
#
#     # --------- King Piece Test ---------
#     # @unittest.skip(' ')
#     def test_kingPiece(self):
#         i = 0
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([1, 4], redPiece)
#         endBoard = CheckerBoard()
#         endBoard.updateBoard([1, 4], kingRedPiece)
#         startBoard = ch.checkKingsRow(i, startBoard)
#         # startBoard.printCheckerBoard()
#         # endBoard.printCheckerBoard()
#         test = startBoard.__eq__(endBoard)
#         self.assertEqual(test, True)
#
#     # @unittest.skip(' ')
#     def test_calculateKingMoves_NoJump(self):
#         test_SelectedPiece = [5, 4]
#         returnedKingMoves = ch.calculateKingMoves(test_SelectedPiece)
#         returnedArray = [[4, 3], [4, 5], [6, 3], [6, 5]]
#         self.assertEqual(returnedKingMoves, returnedArray)
#
#     # @unittest.skip(' ')
#     def test_listKingMoves_NoJump(self):
#         test_SelectedPiece = [5, 4]
#         pieceType = kingRedPiece
#         returnedKingMoves = ch.listAvailableMoves(pieceType, test_SelectedPiece)
#         returnedArray = [[4, 3], [4, 5], [6, 3], [6, 5]]
#         self.assertEqual(returnedKingMoves, returnedArray)
#
#     # @unittest.skip(' ')
#     def test_checkIfKingMovesAreValid_NoJump(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], kingRedPiece)
#         startBoard.updateBoard([6, 3], emptyCell)
#         # startBoard.updateBoard([6, 5], emptyCell)
#         test_SelectedPiece = [5, 4]
#         returnedKingMoves = ch.calculateKingMoves(test_SelectedPiece)
#         legalKingMoves = ch.checkIfMoveIsValidKing(returnedKingMoves, kingWhitePiece, startBoard)
#         self.assertEqual(legalKingMoves, [[4, 3], [4, 5], [6, 3]])
#
#     # @unittest.skip(' ')
#     def test_KingMovesCreateMoveDict(self):
#         returnedDict = {1: [4, 3], 2: [4, 5], 3: [6, 3]}
#         returnedArray = [[4, 3], [4, 5], [6, 3]]
#         kingMovesDict = ch.moveSelectionInput(returnedArray)
#         self.assertEqual(kingMovesDict, returnedDict)
#
#     # @unittest.skip(' ')
#     def test_KingMoveSelection(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], kingRedPiece)
#         kingSelected = ch.playerControl(kingRedPiece)
#         self.assertEqual(kingSelected, True)
#
#     # @unittest.skip(' ')
#     def test_KingOutputPossibleMoves(self):
#         kingDict = {1: [4, 3], 2: [4, 5], 3: [6, 3]}
#         testSelection = 2
#         returnedSelection = ch.outputPossibleMoves(kingDict, testSelection)
#         self.assertEqual(returnedSelection, testSelection)
#
#     # @unittest.skip(' ')
#     def test_KingOutputPossibleMoves_SingleMove(self):
#         kingDict = {1: [4, 3]}
#         testSelection = ''
#         returnedSelection = ch.outputPossibleMoves(kingDict, testSelection)
#         self.assertEqual(returnedSelection, 1)
#
#     # @unittest.skip(' ')
#     def test_KingScanBoard(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], kingRedPiece)
#         startBoard.updateBoard([4, 3], whitePiece)
#         startBoard.updateBoard([3, 2], emptyCell)
#         startBoard.updateBoard([5, 6], whitePiece)
#         i = 0
#         scannedBoard = ch.scanBoard(i, startBoard)
#         returnedDict = {1: [[5, 4], [[3, 2]]], 2: [[6, 5], [[4, 7]]], 3: [[6, 7], [[4, 5]]]}
#         self.assertEqual(scannedBoard, returnedDict)
#
#     # @unittest.skip(' ')
#     def test_KingScanBoard_TwoEndPoints(self):
#         startBoard = CheckerBoard()
#         startBoard.updateBoard([5, 4], kingRedPiece)
#         startBoard.updateBoard([4, 3], whitePiece)
#         startBoard.updateBoard([4, 5], whitePiece)
#         # startBoard.updateBoard([5, 6], whitePiece)
#         startBoard.updateBoard([3, 2], emptyCell)
#         startBoard.updateBoard([3, 6], emptyCell)
#         i = 0
#         scannedBoard = ch.scanBoard(i, startBoard)
#         # startBoard.printCheckerBoard()
#         returnedDict = {1: [[5, 4], [[3, 2], [3, 6]]]}
#         self.assertEqual(scannedBoard, returnedDict)
#
#     # Spare Test?
#     @unittest.skip(' not currently using')
#     def test_outputPossibleMovesChainJump(self):
#         jumpMoves = {1: [[6, 5], ([4, 3], [2, 1])], 2: [[6, 5], [[4, 3]]]}
#         testSelectedPiece = [6, 5]
#         testOutput = [[4, 3], [2, 1]]
#         returnedOutput = ch.outputPossibleCaptureMoves(jumpMoves, testSelectedPiece, 1)
#         # print('returnedOutput ' + str(returnedOutput))
#         self.assertEqual(returnedOutput, testOutput)
#
#     def test_removeOuterBracket(self):
#         testArray = [[4, 5]]
#         formattedArray = ch.removeOuterBracket(testArray)
#         self.assertEqual(formattedArray, [4, 5])
#
#     @unittest.skip('Passes but requires input not using right now')
#     def test_outputSelectionCaptureMoves(self):
#         scannedBoard = {1: [[6, 3], [[4, 5]]], 2: [[6, 5], [[4, 3], [4, 7]]], 3: [[6, 7], [[4, 5]]]}
#         outputSelectionDict = ch.outputSelectionPiece(scannedBoard)
#         expected = 1
#         self.assertEqual(outputSelectionDict, expected)


if __name__ == '__main__':
    unittest.main()
