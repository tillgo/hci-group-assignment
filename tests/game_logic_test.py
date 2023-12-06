import unittest

from rules import Rules
from piececonfig import PieceConfig


class MyTestCase(unittest.TestCase):
    def test_try_capture(self):
        test_board = [
            [PieceConfig.NoPiece, PieceConfig.NoPiece, PieceConfig.NoPiece, PieceConfig.NoPiece],
            [PieceConfig.NoPiece, PieceConfig.White, PieceConfig.NoPiece, PieceConfig.NoPiece],
            [PieceConfig.White, PieceConfig.Black, PieceConfig.White, PieceConfig.NoPiece],
            [PieceConfig.NoPiece, PieceConfig.White, PieceConfig.NoPiece, PieceConfig.NoPiece]
        ]
        Rules.try_captures(test_board, PieceConfig.White)

        result = [
            [PieceConfig.NoPiece, PieceConfig.NoPiece, PieceConfig.NoPiece, PieceConfig.NoPiece],
            [PieceConfig.NoPiece, PieceConfig.White, PieceConfig.NoPiece, PieceConfig.NoPiece],
            [PieceConfig.White, PieceConfig.NoPiece, PieceConfig.White, PieceConfig.NoPiece],
            [PieceConfig.NoPiece, PieceConfig.White, PieceConfig.NoPiece, PieceConfig.NoPiece]
        ]
        self.assertEqual(test_board, result)

        test_board2 = [
            [PieceConfig.Black, PieceConfig.NoPiece, PieceConfig.White, PieceConfig.NoPiece],
            [PieceConfig.NoPiece, PieceConfig.White, PieceConfig.Black, PieceConfig.White],
            [PieceConfig.White, PieceConfig.Black, PieceConfig.Black, PieceConfig.White],
            [PieceConfig.NoPiece, PieceConfig.White, PieceConfig.White, PieceConfig.NoPiece]
        ]
        Rules.try_captures(test_board2, PieceConfig.White)

        result = [
            [PieceConfig.Black, PieceConfig.NoPiece, PieceConfig.White, PieceConfig.NoPiece],
            [PieceConfig.NoPiece, PieceConfig.White, PieceConfig.NoPiece, PieceConfig.White],
            [PieceConfig.White, PieceConfig.NoPiece, PieceConfig.NoPiece, PieceConfig.White],
            [PieceConfig.NoPiece, PieceConfig.White, PieceConfig.White, PieceConfig.NoPiece]
        ]
        self.assertEqual(test_board2, result)

        test_board3 = [
            [PieceConfig.Black, PieceConfig.NoPiece, PieceConfig.Black, PieceConfig.NoPiece],
            [PieceConfig.NoPiece, PieceConfig.Black, PieceConfig.White, PieceConfig.White],
            [PieceConfig.Black, PieceConfig.White, PieceConfig.White, PieceConfig.Black],
            [PieceConfig.NoPiece, PieceConfig.Black, PieceConfig.Black, PieceConfig.NoPiece]
        ]
        Rules.try_captures(test_board3, PieceConfig.Black)

        result = [
            [PieceConfig.Black, PieceConfig.NoPiece, PieceConfig.Black, PieceConfig.NoPiece],
            [PieceConfig.NoPiece, PieceConfig.Black, PieceConfig.White, PieceConfig.White],
            [PieceConfig.Black, PieceConfig.White, PieceConfig.White, PieceConfig.Black],
            [PieceConfig.NoPiece, PieceConfig.Black, PieceConfig.Black, PieceConfig.NoPiece]
        ]
        self.assertEqual(test_board3, result)


if __name__ == '__main__':
    unittest.main()
