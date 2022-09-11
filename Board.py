class Board(object):
    def __init__(self):
        self.empty='.'
        self.board=[[self.empty for _ in range(8)]for _ in range(8)]
        self.board[3][4]='X'
        self.board[4][3]='X'
        self.board[3][3]='O'
        self.board[4][4]='O'
        self.dirs=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    def __getitem__(self,index):
        return self.board[index]
    
    def display(self):
        print()

    def is_on_board(self,x,y):
        return x>=0 and x<8 and y>=0 and y<8
    
    def can_fliped():

    def get_legal_actions(self,color):

    def 