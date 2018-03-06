from colorama import init, Fore, Back, Style

init(autoreset=True, convert=True)

START = '\033[4m'
END = '\033[0m'
emptyCell = (Back.BLACK + '   ' + Fore.RESET)
pinkCell = (Style.BRIGHT + Back.RED + '   ' + Fore.RESET)
whitePiece = (Back.BLACK + Fore.WHITE + START + ' O ' + END + Fore.RESET)
redPiece = (Back.BLACK + Style.BRIGHT + Fore.MAGENTA + START + ' X ' + END + Fore.RESET)
pathPiece = (Back.BLACK + Style.BRIGHT + Fore.GREEN + START + ' * ' + END + Fore.RESET)
kingWhitePiece = (Back.BLACK + Fore.WHITE + START + '(O)' + END + Fore.RESET)
kingRedPiece = (Back.BLACK + Style.BRIGHT + Fore.MAGENTA + START + '<X>' + END + Fore.RESET)

number = 1
blankSpace = ' '

numbersRow = [blankSpace, '1', '2', '3', '4', '5', '6', '7', '8', blankSpace]


class CheckerBoard(object):
    def __init__(self):
        self.board = [[blankSpace, ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', blankSpace],
                      [number, pinkCell, whitePiece, pinkCell, whitePiece, pinkCell, whitePiece, pinkCell, whitePiece,
                       number],
                      [number, whitePiece, pinkCell, whitePiece, pinkCell, whitePiece, pinkCell, whitePiece, pinkCell,
                       number],
                      [number, pinkCell, whitePiece, pinkCell, whitePiece, pinkCell, whitePiece, pinkCell, whitePiece,
                       number],
                      [number, emptyCell, pinkCell, emptyCell, pinkCell, emptyCell, pinkCell, emptyCell, pinkCell,
                       number],
                      [number, pinkCell, emptyCell, pinkCell, emptyCell, pinkCell, emptyCell, pinkCell, emptyCell,
                       number],
                      [number, redPiece, pinkCell, redPiece, pinkCell, redPiece, pinkCell, redPiece, pinkCell, number],
                      [number, pinkCell, redPiece, pinkCell, redPiece, pinkCell, redPiece, pinkCell, redPiece, number],
                      [number, redPiece, pinkCell, redPiece, pinkCell, redPiece, pinkCell, redPiece, pinkCell, number],
                      [blankSpace, ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', blankSpace]]

    def __iter__(self):
        return self.board

    def __eq__(self, other):
        if self.board == other.board:
            return True
        return False

    @staticmethod
    def resetBoard():
        return CheckerBoard()

    def printCheckerBoard(self):
        row = 1
        column = 0
        endRow = 1
        endColumn = 9
        for i in self.board:
            print(''.join(str(a) for a in i))
            if row < 9 and endRow < 9:
                self.board[row][column] = numbersRow[row]
                self.board[endRow][endColumn] = numbersRow[row]
            row += 1
            endRow += 1

    def reverseBoardView(self):
        return self.board.reverse()

    def actualBoardReversal(self):
        reverseBoard = list(self.board)
        for i in reverseBoard:
            if i != self.board[0] or i != self.board[9]:
                i.reverse()
        return reverseBoard

    def updateBoard(self, coord, pieceType):
        self.board[coord[0]][coord[1]] = pieceType
        return self.board

    def pieceType(self, coord):
        boardCoord = self.board[coord[0]][coord[1]]
        if boardCoord == emptyCell:
            return emptyCell
        elif boardCoord == redPiece:
            return redPiece
        elif boardCoord == whitePiece:
            return whitePiece
        elif boardCoord == kingRedPiece:
            return kingRedPiece
        elif boardCoord == kingWhitePiece:
            return kingWhitePiece
        else:
            return False
