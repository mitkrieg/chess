from pieces import *

class Board:
    
    def __init__(self):
        self.grid = [
            [Rook('black',(0,0)),Knight('black',(0,1)),Bishop('black',(0,2)),Queen('black'),King('black'),Bishop('black',(0,5)),Knight('black',(0,6)),Rook('black',(0,7))],
            [Pawn('black',(1,i)) for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [Pawn('white',(6,i)) for i in range(8)],
            [Rook('white',(7,0)),Knight('white',(7,1)),Bishop('white',(7,2)),Queen('white'),King('white'),Bishop('white',(7,5)),Knight('white',(7,6)),Rook('white',(7,7))],
        ]
    
    def __str__(self):
        s = ''
        for row in self.grid:
            for col in row:
                if col is not None:
                    s += col.symbol() + ' '
                else:
                    s += 'XX '
            s += '\n'

        return s

    def check_king(self):
        pass

