from PieceColor import PieceColor


class GameState:
    """
    Class containing information about specific game (board) state
    """
    def __init__(self, player: PieceColor, boardArray: list[list[PieceColor]], prisoners: dict[PieceColor, int], isPass: bool,
                 startTimes: dict[PieceColor, int]):
        """
        Initialize GameState

        parameters:
            - player: Player who is responsible for the current board state
            - boardArray: Current board state
            - prisoners: current state of prisoners
            - isPass: Was the move a pass?
        """
        self.player = player
        self.boardArray = boardArray
        self.prisoners = prisoners
        self.isPass = isPass
        self.startTimes = startTimes
