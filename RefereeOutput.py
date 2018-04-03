"""
Define base classes of referee output
"""

class RefereeOutput():
    def __init__(self, for_player, additional_text=None, *args, **kwargs):
        self.label = None
        self.for_player = for_player
        self.success = None
        self.additional_text = additional_text

        if not additional_text:
            self.additional_text = ""
        else:
            self.additional_text = "[{}]".format(additional_text)

    def __str__(self):
        return "@{p} - {l} {e}".format(p=self.for_player, l=self.label, e=self.additional_text)

class LegalMove(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success = True

class IllegalMove(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success = False


"""
When a legal move is made
"""

class Okay(LegalMove):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Move was legal."


class OkayTaken(LegalMove):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Move was legal and you took a piece."


"""
When an illegal move is attempted
"""

class Blocked(IllegalMove):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Blocked"
        
"""
Check announcements
"""

class DiagonalCheck(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "You are in diagonal check."

class LongDiagonalCheck(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "You are in long diagonal check."

class KnightCheck(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "You are in check by a Knight."

class RowCheck(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "You are in row-check."

class ColumnCheck(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "You are in column-check."

class CheckMate(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "You are in check mate."

