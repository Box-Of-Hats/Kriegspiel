from ChessPiece import ChessPiece, King, Knight
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

    def verify_move(self, _from, _to, board, player_id, player_name=None, echo=False):
        """
        Take a move and return the relevant referee output.
        """
        if not player_name:
            player_name = "Player (ID{})".format(player_id)

        #If the move was made, what would the board be?
        next_board = Board()
        next_board.load_board(board.board)
        next_board.move_piece(_from, _to)
        next_board.print_board(show_key=True)

        #Move is not legal, return 'blocked'
        if not self._is_move_legal(_from, _to, player_id, echo=echo):
            return Blocked(for_player=player_name)
        #Move is legal:
        #Would put player in check mate
        elif self.is_in_check_mate(player_id, next_board.board):
            return CheckMate(for_player=player_name)
        #Would put other player in check mate
        elif self.is_in_check_mate((player_id +1) % 2, next_board.board):
            return CheckMate(for_player=(player_name+1)%2)
        #Move would put player in check
        elif self.is_in_check(player_id, next_board.board):
            return self.is_in_check(player_id, next_board.board)
            #return ColumnCheck(for_player=player_name)
        #Would put other player in check
        elif self.is_in_check((player_id +1) % 2, next_board.board):
            return self.is_in_check((player_id +1) % 2, next_board.board)
            #return ColumnCheck(for_player=(player_id +1) % 2)
        #Move is legal and a piece was taken:
        elif isinstance(board.get_piece(_to), ChessPiece) and board.get_piece(_to) != next_board.get_piece(_to): #TODO: Add condition
            return OkayTaken(for_player=player_name)
        #Move is legal:
        else:
            return Okay(for_player=player_name)


    def is_in_check_mate(self, player_id, board=None):
        #Is a player in check?
        #Returns CheckMate ref output if true. False otherwise
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
                        return CheckMate(for_player=player_id)
        return False
    

    def is_game_over(self, player_id, board=None):
        #Has the king of a given player been killed?
        king_pos = None
        if not board:
            board = self.game.board.board
        for row_no, row in enumerate(board):
            for cell_no, cell in enumerate(row):
                if isinstance(cell, King):
                    if cell.owner_id == player_id:
                        king_pos = (row_no, cell_no)

        return not bool(king_pos)


    def is_in_check(self, player_id, board=None):
        #Is a player in check?
        #We do not yet know the position of the king:
        king_pos = None
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


        if not king_pos:
            #If there is no king on the board, return true.
            return GameOver(for_player=player_id)
        
        for piece in attacking_pieces:
            if piece.is_legal_transform(attacking_pieces[piece], king_pos, attacking=True):
                #Is it an knight putting you in check?
                if isinstance(piece, Knight):
                    print("Knight check!!!!!!")
                    return KnightCheck(for_player=player_id)

                elif attacking_pieces[piece][0] == king_pos[0] and attacking_pieces[piece][1] != king_pos[1]:
                    print("Row check!!!!!!")
                    return RowCheck(for_player=player_id)

                elif attacking_pieces[piece][1] == king_pos[1] and attacking_pieces[piece][0] != king_pos[0]:
                    #print("Column check!!!!!!")
                    return ColumnCheck(for_player=player_id)
                else:
                    print("Diagonal check!!!!!!")
                    return DiagonalCheck(for_player=player_id)

        #Player is not in check
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
