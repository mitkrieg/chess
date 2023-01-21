class Piece: 

    LOCATION_MAPPER = {i:letter for i,letter in enumerate('ABCDEFGH') }

    def __init__(self, name, player, location,nickname=''):
        self.name = name
        assert player in ('white','black'), 'Player must be "white" or "black"'
        self.player = player
        self.nickname = str(nickname)
        self.slug = '-'.join([player, name, self.nickname])
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
                print('a returned square')
                # print('square')
                board.grid[target[0]][target[1]] = board.grid[self.location[0]][self.location[1]]
                board.grid[self.location[0]][self.location[1]] = None
                self.manual_mover(target[0], target[1])

                if self.name == 'King':
                    if self.player == 'white':
                        board.white_king = self
                    else:
                        board.black_king = self
                
                return square
        else:
            raise ValueError('Not Valid Move!')

    def movement(self,target):
        pass

    def check_block(self,target,board):
        pass
        


class Pawn(Piece):

    def __init__(self, player, location, nickname=''):
        self.promoted = False
        super().__init__('pawn', player, location,nickname)

    def move(self, target, board, test=None,promotion=None):
        print(board)

        grid = board.grid
            
        col = self.location[1]
        if self.player == 'white':
            row = self.location[0] - 1
            row2 = self.location[0] - 2
        else:
            row = self.location[0] + 1
            row2 = self.location[0] + 2

        # if ((row == 0 and self.player == 'white') or (row == 7 and self.player == 'black')) and target == (row,col):
        #     assert promotion is not None, 'Must pass promotion class'
        #     print(promotion(self.player,(row,col)))
        #     grid[row][col] = self.promote(promotion,(row,col))
        #     # print(grid[row][col])
        #     grid[self.location[0]][self.location[1]] = None
        if target == (row,col+1) or target == (row,col -1):
            if grid[target[0]][target[1]] is not None and grid[target[0]][target[1]].player != self.player:
                if self.ever_moved == False:
                    self.ever_moved = True
                captured_piece = grid[target[0]][target[1]]
                grid[target[0]][target[1]] = grid[self.location[0]][self.location[1]]
                grid[self.location[0]][self.location[1]] = None 
                self.manual_mover(target[0],target[1])
                return captured_piece.capture()
            else:
                print('huh')
                raise ValueError('Not Valid Move!')
        elif (self.ever_moved == False and target == (row2,col)):
            print('INsight clock')
            if grid[row][col] is not None or grid[row2][col] is not None:
                raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
            else:
                if self.ever_moved == False:
                    self.ever_moved = True
                grid[target[0]][target[1]] = grid[self.location[0]][self.location[1]]
                grid[self.location[0]][self.location[1]] = None 
                self.manual_mover(target[0],target[1])
        elif target == (row,col):
            print(row,col)
            print(target)
            if grid[row][col] is not None:
                raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
            else:
                if self.ever_moved == False:
                    self.ever_moved = True
                grid[target[0]][target[1]] = grid[self.location[0]][self.location[1]]
                grid[self.location[0]][self.location[1]] = None 
                self.manual_mover(target[0],target[1])
        else:
            raise ValueError('Not Valid Move!')

        print('\nXXXXAFTER MOVEXXXXX\n')
        print(board)

        return True


    def promote(self,piece,target):
        p = piece(self.player,target)
        self.promoted = True
        print(f'Pawn promoted to {p}')
        
        return p

class Queen(Piece):

    def __init__(self,player,location=None,nickname=''):
        if location is None:
            if player == 'white':
                location = (7,3)
            else:
                location = (0,3)
        super().__init__('queen',player,location,nickname)

    def movement(self, target):
        print('test for valid movemnet')
        return (
            target[0] == self.location[0] or 
            target[1] == self.location[1] or
            abs(target[0] - self.location[0]) == abs(target[1] - self.location[1])
        )

    def check_block(self, target, board, test=False):
        print('test for pieces in the way or captured')
        dist_x =  target[0] - self.location[0]
        dist_y =  target[1] - self.location[1]
        grid = board.grid

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
                print(f'testing: ({row},{col})')
                if grid[row][col] is not None:
                    if (row, col) == target and grid[row][col].player != self.player:
                        if not test:
                            return grid[row][col].capture()
                        else:
                            return True
                    raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
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
                print(f'testing: ({row},{col})')
                if grid[row][col] is not None:
                    if (row, col) == target and grid[row][col].player != self.player:
                        if not test:
                            return grid[row][col].capture()
                        else:
                            return True
                    raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
        
        elif abs(dist_x) == abs(dist_y):
            for i in range(1,abs(dist_x)+1):
                if dist_x > 0:
                    if dist_y > 0:
                        row = self.location[0]+i
                        col = self.location[1]+i
                        print(f'testing: ({row},{col})')
                        if grid[row][col] is not None:
                            if (row, col) == target and grid[row][col].player != self.player:
                                if not test:
                                    return grid[row][col].capture()
                                else:
                                    return True
                            raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
                    else:
                        row = self.location[0]+i
                        col = self.location[1]-i
                        print(f'testing: ({row},{col})')
                        if grid[row][col] is not None:
                            if (row, col) == target and grid[row][col].player != self.player:
                                if not test:
                                    return grid[row][col].capture()
                                else:
                                    return True
                            raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
                else:
                    if dist_y > 0:
                        row = self.location[0]-i
                        col = self.location[1]+i
                        print(f'testing: ({row},{col})')
                        if grid[row][col] is not None:
                            if (row, col) == target and grid[row][col].player != self.player:
                                if not test:
                                    return grid[row][col].capture()
                                else:
                                    return True
                            raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
                    else:
                        row = self.location[0]-i
                        col = self.location[1]-i
                        print(f'testing: ({row},{col})')
                        if grid[row][col] is not None:
                            if (row, col) == target and grid[row][col].player != self.player:
                                if not test:
                                    return grid[row][col].capture()
                                else:
                                    return True
                            raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
        else:
            return ValueError('Coordinates Off')
        
        return True
            


