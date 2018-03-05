#!/usr/bin/python
# -*- coding: utf-8 -*-

from pieces import Pawn, Rook, Knight, Bishop, King, Queen, PieceFactory, ChessPiece
from Board import Board
from players import HumanPlayer, RandomPlayer
from Referee import * 
import argparse

"""
Misc:
TODO: Implement random moving opponent
Chess Implementation:
TODO: Implement deciding if a player is in check MATE
Kriegspiel:
TODO: Implement Referee
TODO: Indicate what type of check a player is in
Smart thing:
TODO: Implement Analyser

"""


DEFAULT_LAYOUT = ["rnbqkbnr".upper(), "pppppppp".upper(), [0]*8, [0]*8, [0]*8, [0]*8, "pppppppp", "rnbqkbnr"]

[int(i) for i in list("00000000")]

class Chess():
    def __init__(self,  player_1, player_2, referee, board_layout=None, use_symbols=True,):
        """
        board_layout, iterable, a board layout to load.
        use_symbols, bool, if pieces should use chess symbols (♔) or letters (K).
        """
        self.board = Board()
        self.players = {0: player_1,
                        1: player_2}
        self.use_symbols = use_symbols
        self.last_move = 1 #Who's move it was last
        self.referee = referee
        self.referee.game = self
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
        !! Assumes move is legal!
        """

        moving_piece = self.board.get_piece(_from)
        self.board.move_piece(_from, _to)
        moving_piece.move_counter += 1
        return True

    def do_move(self):
        self.last_move = (self.last_move + 1) % 2
        current_player_id = self.last_move
        
        current_player = self.players[self.last_move]

        print("\nIt's {name}'s (ID: {id}) turn to make a move.".format(name=current_player.name, id=current_player_id))

        valid_move = False
        while not valid_move:
            _from, _to = current_player.do_move(self.get_board_for_player(current_player_id))
            valid_move = self.referee.is_move_legal(_from=_from, _to=_to, player_id=self.last_move)

        #When move is valid, perform the move:
        self.move_piece(_from, _to, player_id=self.last_move)

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

    def get_pieces_for_player(self, player_id):
        """
        <Generator>
        Get all of the pieces of a given player
        """
        for r_no, row in enumerate(self.board.board):
            for c_no, cell in enumerate(row):
                if isinstance(cell, ChessPiece):
                    if cell.owner_id == player_id:
                        yield cell
        
if __name__ == "__main__":
    #Check if terminal supports chess characters. Use lettering for characters if not.
    use_symbols = True
    try:
        print(King().symbol,)
    except UnicodeEncodeError:
        use_symbols = False
    #Define players
    p1 = HumanPlayer(name="Jake")
    p2 = HumanPlayer(name="Cheating Bob")
    #Create referee
    #referee = Referee()
    referee = Referee()
    #Parse any passed args:
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--layout_file", help="The filepath of the layout you wish to load.")
    args = parser.parse_args()

    if args.layout_file:
        with open(args.layout_file) as layout_file:
            layout = layout_file.read().splitlines()
    else:
        layout = DEFAULT_LAYOUT
    #Initialise Chess game
    c = Chess(player_1=p1, player_2=p2, referee=referee, use_symbols=use_symbols)
    c.load_game(layout)

    while True:
        print("Full board:")
        c.print_board(show_key=True)
        print("0: Is in check?: {}; mate: {}".format(c.referee.is_in_check(0), c.referee.is_in_check_mate(0)))
        print("1: Is in check?: {}; mate: {}".format(c.referee.is_in_check(1), c.referee.is_in_check_mate(1)))
        c.do_move()
