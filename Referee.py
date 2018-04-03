from ChessPiece import ChessPiece, King
from Board import Board
from RefereeOutput import *

"""
This ref is fair and does not allow any cheating in the game.
"""
class Referee():
    def __init__(self,):


        """
        !!!
        CHECK is currently same output, regardless of the type of check (long, diag etc.) and
        regardless of who is in check. 
        !!!
        """
        self.outputs = {
            "okay": Okay,
            "okay_taken": OkayTaken,
            "blocked": Blocked,
            "diag_check": DiagonalCheck,
            "long_diag_check": LongDiagonalCheck,
            "row_check": RowCheck,
            "col_check": ColumnCheck,
            "knight_check": KnightCheck,
            "check_mate": CheckMate,
        }

    def _is_move_legal(self, _from, _to, player_id, echo=True):
        """
        Actual is legal move check.
        """
        moving_piece = self.game.board.get_piece(_from)
        #Is the _to location on the board?
        #print("to: {}".format(_to))
        if ((_to[0] >= 8) or (_to[1] >= 8)):
            #print("Hey wow, thats above 8")
            return False 
        #else:
        #print("Thats not above 8")
        #Is there a piece in the _from cell?
        if not isinstance(moving_piece, ChessPiece):
            if echo:
                print("No piece in cell {}".format(_from))
            return False
        #If there is a piece on the _to cell, is it the other players?
        if self.game.board.get_piece(_to) != 0:
            if not self.game.board.get_owner_of_piece(_from) != self.game.board.get_owner_of_piece(_to):
                if echo: print("Piece in {} belongs to opponent.".format(_to))
                return False
            #If there is a piece on the _to cell, is the move in the moving pieces attack movespace
            if not moving_piece.is_legal_transform(_from, _to, attacking=True):
                if echo: 
                    print("Not a valid attack move for piece: {}".format(moving_piece))
                    print("legal att moves: {}".format(moving_piece.attack_moves))
                return False
        #else, the space is free. -> Is the move in the piece's movespace?
        elif not moving_piece.is_legal_transform(_from, _to):
            if echo: 
                print("Not a valid move for piece: {}".format(moving_piece))
            return False
        #Is the piece being moved belonging to the player trying to move it?
        if not self.game.board.get_owner_of_piece(_from) == player_id:
            if echo: 
                print("Trying to move opponents piece.")
            return False
        #If piece can't jump, are all cells between _from and _to cells free?
        path_is_clear = True
        if echo: 
            print("{}, can jump: {}".format(moving_piece, moving_piece.can_jump))
        if not moving_piece.can_jump:
            if _from[1] > _to[1]:
                y_range = list(range(_from[1], _to[1], -1))
            else:
                y_range = list(range(_from[1], _to[1]))

            if _from[0] > _to[0]:
                x_range = list(range(_from[0], _to[0], -1))
            else:
                x_range = list(range(_from[0], _to[0]))
    
            #If move is diagonal:
            if abs(_to[0] - _from[0]) == abs(_to[1] - _from[1]):
                cells_to_check = list(zip(x_range, y_range))
                #Dont check current position:
                if _from in cells_to_check:
                    cells_to_check.remove(_from)
            #If move is vertical:
            elif _from[0] == _to[0]:
                x_range = [_from[0]]*len(y_range)
                cells_to_check = list(zip(x_range, y_range))
                if _from in cells_to_check:
                    cells_to_check.remove(_from)
            #If move is horizontal:
            elif _from[1] == _to[1]:
                y_range = [_from[1]]*len(x_range)
                cells_to_check = list(zip(x_range, y_range))
                if _from in cells_to_check:
                    cells_to_check.remove(_from)
            else:
                cells_to_check = [(None, None)]
                if echo: 
                    print("Something went wrong with checking if the path was clear! >:c ")
                    print("Debug:")
                    print("\tFrom: {f} , To: {t} , Player: {p}".format(f=_from, t=_to, p=player_id))
            #Is the cell free?
            for i,j in cells_to_check:
                if not self.game.board.cell_is_free((i, j)):
                    return False

        return True

    def verify_move(self, _from, _to, board, player_id, echo=False):
        """
        Take a move and return the relevant referee output.
        """
        #If the move was made, what would the board be?
        next_board = Board()
        next_board.load_board(board.board)
        next_board.move_piece(_from, _to)
        next_board.print_board(show_key=True)

        #Move is not legal, return 'blocked'
        if not self._is_move_legal(_from, _to, player_id, echo=echo):
            return self.outputs["blocked"](for_player=player_id)
        #Move is legal:
        #Move would put player in check
        elif self.is_in_check(player_id, next_board.board):
            return self.outputs["check"](for_player=player_id)
        #Would put other player in check
        elif self.is_in_check((player_id +1) % 2, next_board.board):
            return self.outputs["check"](for_player=player_id)
        #Would put player in check mate
        elif self.is_in_check_mate(player_id, next_board.board):
            return self.outputs["check_mate"](for_player=player_id)
        #Would put other player in check mate
        elif self.is_in_check_mate((player_id +1) % 2, next_board.board):
            return self.outputs["check_mate"](for_player=player_id)
        #Move is legal and a piece was taken:
        elif True: #TODO: Add condition
            return self.outputs["okay_taken"](for_player=player_id)
        #Move is legal:
        elif True: #TODO Add condition
            return self.outputs["okay"](for_player=player_id)
        else:
            raise Exception("Was verifying move but no conditions were met :/ :/ smh")

        


    def is_in_check_mate(self, player_id, board=None):
        #Is a player in check?
        if not board:
            board = self.game.board.board
        defending_pieces = {}
        for row_no, row in enumerate(board):
            for cell_no, cell in enumerate(row):
                if issubclass(type(cell), ChessPiece):
                    if cell.owner_id == player_id:
                        defending_pieces[cell] = (row_no, cell_no)
        
        #previous_board_layout = board.save_board()
        for piece in defending_pieces:
            for move in list(set(piece.moves + piece.attack_moves)):
                current_pos = defending_pieces[piece]
                to_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
                #print("Checking {}: {}->{}".format(piece, current_pos, to_pos))
                if self._is_move_legal(current_pos, to_pos, player_id=player_id, echo=False):
                    #print("Legal move {}->{}".format(current_pos, to_pos))
                    temp_board = Board()
                    temp_board.load_board(board)
                    #print("Move: {}->{}".format(current_pos, to_pos))
                    temp_board.move_piece(current_pos, to_pos)
                    if self.is_in_check(player_id, board=board):
                        return True
        return False
    

    def is_in_check(self, player_id, board=None):
        #Is a player in check?
        if not board:
            board = self.game.board.board
        attacking_pieces = {}
        for row_no, row in enumerate(board):
            for cell_no, cell in enumerate(row):
                if isinstance(cell, King):
                    if cell.owner_id == player_id:
                        king_pos = (row_no, cell_no)
                elif issubclass(type(cell), ChessPiece):
                    if cell.owner_id != player_id:
                        attacking_pieces[cell] = (row_no, cell_no)
        
        for piece in attacking_pieces:
            if piece.is_legal_transform(attacking_pieces[piece], king_pos, attacking=True):
                return True
        return False
    
    def is_move_legal(self, _from, _to, player_id, echo=True):
        return self._is_move_legal(_from, _to, player_id, echo=True)

    def set_game(self, _game):
        self._game = _game

    def get_game(self):
        return self._game

    game = property(get_game, set_game)

"""
This ref is consorting with a player and allows them to cheat.
"""
class CheatingReferee(Referee):
    def __init__(self, cheating_player_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Id of player who is cheating:
        self.cheating_player_id = cheating_player_id

    def is_move_legal(self, *args, **kwargs):
        #Override is_move_legal method.
        #Allows one player to cheat and uses the standard rules for the other player.
        if kwargs["player_id"] == self.cheating_player_id:
            return True
        else:
            return super().is_move_legal(*args, **kwargs)
        
"""
This ref couldn't care less about the game. Anything goes!
"""
class LaxxReferee(Referee):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_move_legal(self, *args, **kwargs):
        return True
