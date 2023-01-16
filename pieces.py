class Piece: 

    LOCATION_MAPPER = {i:letter for i,letter in enumerate('ABCDEFGH') }

    def __init__(self, name, player, location):
        self.name = name
        assert player in ('white','black'), 'Player must be "white" or "black"'
        self.player = player
        assert (location[0], location[1]) <= (7,7) and (location[0], location[1]) >= (0,0), 'Out of Bounds'
        self.location = location
        self.captured = False 
        self.ever_moved = False


    def __str__(self):
        if self.captured:
            return f'{self.player} {self.name} is captured\n'
        else:
            return f'{self.player} {self.name} at location {self.location}\n'


    def capture(self):
        print(f'{self.name} captured at {self.get_location()}')
        self.location = None 
        self.captured = True

        return self
        

    def get_location(self):
        row = 8 - self.location[0]
        col = self.LOCATION_MAPPER[self.location[1]]
        return(str(row) + col )

    def symbol(self):
        return self.name[0] + self.player[0]

    def manual_mover(self, row, col):
        assert (row,col) != self.location, 'No movement'
        assert row <= 7 and row >= 0 and col <= 7 and col >= 0, 'Out of Bounds'

        prev_loc = self.get_location()

        self.location = (row, col)
        curr_loc = self.get_location()

        if self.ever_moved == False:
            self.ever_moved = True

        print(f'{self.name} from {prev_loc} to {curr_loc}')

    def move(self, target, board):
        if self.movement(target):
            square = self.check_block(target,board)
            if square:
                print('returned check block')
                # print('square')
                board[target[0]][target[1]] = board[self.location[0]][self.location[1]]
                board[self.location[0]][self.location[1]] = None
                self.manual_mover(target[0], target[1])
                
                return square
        else:
            raise ValueError('Not Valid Move!')

    def movement(self,target):
        pass

    def check_block(self,target,board):
        pass
        


class Pawn(Piece):

    def __init__(self, player, location):
        self.promoted = False
        super().__init__('Pawn', player, location)

    def move(self, target, board, capture=0,promotion=None):
        assert capture in [0, -1, 1], 'Capture must be int: 1 (right) or -1 (left) or 0 (No Capture)'

        if capture != 0:
            
            col = self.location[1] + capture
            if self.player == 'white':
                row = self.location[0] - 1
            else:
                row = self.location[0] + 1

            assert target == (row,col), 'Not Valid Move!'

            if board[row][col] is not None:
                captured_piece = board[row][col].capture() 
                if (row == 0 and self.player == 'white') or (row == 7 and self.player == 'black'):
                    assert promotion is not None, 'Must pass promotion class'
                    board[row][col] == self.promote(promotion)
                    print(board[row][col])
                    board[self.location[0]][self.location[1]] = None
                else:
                    board[row][col] = board[self.location[0]][self.location[1]]
                    board[self.location[0]][self.location[1]] = None
                    self.manual_mover(row, col)               
                
                return captured_piece

        else:
            col = self.location[1]
            if self.player == 'white':
                row = self.location[0] - 1
                row2 = self.location[0] - 2
            else:
                row = self.location[0] + 1
                row2 = self.location[0] + 2

            assert target == (row,col) or (self.ever_moved == False and target == (row2,col)), 'Not Valid Move!'

            if board[row][col] is not None:
                raise ValueError('Piece is blocking the way')

            if (row == 0 and self.player == 'white') or (row == 7 and self.player == 'black'):
                assert promotion is not None, 'Must pass promotion class'
                print(promotion(self.player,(row,col)))
                board[row][col] = self.promote(promotion,(row,col))
                print(board[row][col])
                board[self.location[0]][self.location[1]] = None
            else:
                board[target[0]][target[1]] = board[self.location[0]][self.location[1]]
                board[self.location[0]][self.location[1]] = None
                self.manual_mover(row, col)


        return True


    def promote(self,piece,target):
        self.promoted = True
        return piece(self.player,target)

