#!/usr/bin/python
# -*- coding: utf-8 -*-

from ChessPiece import Pawn, Rook, Knight, Bishop, King, Queen, PieceFactory, ChessPiece
from Board import Board
from Player import HumanPlayer, RandomPlayer
from Referee import * 
import argparse

"""
Kriegspiel:
TODO: Implement Referee output
Smart thing:
TODO: Implement Analyser


TODO: Player can move their king into check - fix!
TODO: Checkmate doesnt seem to work properly :/

"""


DEFAULT_LAYOUT = ["rnbqkbnr".upper(), "pppppppp".upper(), [0]*8, [0]*8, [0]*8, [0]*8, "pppppppp", "rnbqkbnr"]

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
        self.moves_made = 0
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
        self.last_move = Chess.opponent_id(self.last_move)
        current_player_id = self.last_move
        
        current_player = self.players[self.last_move]

        print("\nIt's {name}'s (ID: {id}) turn to make a move.".format(name=current_player.name, id=current_player_id))

        is_valid_move = False
        while not is_valid_move:
            _from, _to = current_player.do_move(self.get_board_for_player(current_player_id))
            is_valid_move = self.referee.is_move_legal(_from=_from, _to=_to, player_id=self.last_move)
            move_output = self.referee.verify_move(_from=_from, _to=_to, board=self.board, player_id=self.last_move, player_name=self.players[self.last_move].name)
            print(move_output)
            current_player.notify(move_output, self.moves_made)


        #When move is valid, perform the move:
        self.move_piece(_from, _to, player_id=self.last_move)
        self.moves_made += 1

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


    def opponent_id(player_id):
        """
        <Static>
        Get the opposing ID of a player.
        """
        return (player_id+1)%2




def pvp(c):
    """Play chess in PVP mode."""
    import os
    #Ensure that correct console clearing command is in use, depending on the OS
    if os.name == "nt":
        clear_cmd = "cls"
    else:
        clear_cmd = "clear"

    while True:
        c.do_move()
        input("@{} Press enter once you've ready.".format(c.players[c.last_move].name))
        os.system(clear_cmd)
        input("Press enter when you're ready >")

def debug(c):
    """Play chess with debug mode enabled. Prints out entire board after each move."""
    while True:
        print("Full board:")
        c.print_board(show_key=True)
        c.do_move()

def testing(c):
    #c.do_move()
    c.referee.verify_move((0,0), (0,1), c.board, 0)

                    
if __name__ == "__main__":
    #Check if terminal supports chess characters. Use lettering for characters if not.
    use_symbols = True
    try:
        print(King().symbol,)
    except UnicodeEncodeError:
        use_symbols = False

    referees = {
        "fair": Referee(),
        "0": CheatingReferee(cheating_player_id=0),
        "1": CheatingReferee(cheating_player_id=1),
        "laxx": LaxxReferee(),
    }

    player_types = {
        "human": HumanPlayer,
        "random": RandomPlayer,
    }

    game_modes = {
        "pvp": pvp,
        "debug": debug,
        "testing": testing,
    }

    #Parse any passed args:
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--layout_file", help="The filepath of the layout you wish to load.")
    parser.add_argument("-r", "--referee", help="The type of referee. 0: fair, 1: cheat w/p1, 2: cheat w/p2, 3: laxx", choices=sorted([x for x in referees]))
    parser.add_argument("-g", "--gamemode", help="The game mode to use.", choices=sorted([x for x in game_modes]))
    parser.add_argument("-p1", "--player1", help="The type of player one.", choices=sorted([x for x in player_types]))
    parser.add_argument("-p2", "--player2", help="The type of player two.", choices=sorted([x for x in player_types]))
    args = parser.parse_args()


    #Set the players
    if args.player1:
        p1 = player_types[args.player1](name="White")
    else:
        p1 = HumanPlayer(name="White") 
    if args.player2:
        p2 = player_types[args.player2](name="Black")
    else:
        p2 = HumanPlayer(name="Black") 

    #Set the layout
    if args.layout_file:
        with open(args.layout_file) as layout_file:
            layout = layout_file.read().splitlines()
    else:
        layout = DEFAULT_LAYOUT

    #Set the type of referee
    if args.referee:
        referee = referees[int(args.referee)]
    else:
        #If referee is not specified, use a fair referee
        referee = referees["fair"]
        
    #Set the game mode
    if args.gamemode:
        gamemode = args.gamemode
    else:
        gamemode = "debug"

    #Initialise Chess game
    c = Chess(player_1=p1, player_2=p2, referee=referee, use_symbols=use_symbols)
    c.load_game(layout)

    game_modes[gamemode](c)
    #c.do_move()
    #referee.verify_move()
