"""
Chess piece values from: 
"Chess Fundamentals: Completely Revised and Updated for the 21st Century"
    https://books.google.co.uk/books/about/Chess_Fundamentals.html?id=rDz8do_EDjkC
"""

from ChessPiece import *
from RefereeOutput import *


"""
Container for referee output objects, with additional arguments.
"""
class SavedOutput():
    def __init__(self, from_cell, to_cell, output=None, moves_made=None):
        self.output = output
        self.moves_made = moves_made
        self.from_cell = from_cell
        self.to_cell = to_cell
        


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
        #A log of all referee outputs, in chronological order
        self.ref_outputs = []

    def get_score_for_board(self, board, player_id):
        """
        Basic utility function.
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

    #def add_ref_output(self, output, moves_made, from_cell, to_cell):
    #    self.ref_outputs.append(SavedOutput(output, moves_made, from_cell, to_cell))
    def add_ref_output(self, output, moves_made):
        """
        Update the latest referee output object in the log with the number of moves made and the output
        given by the referee.
        """
        try:
            if not self.ref_outputs[-1].output:
                self.ref_outputs[-1].output = output
                self.ref_outputs[-1].moves_made = moves_made
            else:
                #raise Exception("Big issue with ref output :/")
                self.create_next_ref_output()
                self.add_ref_output(output, moves_made)
        except IndexError:
            #Triggers if the ref_outputs list is empty.
            #Fix by creating a ref output object before adding to it.
            self.create_next_ref_output()
            self.add_ref_output(output, moves_made)

        
        #print("Latest output: {}".format(self.ref_outputs))
        print("Saved outputs:")
        print("  m#\tFrom\tTo\tOutput")
        for o in self.ref_outputs:
            print("  {}\t{}\t{}\t{}".format(o.moves_made, o.from_cell, o.to_cell, o.output))

    def create_next_ref_output(self, from_cell=None, to_cell=None, output=None, moves_made=None):
        """
        Create next SavedOutput object and add it to the log.
        """
        self.ref_outputs.append(SavedOutput(from_cell, to_cell, output, moves_made))