class Queen(Piece):

    def __init__(self,player,location=None):
        if location is None:
            if player == 'white':
                location = (7,3)
            else:
                location = (0,3)
        super().__init__('Queen',player,location)

    def movement(self, target):
        print('check for valid movemnet')
        return (
            target[0] == self.location[0] or 
            target[1] == self.location[1] or
            abs(target[0] - self.location[0]) == abs(target[1] - self.location[1])
        )

    def check_block(self, target, board):
        print('checked for pieces')
        dist_x =  target[0] - self.location[0]
        dist_y =  target[1] - self.location[1]

        if dist_y == 0:
            if dist_x > 0:
                direction = 1
            elif dist_x < 0:
                direction = -1
            else:
                raise ValueError('No Movement') 

            for i in range(direction,dist_x+direction,direction):
                row = self.location[0]+i
                col = target[1]
                print(f'checking: ({row},{col})')
                if board[row][col] is not None:
                    if (row, col) == target and board[row][col].player != self.player:
                        return board[row][col].capture()
                    raise ValueError('Piece is Blocking the Way')
        elif dist_x == 0:
            if dist_y > 0:
                direction = 1
            elif dist_y < 0:
                direction = -1
            else:
                raise ValueError('No Movement') 

            for i in range(direction,dist_y+direction,direction):
                row = target[0]
                col = self.location[1]+i
                print(f'checking: ({row},{col})')
                if board[row][col] is not None:
                    if (row, col) == target and board[row][col].player != self.player:
                        return board[row][col].capture()
                    raise ValueError('Piece is Blocking the Way')
        
        elif abs(dist_x) == abs(dist_y):
            for i in range(1,abs(dist_x)+1):
                if dist_x > 0:
                    if dist_y > 0:
                        row = self.location[0]+i
                        col = self.location[1]+i
                        print(f'checking: ({row},{col})')
                        if board[row][col] is not None:
                            if (row, col) == target and board[row][col].player != self.player:
                                return board[row][col].capture()
                            raise ValueError('Piece is Blocking the Way')
                    else:
                        row = self.location[0]+i
                        col = self.location[1]-i
                        print(f'checking: ({row},{col})')
                        if board[row][col] is not None:
                            if (row, col) == target and board[row][col].player != self.player:
                                return board[row][col].capture()
                            raise ValueError('Piece is Blocking the Way')
                else:
                    if dist_y > 0:
                        row = self.location[0]-i
                        col = self.location[1]+i
                        print(f'checking: ({row},{col})')
                        if board[row][col] is not None:
                            if (row, col) == target and board[row][col].player != self.player:
                                return board[row][col].capture()
                            raise ValueError('Piece is Blocking the Way')
                    else:
                        row = self.location[0]-i
                        col = self.location[1]-i
                        print(f'checking: ({row},{col})')
                        if board[row][col] is not None:
                            if (row, col) == target and board[row][col].player != self.player:
                                return board[row][col].capture()
                            raise ValueError('Piece is Blocking the Way')
        else:
            return ValueError('Coordinates Off')
        
        return True
            


class King(Piece):

    def __init__(self,player,location=None):
        if location is None:
            if player == 'white':
                location = (7,4)
            else:
                location = (0,4)
        super().__init__('King',player,location)


    def movement(self, target):
        return (
            (target[0] == self.location[0] and abs(target[1] - self.location[1]) == 1) or 
            (target[1] == self.location[1] and abs(target[0] - self.location[0]) == 1) or
            (abs(target[0] - self.location[0]) == 1 and abs(target[1] - self.location[1]) == 1)
        )

    def check_block(self, target, board):
        if board[target[0]][target[1]] is not None:
            if board[target[0]][target[1]].player != self.player:
                return board[target[0]][target[1]].capture()
            raise ValueError('Piece is Blocking the Way')
        
        return True



