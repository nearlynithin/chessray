class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.moves = []

    def __del__(self):
        # destructor
        pass
    
    # Some methods to be overidden by the classes of each piece
    def move(self,x,y):
        if (x,y) in self.moves:
            self.x = x
            self.y = y
    def get_position(self):
        pass
    def highlight(self):
        pass
    def get_moves(self):
        pass
    
    
class pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.first = True
    
    def move(self,x,y):
        self.moves = self.get_moves()
        super().move(x,y)
        
    def get_moves(self):
        if self.color == "white":
            pass
        if self.color == "black":
            pass