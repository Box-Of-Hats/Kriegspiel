import itertools

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
        super().__init__(*args, **kwargs)

    def do_move(self, board):
        board.print_board(show_key=True)
        col_conversion = {a: b for a,b in zip(list("abcdefgh"),[0,1,2,3,4,5,6,7])}
        row_conversion = {a: b for a,b in zip(list("87654321"),[0,1,2,3,4,5,6,7])}
        in_string = input(">")

        _from, _to = in_string.split(" ")
        from_cell = (row_conversion[_from[1]], col_conversion[_from[0]])
        to_cell = (row_conversion[_to[1]], col_conversion[_to[0]])
        print("You want to move from {} to {}".format(from_cell, to_cell))
        return (from_cell, to_cell)

class RandomPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)