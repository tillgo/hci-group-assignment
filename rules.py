from PieceColor import PieceColor
from piececonfig import PieceConfig


class Rules:

    @staticmethod
    def checkLegalMove(boardArray, fieldToBePlaced):
        # ToDo check if Move was a suicide
        return Rules.checkFieldUnoccupied(boardArray, fieldToBePlaced)

    @staticmethod
    def checkFieldUnoccupied(boardArray, fieldToBePlaced):
        return boardArray[fieldToBePlaced.row][fieldToBePlaced.col] is PieceConfig.NoPiece

    @staticmethod
    def try_captures(boardArray: list[list[PieceColor]], placed: PieceColor) -> int:
        capturedCount = 0
        for rIdx, row in enumerate(boardArray):
            for cIdx, piece in enumerate(row):
                if piece == placed or piece == PieceConfig.NoPiece:  # skip if empty or same color
                    continue

                # check the liberties and keep track of the connected stones
                visited = set()
                hasLiberties = Rules.find_liberties(boardArray, rIdx, cIdx, piece, visited)

                if not hasLiberties:
                    for r, c in visited:
                        capturedCount += 1
                        boardArray[r][c] = PieceConfig.NoPiece
        return capturedCount

    @staticmethod
    def find_liberties(boardArray: list[list[PieceColor]], row, col, piece: PieceColor, visited):
        """
        Recursively find liberties for a group of stones with the specified color.

        Parameters:
        - boardArray: 2D array representing the Go board
        - row: Row index of the stone
        - col: Column index of the stone
        - color: Color of the stone
        - visited: Set to keep track of visited positions

        Returns:
        - Set of liberties for the group of stones
        """
        # Check if the position is on the board and has the same color
        if not (0 <= row < len(boardArray) and 0 <= col < len(boardArray[0])) or boardArray[row][col] != piece:
            return False

        # Check if the position has already been visited
        if (row, col) in visited:
            return False

        visited.add((row, col))  # Mark the position as visited

        liberties = False
        # Check liberties in adjacent positions
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row = row + dr if 0 <= row + dr < len(boardArray) else row
            next_col = col + dc if 0 <= col + dc < len(boardArray[0]) else col

            # liberties to True if any surrounding piece is empty or recursively check neighbour pieces
            liberties = (liberties or boardArray[next_row][next_col] == PieceConfig.NoPiece
                         or Rules.find_liberties(boardArray, next_row, next_col, piece, visited))

        return liberties

    @staticmethod
    def calculate_territories(boardArray: list[list[PieceColor]]) -> list[int, int]:
        checked = set()
        territories = [0, 0]
        for rIdx, row in enumerate(boardArray):
            for cIdx, piece in enumerate(row):
                if piece != PieceConfig.NoPiece or (rIdx, cIdx) in checked:  # skip if not empty or same color
                    continue

                # check the liberties and keep track of the connected stones
                visited = set()
                borders = {
                    PieceConfig.White: set(),
                    PieceConfig.Black: set()
                }
                Rules.find_territories(boardArray, rIdx, cIdx, visited, borders)

                for v in visited:
                    checked.add(v)

                if len(borders[PieceConfig.White]) > len(borders[PieceConfig.Black]):
                    territories[0] += len(visited)
                elif len(borders[PieceConfig.White]) < len(borders[PieceConfig.Black]):
                    territories[1] += len(visited)

        return territories

    @staticmethod
    def find_territories(boardArray: list[list[PieceColor]], row, col, visited, borders):
        # Check if the position is on the board and has the same color
        if not (0 <= row < len(boardArray) and 0 <= col < len(boardArray[0])):
            return

        piece = boardArray[row][col]
        if piece != PieceConfig.NoPiece:
            borders[piece].add((row, col))
            return

        # Check if the position has already been visited
        if (row, col) in visited:
            return

        visited.add((row, col))  # Mark the position as visited

        # Check liberties in adjacent positions
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row = row + dr
            next_col = col + dc

            Rules.find_territories(boardArray, next_row, next_col, visited, borders)

