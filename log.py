import chess
import pieces



class Action:
    color = ''
    
    def __init__(self, action):
        self.action = action
        self.origin = self.action[:2]
        self.destination = self.action[2:]

    def __str__(self):
        return self.action


class ActionLog:
    def __init__(self):
        self.log = list()
        
    def __len__(self):
        return len(self.log)
    
    def __str__(self):
        return str([str(i) for i in self.log])
    
    def append(self, new_action : Action):
        self.log.append(new_action)

    def toBoard(self) -> chess.Board:
        newBoard = chess.Board(8, 8)
        for i in self.log:
            x1, y1 = newBoard.getIndexFromCoordinate(i.origin)
            x2, y2 = newBoard.getIndexFromCoordinate(i.destination)
            newBoard.move((y1, x1), (y2, x2))
        return newBoard


if __name__ == '__main__':
    print('Unit Test')
    log = ActionLog()
    log.append(Action('c2c4'))
    log.append(Action('g8f6'))
    log.append(Action('b1c3'))
    b = chess.Board(8, 8)
    testBoard : chess.Board = log.toBoard()
    print('testBoard ---> ', type(testBoard))
    print(testBoard.toString())

    assert isinstance(testBoard.getElementFromCoordinate('c2'), int), 'Test 1 failed -- \'c2\' should be 0, instead got %s' %testBoard.getElementFromCoordinate('c2')
    assert isinstance(testBoard.getElementFromCoordinate('c4'), pieces.Piece), 'Test 2 failed -- \'c4\' should be of type chess.pieces.Piece, instead got %s' %testBoard.getElementFromCoordinate('c4') 