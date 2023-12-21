import copy

from PieceColor import PieceColor
from field import Field
from game_state import GameState
from piececonfig import getOpposite, PieceConfig


class Rules:

    @staticmethod
    def checkLegalMove(gameHistory: list[GameState], boardArray: list[list[PieceColor]], fieldToBePlaced: Field,
                       colorToBePlaced: PieceColor) -> bool:
        # ToDo check if Move was move
        return (Rules.checkFieldUnoccupied(boardArray, fieldToBePlaced)
                and not Rules.checkSuicideMove(boardArray, fieldToBePlaced, colorToBePlaced)
                and Rules.checkKoRule(gameHistory, fieldToBePlaced, colorToBePlaced))

    @staticmethod
    def checkFieldUnoccupied(boardArray: list[list[PieceColor]], fieldToBePlaced: Field) -> bool:
        return boardArray[fieldToBePlaced.row][fieldToBePlaced.col] is PieceConfig.NoPiece

    @staticmethod
    def checkSuicideMove(boardArray: list[list[PieceColor]], fieldToBePlaced: Field,
                         colorToBePlaced: PieceColor) -> bool:
        """
        check, if move would be a suicide move

        parameters:
            - boardArray: 2D array representing the Go Board
            - fieldToBePlaced: field on which a stone should be placed
            - colorToBePlaced: Color which is tried to be placed

        returns:
            - boolean: - True if Suicide Move
                       - False if no Suicide Move
        """
        boardCopy = copy.deepcopy(boardArray)
        boardCopy[fieldToBePlaced.row][fieldToBePlaced.col] = colorToBePlaced

        isCaptureMade = Rules.try_captures(boardCopy, colorToBePlaced) > 0
        isFiledSourroundedByEnemy = fieldToBePlaced.isFieldSurroundedByEnemy(boardArray, getOpposite(colorToBePlaced))

        return isFiledSourroundedByEnemy and not isCaptureMade

    @staticmethod
    def checkKoRule(gameHistory: list[GameState], fieldToBePlaced: Field, colorToBePlaced: PieceColor) -> bool:
        """
        Checks if Ko-Rule is satisfied
        parameters:
            - gameHistory: list with all previous game states of the Go Board
            - fieldToBePlaced: field on which a stone should be placed
            - colorToBePlaced: Color which is tried to be placed
        """
        if len(gameHistory) < 2:
            return True

        currentBoardState = gameHistory[-1].boardArray
        nextBoardState = copy.deepcopy(currentBoardState)
        nextBoardState[fieldToBePlaced.row][fieldToBePlaced.col] = colorToBePlaced
        Rules.try_captures(nextBoardState, colorToBePlaced)

        return nextBoardState != gameHistory[-2].boardArray

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
    def calculate_stone_score(boardArray) -> dict[PieceColor, int]:
        scores = {
            PieceConfig.Black: 0,
            PieceConfig.White: 0,
        }
        for row in boardArray:
            for piece in row:
                scores[piece] += 1

        return scores
