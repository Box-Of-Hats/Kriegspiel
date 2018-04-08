from ChessPiece import *


class CheatAnalyser():
    def __init__(self):
        self.piece_values = {
            Pawn: 1,
            King: 10000,
            Queen: 9,
            Rook: 5,
            Knight: 3,
            Bishop: 3,
        }

    def get_score_for_board(self, board, player_id):
        """
        Get the score of a given board state.
        Simply sums the scores of all pieces on the board.
        """
        score = 0
        for row in board:
            for piece in row:
                if isinstance(piece, ChessPiece):
                    if piece.owner_id == player_id:
                        score += self.piece_values[type(piece)]
                    else:
                        score -= self.piece_values[type(piece)]

        return score
