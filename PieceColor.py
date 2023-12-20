class PieceColor:

    def __init__(self, color):
        self.color = color

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __hash__(self):
        return hash(self.color)
