from pieces import *

class Board:
    
    def __init__(self):
        self.grid = [
            [Rook('black',(0,0),'q'),Knight('black',(0,1),'q'),Bishop('black',(0,2),'q'),Queen('black'),King('black'),Bishop('black',(0,5),'k'),Knight('black',(0,6),'k'),Rook('black',(0,7),'k')],
            [Pawn('black',(1,i),i) for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [Pawn('white',(6,i),i) for i in range(8)],
            [Rook('white',(7,0),'q'),Knight('white',(7,1),'q'),Bishop('white',(7,2),'q'),Queen('white'),King('white'),Bishop('white',(7,5),'k'),Knight('white',(7,6),'k'),Rook('white',(7,7),'k')],
        ]
        self.black_king = self.grid[0][4]
        self.white_king = self.grid[7][4]
    
    def __str__(self):
        s = ''
        for i, row in enumerate(self.grid):
            s += str(i) + ' '
            for col in row:
                if col is not None:
                    s += col.symbol() + ' '
                else:
                    s += 'XX '
            s += '\n'

        return '   0  1  2  3  4  5  6  7\n' + s

    def check_king(self,color):
        assert color in ('white','black'), 'Must be white or black'

        if color == 'white':
            king = self.white_king
        else:
            king = self.black_king

        checks = 0

        for row in self.grid:
            for col in row:
                try:
                    if not isinstance(col, Pawn) and issubclass(type(col),Piece) and col.player != king.player:
                        # print('test',col)
                        if col.movement(king.location):
                            # print('in movement')
                            if col.check_block(king.location,self,test=True):
                                print(f'CHECK on {king} from {col}')
                                checks += 1
                    elif isinstance(col, Pawn) and col.player != king.player:
                        # print('test',col)
                        if (col.location[1] == king.location[1]-1 or col.location[1] == king.location[1]+1):
                            # print('in column attack range')
                            if color == 'white' and col.location[0]+1 == king.location[0]:
                                print(f'CHECK on {king} from {col}')
                                checks += 1
                            elif color == 'black' and col.location[0]-1 == king.location[0]:
                                print(f'CHECK on {king} from {col}')
                                checks += 1

                            

                                
                except Exception as e:
                    print('ERROR',e)
                    
        if checks > 0:
            return True
        else:
            return False

    def checkmate_king(self,color):
        assert color in ('white','black'), 'Must be white or black'
        
        if color == 'white':
            king = self.white_king
        else:
            king = self.black_king

        locations_to_check = []
        for i in (-1,0,1):
            for j in (-1,0,1):
                l = (king.location[0] + i, king.location[1] + j) 
                if l[0] >= 0 and l[0] <= 7 and l[1] >= 0 and l[1] <= 7:
                    locations_to_check.append(j)

        for location in locations_to_check:
            for row in self.grid:
                for piece in row:
                    if piece is None:
                        continue
                    



            


