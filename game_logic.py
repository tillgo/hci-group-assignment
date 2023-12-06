from piececonfig import PieceConfig


class GameLogic:
    print("Game Logic Object Created")

    # TODO add code here to manage the logic of your game

    @staticmethod
    def checkLegalMove(boardArray, fieldToBePlaced):
        # ToDo check if Move was a suicide
        return GameLogic.checkFieldUnoccupied(boardArray, fieldToBePlaced)

    @staticmethod
    def checkFieldUnoccupied(boardArray, fieldToBePlaced):
        return boardArray[fieldToBePlaced.y][fieldToBePlaced.x] is PieceConfig.NoPiece
