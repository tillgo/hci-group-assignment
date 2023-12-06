from piece import Piece


def getOpposite(piece: Piece):
    if piece == PieceConfig.Black:
        return PieceConfig.White
    elif piece == PieceConfig.White:
        return PieceConfig.Black
    return PieceConfig.NoPiece


class PieceConfig(object):
    NoPiece = Piece(None)
    White = Piece("#FFFFFF")
    Black = Piece("#000000")
