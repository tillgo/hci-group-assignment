from PieceColor import PieceColor
from piececonfig import PieceConfig


class Field:
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def isFieldSurroundedByEnemy(self, boardArray: list[list[PieceColor]], color: PieceColor) -> bool:
        """
        Check, if given fields liberties are all occupied by given color
        parameters:
            - boardArray: 2D array representing the Go board
            - color: enemy color

        returns: boolean
            - True if field is surrounded by enemy color
            - False if field is not surrounded by enemy color
        """
        # Check if field above field to check is border or enemy color
        return ((self.row - 1 < 0 or boardArray[self.row - 1][self.col] == color)
                # Check if field to the right of field to check is border or enemy color
                and (self.col + 1 >= len(boardArray[0]) or boardArray[self.row][self.col + 1] == color)
                # Check if field below field to check is border or enemy color
                and (self.row + 1 >= len(boardArray) or boardArray[self.row + 1][self.col] == color)
                # Check if field to the right of field to check is border or enemy color
                and (self.col - 1 < 0 or boardArray[self.row][self.col - 1] == color))
