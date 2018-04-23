from ChessPiece import ChessPiece, King, Knight
from Board import Board
from RefereeOutput import *
from Kriegspiel import Kriegspiel
"""
This ref is fair and does not allow any cheating in the game.
"""

class Referee():
    def __init__(self,):
        pass

    def is_path_blocked(self, _from, _to, board, echo=False):
        """
        Check if there are pieces in the way between two pieces.
        DOESNT SEEM TO WORK??
        """
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
            print("Reached end of path checks...")
            return False

        #Dont check current position:
        if _from in cells_to_check:
            cells_to_check.remove(_from)
        for i,j in cells_to_check:
            if not board.cell_is_free((i, j)):
                print("Piece blocking in cell ({},{})".format(i,j))
                return True
        return False

    def is_move_impossible(self, _from, _to, board, echo=False):
        """
        Is the move in the piece's movespace?
        """
        moving_piece = board.get_piece(_from)
        if isinstance(moving_piece, ChessPiece):
            return not (moving_piece.is_legal_transform(_from, _to, attacking=True) or moving_piece.is_legal_transform(_from, _to, attacking=False))
        else:
            return True

    def _is_move_legal(self, _from, _to, player_id, board, echo=False):
        """
        Actual is_legal_move check.
        Only ever called privately.
        """
        moving_piece = board.get_piece(_from)
        #Is the _to location on the board?
        if ((_to[0] >= 8) or (_to[1] >= 8)):
            return False 
        
        #Would you put yourself into check?
        next_board = Board()
        next_board.load_board(board.board)
        next_board.move_piece(_from, _to)
        if self.is_in_check(player_id, board=next_board):
            if echo: print("That would put you in check [{}->{}]".format(_from, _to))
            return False

        #Is there a piece in the _from cell?
        if not isinstance(moving_piece, ChessPiece):
            if echo:
                print("No piece in cell {}".format(_from))
            return False
        #If there is a piece on the _to cell, is it the other players?
        if board.get_piece(_to) != 0:
            if not board.get_owner_of_piece(_from) != board.get_owner_of_piece(_to):
                if echo: print("Piece in {} belongs to opponent.".format(_to))
                return False
            #If there is a piece on the _to cell, is the move in the moving pieces attack movespace
            if not moving_piece.is_legal_transform(_from, _to, attacking=True): #Replaced this line with a separate function
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
        if not board.get_owner_of_piece(_from) == player_id:
            if echo: print("Trying to move opponents piece.")
            return False
        #If piece can't jump, are all cells between _from and _to cells free?
        path_is_clear = True
        if echo: print("{}, can jump: {}".format(moving_piece, moving_piece.can_jump))
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
                if not board.cell_is_free((i, j)):
                    return False

        return True

    def verify_move(self, _from, _to, board, player_id, player_name=None, echo=False):
        """
        Take a move and return the relevant referee output.
        """
        #List of outputs generated by the move
        outputs = []

        if not player_name:
            player_name = "Player (ID{})".format(player_id)

        #If the move was made, what would the board be?
        next_board = Board()
        next_board.load_board(board.board)
        next_board.move_piece(_from, _to)
        #next_board.print_board(show_key=True)

        if self.is_move_impossible(_from, _to, board=board, echo=echo):
            return [Impossible(for_player=player_id, from_cell=_from, to_cell=_to)]
        #Move is not legal, return 'blocked'
        elif not self._is_move_legal(_from, _to, player_id, board=board, echo=echo):
            return [Blocked(for_player=player_id, from_cell=_from, to_cell=_to)]

        #Would put player in check mate
        #if self.is_in_check_mate(player_id, next_board.board):
        #    print("Youre putting yourself in checkmate")
        #    return CheckMate(for_player=player_name)

        #Would put other player in check mate
        if self.is_in_check_mate(Kriegspiel.opponent_id(player_id), next_board):
            if echo: print("Youre putting them in checkmate")
            #return CheckMate(for_player=Kriegspiel.opponent_id(player_id))
            outputs.append(CheckMate(for_player=Kriegspiel.opponent_id(player_id)))
        #Move is legal:
        #Move would put player in check
        #if self.is_in_check(player_id, next_board.board):
        #    return self.is_in_check(player_id, next_board.board)

        #Would put other player in check
        if self.is_in_check(Kriegspiel.opponent_id(player_id), next_board):
            #return self.is_in_check(Kriegspiel.opponent_id(player_id), next_board.board)
            outputs.append(self.is_in_check(Kriegspiel.opponent_id(player_id), next_board))

        #Move is legal and a piece was taken:
        if isinstance(board.get_piece(_to), ChessPiece) and board.get_piece(_to) != next_board.get_piece(_to):
            #return OkayTaken(for_player=player_name, additional_text=" - from cell {}".format(_to))
            outputs.append(OkayTaken(for_player=player_id, from_cell=_from, to_cell=_to, additional_text=" - from cell {}".format(_to)))
            outputs.append(OkayTaken(for_player=Kriegspiel.opponent_id(player_id), from_cell=_to, to_cell=_to, additional_text=" - from cell {}".format(_to)))
        else:
            #return Okay(for_player=player_name)
            outputs.append(Okay(for_player=player_id, from_cell=_from, to_cell=_to))

        return outputs

    #testing new check mate function:
    def _is_in_check_mate(self, player_id, board, echo=False):
        if self.is_in_check(player_id, board):
            defending_pieces = {}
            #Find all of the pieces of the defending player
            for row_no, row in enumerate(board):
                for cell_no, cell in enumerate(row):
                    if issubclass(type(cell), ChessPiece):
                        if cell.owner_id == player_id:
                            defending_pieces[cell] = (cell_no, row_no)


    def is_in_check_mate(self, player_id, board, echo=False):
        #TODO: Make this take in a Board object and not a board array ??
        #Is a player in check?
        #Returns CheckMate ref output if true. False otherwise
        if echo: print(" ---- testing with board:")
        if echo: print(board)
        if echo: print("Doing check-mate test...")
        if self.is_in_check(player_id, board):
            if echo: print("  - is currently in check")
            
            defending_pieces = {}
            #Find all of the pieces of the defending player
            for row_no, row in enumerate(board.board):
                for cell_no, cell in enumerate(row):
                    if issubclass(type(cell), ChessPiece):
                        if cell.owner_id == player_id:
                            defending_pieces[cell] = (cell_no, row_no)
            
            #previous_board_layout = board.save_board()
            for piece in defending_pieces:
                for move in list(set(piece.moves + piece.attack_moves)):
                    #Look at every possible move the defending pieces can make.
                    current_pos = defending_pieces[piece]
                    to_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
                    if echo: print("Testing {}->{}".format(current_pos, to_pos))

                    if self._is_move_legal(current_pos, to_pos, player_id=player_id, board=board, echo=False):
                        if echo: print("\tlegal move...")
                        #If the move is legal:
                        temp_board = Board()
                        temp_board.load_board(board)
                        temp_board.move_piece(current_pos, to_pos)
                        #If after that move, the player is no longer in check then it's not checkmate:
                        if not self.is_in_check(player_id, board=temp_board):
                            #return CheckMate(for_player=player_id)
                            if echo: print("Found a way out of check. Move {}, {}->{}".format(cell, current_pos, to_pos))
                            return False
            #return False
            return CheckMate(for_player=player_id)
        else:
            if echo: print("  - is not currently in check")
            return False
    

    def is_game_over(self, player_id, board):
        #Has the king of a given player been killed?
        king_pos = None
        for row_no, row in enumerate(board.board):
            for cell_no, cell in enumerate(row):
                if isinstance(cell, King) and cell.owner_id == player_id:
                    king_pos = (row_no, cell_no)
                    print("Found king: {}".format(king_pos))

        return self.is_in_check_mate(player_id, board) or not bool(king_pos)


    def is_in_check(self, player_id, board, echo=False):
        #Is a player in check?
        king_pos = None
        attacking_pieces = {}
        #Find the position of the king of the defending player and the positions of the attacking pieces
        for row_no, row in enumerate(board.board):
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
            #If a piece can attack the king's position, determine what type of check that is.
            if piece.is_legal_transform(attacking_pieces[piece], king_pos, attacking=True):
                #Is it an knight putting you in check?
                if isinstance(piece, Knight):
                    if echo: print("Knight check from: {}".format(piece))
                    return KnightCheck(for_player=player_id)

                elif attacking_pieces[piece][0] == king_pos[0] and attacking_pieces[piece][1] != king_pos[1]:
                    if echo: print("Row check from: {}".format(piece))
                    return RowCheck(for_player=player_id)

                elif attacking_pieces[piece][1] == king_pos[1] and attacking_pieces[piece][0] != king_pos[0]:
                    if echo: print("Column check from: {}".format(piece))
                    return ColumnCheck(for_player=player_id)
                else:
                    if echo: print("Diagonal check from: {}".format(piece))
                    return DiagonalCheck(for_player=player_id)

        #Player is not in check
        return False

    
    def is_move_legal(self, _from, _to, player_id, board, echo=False):
        return self._is_move_legal(_from, _to, player_id, board, echo=echo)

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
