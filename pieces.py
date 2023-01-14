class Piece: 

    LOCATION_MAPPER = {i:letter for i,letter in enumerate('ABCDEFGH') }

    def __init__(self, name, player, location):
        self.name = name
        assert player in ('white','black'), 'Player must be "white" or "black"'
        self.player = player
        assert (location[0], location[1]) <= (7,7) and (location[0], location[1]) >= (0,0), 'Out of Bounds'
        self.location = location
        self.captured = False 


    def capture(self):
        self.location = None 
        self.captured = True

    def get_location(self):
        row = 8 - self.location[0]
        col = self.LOCATION_MAPPER[self.location[1]]
        return(str(row) + col )

    def manual_mover(self, row, col):
        assert (row,col) != self.location, 'No movement'
        assert row <= 7 and row >= 0 and col <= 7 and col >= 0, 'Out of Bounds'

        prev_loc = self.get_location()

        self.location = (row, col)
        curr_loc = self.get_location()

        return f'{self.name} from {prev_loc} to {curr_loc}'
        


class Pawn(Piece):

    def __init__(self, player, location):
        super().__init__('Pawn', player, location)

    def move(self, capture=None):
        assert capture in [None, -1, 1], 'Capture must be int: 1 (right) or -1 (left)'
        if capture is not None:
            
            col = self.location[0] + capture
            if self.player == 'white':
                row = self.location[1] - 1
            else:
                row = self.location[1] + 1

        else:
            if self.player == 'white':
                row = self.location[1] - 1
            else:
                row = self.location[1] + 1

        return self.manual_mover(row, col)

    def promote(self):
        q =  Queen(self.player())

class Queen(Piece):

    def __init__(self,player):
        if player == 'white':
            super().__init__('Queen',player,(7,3))
        else:
            super().__init__('Queen',player,(0,3))

    def move(self, target):
        if (
            target[0] == self.location[0] or 
            target[1] == self.location[1] or
            abs(target[0] - self.location[0]) == abs(target[1] - self.location[1])
        ):
            return self.manual_mover(target[0], target[1])
        else:
            raise ValueError('Not Valid Move!')

class King(Piece):

    def __init__(self,player):
        if player == 'white':
            super().__init__('Queen',player,(7,4))
        else:
            super().__init__('Queen',player,(0,4))


    def move(self, target):
        if (
            (target[0] == self.location[0] and abs(target[1] - self.location[1]) == 1) or 
            (target[1] == self.location[1] and abs(target[0] - self.location[0]) == 1) or
            (abs(target[0] - self.location[0]) == 1 and abs(target[1] - self.location[1]) == 1)
        ):
            return self.manual_mover(target[0], target[1])
        else:
            raise ValueError('Not Valid Move!')


class Rook(Piece):

    def __init__(self,player,location):
        if player == 'white':
            super().__init__('Rook',player,location)
        else:
            super().__init__('Rook',player,location)


    def move(self, target):
        if (
            target[0] == self.location[0] or 
            target[1] == self.location[1] 
        ):
            return self.manual_mover(target[0], target[1])
        else:
            raise ValueError('Not Valid Move!')

class Bishop(Piece):

    def __init__(self,player,location):
        if player == 'white':
            super().__init__('Bishop',player,location)
        else:
            super().__init__('Bishop',player,location)


    def move(self, target):
        if (
            abs(target[0] - self.location[0]) == abs(target[1] - self.location[1])
        ):
            return self.manual_mover(target[0], target[1])
        else:
            raise ValueError('Not Valid Move!')

class Knight(Piece):

    def __init__(self,player,location):
        if player == 'white':
            super().__init__('Knight',player,location)
        else:
            super().__init__('Knight',player,location)

    def move(self,target):
        if (
            (abs(target[0] - self.location[0]) == 1 and abs(target[1] - self.location[1]) == 2) or
            (abs(target[0] - self.location[0]) == 2 and abs(target[1] - self.location[1]) == 1)
        ):
            return self.manual_mover(target[0],target[1])
        else:
            raise ValueError('Not Valid Move!')
        

