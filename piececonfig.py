from PieceColor import PieceColor


def getOpposite(piece: PieceColor):
    if piece == PieceConfig.Black:
        return PieceConfig.White
    elif piece == PieceConfig.White:
        return PieceConfig.Black
    return PieceConfig.NoPiece


class PieceConfig(object):
    NoPiece = PieceColor(None)
    White = PieceColor("#FFFFFF")
    Black = PieceColor("#000000")
