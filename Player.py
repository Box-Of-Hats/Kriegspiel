import itertools
from ChessPiece import ChessPiece
import random
from CheatAnalyser import CheatAnalyser

class Player():
    def __init__(self, name=None):
        self.name = name

    def do_move(self, board):
        """
        Choose a move and return it in the form (from, to) where
        from and to are coordinates on the board.
        """
        raise NotImplementedError("do_move method not implemented for Player: {}".format(self))

class HumanPlayer(Player):
    def __init__(self, *args, **kwargs):
        self.analyser = CheatAnalyser()
        super().__init__(*args, **kwargs)

    def do_move(self, board):
        board.print_board(show_key=True)
        col_conversion = {a: b for a,b in zip(list("abcdefgh"),[0,1,2,3,4,5,6,7])}
        row_conversion = {a: b for a,b in zip(list("87654321"),[0,1,2,3,4,5,6,7])}
        in_string = input(">")
        #Handle user input and potential errors if the format is incorrect:
        try:
            _from, _to = in_string.split(" ")
        except ValueError:
            print("Invalid input!")
            print("\tMust be in format: [from_location] [to_location] (e.g 'a2 a3')")
            return self.do_move(board)

        try:
            #Convert user input to numerical coordinates. a7 -> (0,1); a6 -> (0,2)...
            from_cell = (col_conversion[_from[0]], row_conversion[_from[1]])
            to_cell = (col_conversion[_to[0]], row_conversion[_to[1]])
        except KeyError:
            print("Invalid move coordinates.")
            print("\tMust be in range a1-h7")
            return self.do_move(board)
            
        print("You want to move from {} to {}".format(from_cell, to_cell))
        return (from_cell, to_cell)

class RandomPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_move(self, board):
        my_pieces = {}
        for row_no, row in enumerate(board.board):
            for col_no, cell in enumerate(row):
                if isinstance(cell, ChessPiece):
                    my_pieces[(col_no, row_no)] = cell

        moving_piece_loc = random.choice([i for i in my_pieces])
        moving_piece_type = my_pieces[moving_piece_loc]
        random_move = random.choice(moving_piece_type.moves + moving_piece_type.attack_moves)
        random_to = ((moving_piece_loc[0] - random_move[0]) %8, (moving_piece_loc[1] - random_move[1]) %8)
        print(my_pieces)
        print("Random move: {} -> {}".format(moving_piece_loc, random_to))
        return (moving_piece_loc, random_to)
        