class King(Piece):

    def __init__(self,player,location=None,nickname=''):
        if location is None:
            if player == 'white':
                location = (7,4)
            else:
                location = (0,4)
        super().__init__('king',player,location, nickname)


    def movement(self, target):
        return (
            (target[0] == self.location[0] and abs(target[1] - self.location[1]) == 1) or 
            (target[1] == self.location[1] and abs(target[0] - self.location[0]) == 1) or
            (abs(target[0] - self.location[0]) == 1 and abs(target[1] - self.location[1]) == 1)
        )

    def check_block(self, target, board, test=False):
        grid = board.grid
        if grid[target[0]][target[1]] is not None:
            if grid[target[0]][target[1]].player != self.player:
                if not test:
                    return grid[target[0]][target[1]].capture()
                else:
                    return True
            raise ValueError(f'Piece {grid[target[0]][target[1]]} is Blocking the Way')
        
        return True



class Rook(Piece):

    def __init__(self, player, location, nickname=''):
        super().__init__('rook', player, location, nickname)


    def movement(self,target):
        return (
            target[0] == self.location[0] or 
            target[1] == self.location[1] 
        )

    def check_block(self, target, board, test=False):
        print('checked for pieces')
        dist_x =  target[0] - self.location[0]
        dist_y =  target[1] - self.location[1]
        grid = board.grid

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
                print(f'testing: ({row},{col})')
                if grid[row][col] is not None:
                    if (row, col) == target and grid[row][col].player != self.player:
                        if not test:
                            return grid[row][col].capture()
                        else:
                            return True
                    raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
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
                print(f'testing: ({row},{col})')
                if grid[row][col] is not None:
                    if (row, col) == target and grid[row][col].player != self.player:
                        if not test:
                            return grid[row][col].capture()
                        else:
                            return True
                    raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
        else:
            return ValueError('Coordinates Off')

        return True

class Bishop(Piece):

    def __init__(self,player,location,nickname=''):
        super().__init__('bishop',player,location,nickname)


    def movement(self, target):
        return (
            abs(target[0] - self.location[0]) == abs(target[1] - self.location[1])
        )

    def check_block(self, target, board, test=False):
        dist_x =  target[0] - self.location[0]
        dist_y =  target[1] - self.location[1]
        grid = board.grid
        
        if abs(dist_x) == abs(dist_y):
            for i in range(1,abs(dist_x)+1):
                if dist_x > 0:
                    if dist_y > 0:
                        row = self.location[0]+i
                        col = self.location[1]+i
                        print(f'testing: ({row},{col})')
                        if grid[row][col] is not None:
                            if (row, col) == target and grid[row][col].player != self.player:
                                if not test:
                                    return grid[row][col].capture()
                                else:
                                    return True
                            raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
                    else:
                        row = self.location[0]+i
                        col = self.location[1]-i
                        print(f'testing: ({row},{col})')
                        if grid[row][col] is not None:
                            if (row, col) == target and grid[row][col].player != self.player:
                                if not test:
                                    return grid[row][col].capture()
                                else:
                                    return True
                            raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
                else:
                    if dist_y > 0:
                        row = self.location[0]-i
                        col = self.location[1]+i
                        print(f'testing: ({row},{col})')
                        if grid[row][col] is not None:
                            if (row, col) == target and grid[row][col].player != self.player:
                                if not test:
                                    return grid[row][col].capture()
                                else:
                                    return True
                            raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
                    else:
                        row = self.location[0]-i
                        col = self.location[1]-i
                        print(f'testing: ({row},{col})')
                        if grid[row][col] is not None:
                            if (row, col) == target and grid[row][col].player != self.player:
                                if not test:
                                    return grid[row][col].capture()
                                else:
                                    return True
                            raise ValueError(f'Piece {grid[row][col]} is Blocking the Way')
        else:
            return ValueError('Coordinates Off')

        return True


class Knight(Piece):

    def __init__(self,player,location,nickname=''):
        super().__init__('knight',player,location,nickname)

    def symbol(self):
        return 'n' + self.player[0]

    def movement(self,target):
        return (
            (abs(target[0] - self.location[0]) == 1 and abs(target[1] - self.location[1]) == 2) or
            (abs(target[0] - self.location[0]) == 2 and abs(target[1] - self.location[1]) == 1)
        )

    def check_block(self, target, board, test = False):
        grid = board.grid
        if grid[target[0]][target[1]] is not None:
            if grid[target[0]][target[1]].player != self.player:
                if not test:
                    return grid[target[0]][target[1]].capture()
                else:
                    return True
            raise ValueError(f'Piece {grid[target[0]][target[1]]} is Blocking the Way')
        
        return True
        