class Rook(Piece):

    def __init__(self,player,location):
        super().__init__('Rook',player,location)


    def movement(self,target):
        return (
            target[0] == self.location[0] or 
            target[1] == self.location[1] 
        )

    def check_block(self, target, board):
        print('checked for pieces')
        dist_x =  target[0] - self.location[0]
        dist_y =  target[1] - self.location[1]

        if dist_y == 0:
            if dist_x > 0:
                direction = 1
            elif dist_x < 0:
                direction = -1
            else:
                raise ValueError('No Movement') 

            for i in range(direction,dist_x+direction,direction):
                row = self.location[0]+i
                col = target[1]
                print(f'checking: ({row},{col})')
                if board[row][col] is not None:
                    if (row, col) == target and board[row][col].player != self.player:
                        return board[row][col].capture()
                    raise ValueError('Piece is Blocking the Way')
        elif dist_x == 0:
            if dist_y > 0:
                direction = 1
            elif dist_y < 0:
                direction = -1
            else:
                raise ValueError('No Movement') 

            for i in range(direction,dist_y+direction,direction):
                row = target[0]
                col = self.location[1]+i
                print(f'checking: ({row},{col})')
                if board[row][col] is not None:
                    if (row, col) == target and board[row][col].player != self.player:
                        return board[row][col].capture()
                    raise ValueError('Piece is Blocking the Way')
        else:
            return ValueError('Coordinates Off')

        return True

class Bishop(Piece):

    def __init__(self,player,location):
        super().__init__('Bishop',player,location)


    def movement(self, target):
        return (
            abs(target[0] - self.location[0]) == abs(target[1] - self.location[1])
        )

    def check_block(self, target, board):
        dist_x =  target[0] - self.location[0]
        dist_y =  target[1] - self.location[1]
        
        if abs(dist_x) == abs(dist_y):
            for i in range(1,abs(dist_x)+1):
                if dist_x > 0:
                    if dist_y > 0:
                        row = self.location[0]+i
                        col = self.location[1]+i
                        print(f'checking: ({row},{col})')
                        if board[row][col] is not None:
                            if (row, col) == target and board[row][col].player != self.player:
                                return board[row][col].capture()
                            raise ValueError('Piece is Blocking the Way')
                    else:
                        row = self.location[0]+i
                        col = self.location[1]-i
                        print(f'checking: ({row},{col})')
                        if board[row][col] is not None:
                            if (row, col) == target and board[row][col].player != self.player:
                                return board[row][col].capture()
                            raise ValueError('Piece is Blocking the Way')
                else:
                    if dist_y > 0:
                        row = self.location[0]-i
                        col = self.location[1]+i
                        print(f'checking: ({row},{col})')
                        if board[row][col] is not None:
                            if (row, col) == target and board[row][col].player != self.player:
                                return board[row][col].capture()
                            raise ValueError('Piece is Blocking the Way')
                    else:
                        row = self.location[0]-i
                        col = self.location[1]-i
                        print(f'checking: ({row},{col})')
                        if board[row][col] is not None:
                            if (row, col) == target and board[row][col].player != self.player:
                                return board[row][col].capture()
                            raise ValueError('Piece is Blocking the Way')
        else:
            return ValueError('Coordinates Off')

        return True


class Knight(Piece):

    def __init__(self,player,location):
        super().__init__('Knight',player,location)

    def movement(self,target):
        return (
            (abs(target[0] - self.location[0]) == 1 and abs(target[1] - self.location[1]) == 2) or
            (abs(target[0] - self.location[0]) == 2 and abs(target[1] - self.location[1]) == 1)
        )

    def check_block(self, target, board):
        if board[target[0]][target[1]] is not None:
            if board[target[0]][target[1]].player != self.player:
                return board[target[0]][target[1]].capture()
            raise ValueError('Piece is Blocking the Way')
        
        return True
        

