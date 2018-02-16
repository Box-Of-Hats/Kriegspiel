from tkinter import *
from pieces import PieceFactory
from easygui import filesavebox, ccbox
"""
This has some incredibly questionable OO programming.
This was created in about an hour just as a quick tool.
Proceed with caution...
"""

class BoardBuilder():
    def __init__(self):
        #Set up frames
        root = Tk()
        root.title("Board Builder")
        app_window = Frame(root)
        app_window.grid(column=0, row=0)
        board_frame = Frame(app_window)
        board_frame.grid(column=1, row=0)
        piece_frame = Frame(app_window)
        piece_frame.grid(column=0, row=0)
        
        font_choice = ("Courier", 16)

        self.matrix = [[0 for x in range(8)] for y in range(8)]
        self.button_matrix = [[0 for x in range(8)] for y in range(8)]

        self.piece_symbols = {"0": ""}

        black_pieces = list("prnbkq")
        white_pieces = list("PRNBKQ")

        factory = PieceFactory()
        for t in black_pieces:
            tmp = factory.create_piece(piece=t, use_symbol=True, colour=0)
            self.piece_symbols[t] = tmp.symbol
            tmp = factory.create_piece(piece=t, use_symbol=True, colour=1)
            self.piece_symbols[t.upper()] = tmp.symbol


        cell_colour = 0
        cell_colours = {
            0: "#e0e0e0",
            1: "#bababa",
        }

        for i in range(0,8):
            for j in range(0,8):
                t = Button(board_frame, height=1, width=2, command=lambda i=i,j=j: self.set_piece(i, j), font=font_choice, bg=cell_colours[cell_colour], relief="flat")
                t.grid(column=j, row=i)
                self.button_matrix[i][j] = t
                cell_colour = (cell_colour + 1) %2
            cell_colour = (cell_colour + 1) %2

        self.current_piece = StringVar()
        self.current_piece.set("p")

        for r, piece in enumerate(white_pieces):
            b = Radiobutton(piece_frame, text=self.piece_symbols[piece],
                            variable=self.current_piece, value=piece, font=font_choice)
            b.grid(row=r, column=0)

        for r, piece in enumerate(black_pieces):
            b = Radiobutton(piece_frame, text=self.piece_symbols[piece],
                            variable=self.current_piece, value=piece, font=font_choice)
            b.grid(row=r, column=1)

        Radiobutton(piece_frame, text="␡", variable=self.current_piece, value="0", font=font_choice).grid(row=8, column=0)

        Button(piece_frame, text="Save", command= lambda: self.save_matrix(filesavebox(default='.\\*.txt')), font=font_choice, relief="groove").grid(row=10, column=0, columnspan=2)
        Button(piece_frame, text="Clear", command= lambda: self.clear(), font=("Courier", 10), relief="groove").grid(row=11, column=0, columnspan=2,)

        root.mainloop()
    
    def set_piece(self, i, j):
        self.matrix[i][j] = self.current_piece.get()
        self.button_matrix[i][j].config(text=self.piece_symbols[self.current_piece.get()])

    def save_matrix(self, fname=None):
        if fname:
            with open(fname, "w") as f:
                for row in self.matrix:
                    for cell in row:
                        f.write(str(cell))
                    f.write("\n")
            print("Saved layout to: {}".format(fname))
        else:
            return False
        
    def clear(self):
        if ccbox("Clear?", "Confirm you wish to clear", choices=("sure", "nah")):
            self.matrix = [[0 for x in range(8)] for y in range(8)]
            for row in self.button_matrix:
                for b in row:
                    b.config(text="")

if __name__ == "__main__":
    b = BoardBuilder()
    