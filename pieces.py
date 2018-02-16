import itertools

"""
TODO: Define legal transforms for all pieces
Pawn    
Rook    ✔
Knight  ✔
Bishop  ✔
King    ✔
Queen   ✔

"""

class PieceFactory():
    def __init__(self):
        self.pieces = {
            "p": Pawn,
            "r": Rook,
            "n": Knight,
            "b": Bishop,
            "k": King,
            "q": Queen,
        }

    def create_piece(self, piece, colour, use_symbol):
        """
        Colour must be explicitly stated.
        Piece must be specified with a LOWERCASE letter.
        Use_symbol is bool and decides if a piece is represented by a letter or a symbol.
        """
        return self.pieces[piece](colour=colour, use_symbol=use_symbol)

    def letter_to_symbol(self, letter, colour=0):
        """Get the chess symbol for a piece from it's representing letter"""
        for piece_letter in self.pieces:
            if letter == piece_letter:
                return self.pieces[piece_letter]().symbols[colour]
        return False

class ChessPiece():
    def __init__(self, use_symbol=True, colour=0):
        self.owner_id = colour
        self.illegal_moves = [(0,0)]
        self.letter = self.letters[colour]
        self.moved_counter = 0
        if use_symbol:
            self.symbol = self.symbols[colour]
        else:
            self.symbol = self.letters[colour]

        if isinstance(self.moves, dict): #If moves are colour depenedant, moves should be a dict
            self.moves = self.moves[colour]
        
        if not hasattr(self, "can_jump"):
            self.can_jump = False

    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return self.symbol

    def is_legal_transform(self, _from, _to):
        """
        Check if a move transform is legal for that piece type.
        Only checks if the move is in the piece's movespace.
        """
        x_transform = _from[0] - _to[0]
        y_transfrom = _from[1] - _to[1]
        return (x_transform, y_transfrom) in self.moves
            
class Pawn(ChessPiece):
    def __init__(self, *args, **kwargs):
        self.name = "Pawn"
        self.symbols = {0: "♙", 1: "♟"}
        self.letters = {0: "P", 1: "p"}
        self.moves = {0: [(0,0), (-1,0)], 1: [(0,0), (1,0)]}
        super().__init__(*args, **kwargs)

class King(ChessPiece):
    def __init__(self, *args, **kwargs):
        self.name = "King"
        self.symbols = {0: "♔", 1: "♚"}
        self.letters = {0: "K", 1: "k"}
        self.moves = [combination for combination in itertools.product([0,-1,1], repeat=2)]
        super().__init__(*args, **kwargs)

class Queen(ChessPiece):
    def __init__(self, *args, **kwargs):
        self.name = "Queen"
        self.symbols = {0: "♕", 1: "♛"}
        self.letters = {0: "Q", 1: "q"}
        up_moves = [(0,i) for i in range(0,8)]
        down_moves = [(0,i) for i in range(-8,0)]
        right_moves = [(i,0) for i in range(0,8)]
        left_moves = [(i,0) for i in range(-8, 0)]
        up_right = [(a,a) for a in range(0,8)]
        down_right = [(a,-a) for a in range(0,8)]
        up_left = [(-a,a) for a in range(0,8)]
        down_left = [(-a,-a) for a in range(0,8)]
        self.moves = list(itertools.chain(up_right, down_right, up_left, down_left, down_moves, up_moves, right_moves, left_moves))

        super().__init__(*args, **kwargs)
        
class Rook(ChessPiece):
    def __init__(self, *args, **kwargs):
        self.name = "Rook"
        self.symbols = {0: "♖", 1: "♜"}
        self.letters = {0: "R", 1: "r"}
        up_moves = [(0,i) for i in range(0,8)]
        down_moves = [(0,i) for i in range(-8,0)]
        right_moves = [(i,0) for i in range(0,8)]
        left_moves = [(i,0) for i in range(-8, 0)]
        self.moves = list(itertools.chain(down_moves, up_moves, right_moves, left_moves))
        super().__init__(*args, **kwargs)

class Knight(ChessPiece):
    def __init__(self, *args, **kwargs):
        self.name = "Knight"
        self.symbols = {0: "♘", 1: "♞"}
        self.letters = {0: "N", 1: "n"}
        self.moves = [(2, 1), (2, -1), (-2,1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        self.can_jump = True
        super().__init__(*args, **kwargs)

class Bishop(ChessPiece):
    def __init__(self, *args, **kwargs):
        self.name = "Bishop"
        self.symbols = {0: "♗", 1: "♝"}
        self.letters = {0: "B", 1: "b"}
        up_right = [(a,a) for a in range(0,8)]
        down_right = [(a,-a) for a in range(0,8)]
        up_left = [(-a,a) for a in range(0,8)]
        down_left = [(-a,-a) for a in range(0,8)]
        self.moves = list(itertools.chain(up_right, down_right, up_left, down_left))
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    factory = PieceFactory()
    for t in list("pnkbqn"):
        tmp = factory.create_piece(piece=t, use_symbol=True, colour=0)
        print(tmp, tmp.name)
    print(factory.letter_to_symbol("n", 1))
    print(factory.letter_to_symbol("n", 0))
