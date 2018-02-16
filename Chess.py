from pieces import Pawn, Rook, Knight, Bishop, King, Queen, PieceFactory, ChessPiece
from Board import Board
from players import HumanPlayer, RandomPlayer
import argparse

DEFAULT_LAYOUT = ["rnbqkbnr".upper(), "pppppppp".upper(), [0]*8, [0]*8, [0]*8, [0]*8, "pppppppp", "rnbqkbnr"]

[int(i) for i in list("00000000")]

class Chess():
    def __init__(self,  player_1, player_2, board_layout=None, use_symbols=True,):
        """
        board_layout, iterable, a board layout to load.
        use_symbols, bool, if pieces should use chess symbols (♔) or letters (K).
        """
        self.board = Board()
        self.players = {0: player_1,
                        1: player_2}
        self.use_symbols = use_symbols
        self.last_move = 0 #Who's move it was last
        if not board_layout:
            #If no board layout specified, load default starting chess board
            self.load_game(DEFAULT_LAYOUT)
        else:
            self.load_game(board_layout)

    def print_board(self, show_key=True):
        self.board.print_board(show_key=show_key)

    def load_game(self, board_layout):
        """
        Load a game from a matrix in the format:
        ["rnbqkbnr", "pppppppp", "00000000", ... ]
        
        CAPITAL letters are WHITE pieces, lowercase are black.
        """
        piece_layout = []
        for row in board_layout:
            temp_row = []
            for piece in row:
                if str(piece) == "0":
                    temp_piece = 0
                elif piece.istitle():
                    temp_piece = PieceFactory().create_piece(piece=piece.lower(), colour=0, use_symbol=self.use_symbols)
                else:
                    temp_piece = PieceFactory().create_piece(piece=piece, colour=1, use_symbol=self.use_symbols)
                temp_row.append(temp_piece)
            piece_layout.append(temp_row)
        self.board.load_board(piece_layout)
            
    def move_piece(self, _from, _to, player_id):
        """
        Move a piece from one cell to another.
        TODO: Add checks for if a move is legal
        """
        #try:
        if not self.is_legal_move(_from, _to, player_id):
            print("Illegal Move.")
            return False

        moving_piece = self.board.get_piece(_from)
        self.board.move_piece(_from, _to)
        return True
        #except:
        #    return False

    def is_legal_move(self, _from, _to, player_id):
        moving_piece = self.board.get_piece(_from)
        #Is there a piece in the _from cell?
        if not isinstance(moving_piece, ChessPiece):
            return False
        #Is the move in the piece's movespace?
        in_move_space = moving_piece.is_legal_transform(_from, _to)
        #If there is a piece on the _to cell, is it the other players?
        if self.board.get_piece(_to) != 0:
            not_moving_onto_own_piece = self.board.get_owner_of_piece(_from) != self.board.get_owner_of_piece(_to)
        else:
            not_moving_onto_own_piece = True
        #Is the piece being moved belonging to the player trying to move it?
        is_own_piece = self.board.get_owner_of_piece(_from) == player_id
        #If piece can't jump, are all cells between _from and _to cells free?

        #TODO: MAKE THIS WORK! Currently nothing I've tried actually works
        #m = (_to[1] - _from[1])/(_to[0] - _from[0])
        #x , y = _to
        #c = y + (m*x)
        #print("m={}".format(m))
        #print("c={}".format(c))
        #print("y = {m}x + {c}".format(m=m, c=c))
        #x_points = list(range(_from[1], _to[0]-_from[1]))
        #y_points = [(m*i)+c for i in x_points]
        #print("x_points={}".format(x_points))
        #print("y_points={yp}, (calculated with: y={m}x + {c})".format(yp=y_points, m=m, c=c))

        
        not_blocked = True
        """
        if not moving_piece.can_jump:
            x_diff = abs(_to[0] - _from[0])
            y_diff = abs(_to[1] - _from[1])
            print(x_diff, y_diff)
            if x_diff == y_diff:
                for i in range(0, x_diff):
                    print("Is cell free? ({},{}): {}".format(i,i, self.board.cell_is_free((i, i))))
                    if not self.board.cell_is_free((i, i)):
                        not_blocked = False
                        break
        """

        print("In move space: {}".format(in_move_space))
        print("Space not occupied by own piece: {}".format(not_moving_onto_own_piece))
        print("Is own piece: {}".format(is_own_piece))
        print("Path not blocked: {}".format(not_blocked))
        return in_move_space and not_moving_onto_own_piece and is_own_piece and not_blocked

    def user_prompt(self):
        """
        DELETE
        Just shows that save/load works
        """
        in_string = input(">")
        if in_string == "save": #Testing save function. Appears to work
            print("Saving game.")
            self.saved_game = self.board.save_board()
            self.load_game(DEFAULT_LAYOUT)

        elif in_string == "load": #Testing load funciton. Appears to work
            print("Loading game")
            self.load_game(self.saved_game)

    def do_move(self):
        self.last_move = (self.last_move + 1) % 2
        current_player_id = self.last_move
        current_player = self.players[self.last_move]
        #move = _from, _to = current_player.do_move(self.get_board_for_player(current_player))
        valid_move = False
        while not valid_move:
            _from, _to = current_player.do_move(self.get_board_for_player(current_player_id))
            valid_move = self.move_piece(_from, _to, player_id=self.last_move)

    def get_board_for_player(self, player_id):
        """
        Return the board from a player's perspective.
        Only includes their pieces.
        """
        board_copy = Board()
        for r_no, row in enumerate(self.board.board):
            for c_no, cell in enumerate(row):
                if isinstance(cell, ChessPiece):
                    if cell.owner_id == player_id:
                        board_copy.add_piece(r_no, c_no, cell)

        return board_copy
        
if __name__ == "__main__":
    use_symbols = True
    try:
        print(King().symbol, end="\r")
    except UnicodeEncodeError:
        use_symbols = False

    p1 = HumanPlayer(name="Jake")
    p2 = HumanPlayer(name="Bob")


    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--layout_file", help="The filepath of the layout you wish to load.")
    args = parser.parse_args()

    if args.layout_file:
        with open(args.layout_file) as layout_file:
            layout = layout_file.read().splitlines()
    else:
        layout = DEFAULT_LAYOUT

    c = Chess(player_1=p1, player_2=p2, use_symbols=use_symbols)
    c.load_game(layout)


    while True:
        c.print_board(show_key=True)
        print("It's {name}'s (ID: {id}) turn to make a move.".format(name=c.players[c.last_move].name, id=c.last_move))
        c.do_move()
