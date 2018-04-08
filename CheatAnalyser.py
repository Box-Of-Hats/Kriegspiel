from ChessPiece import *


class CheatAnalyser():
    def __init__(self):
        self.piece_values = {
            Pawn: 1,
            King: 10000,
            Queen: 20,
            Rook: 8,
            Knight: 10,
            Bishop: 8,
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
