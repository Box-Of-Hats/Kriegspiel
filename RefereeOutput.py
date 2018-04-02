"""
        self.outputs = {
            0: {"name": "Okay", "success": True},
            1: {"name": "Blocked", "success": False},
            2: {"name": "Piece taken", "success": True},
            3: {"name": "Check", "success": True},
            4: {"name": "Check mate", "success": True},
        }
"""

class RefereeOutput():
    def __init__(self, for_player, *args, **kwargs):
        self.label = None
        self.for_player = for_player
        self.success = None

    def __str__(self):
        return "Player: {p} - {l}".format(p=self.for_player, l=self.label)

class LegalMove(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success = True

class IllegalMove(RefereeOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success = False



class Blocked(IllegalMove):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Blocked"
        

class Check(LegalMove):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Check"
        self.success = True


c = Check(for_player=2)
print(c)
