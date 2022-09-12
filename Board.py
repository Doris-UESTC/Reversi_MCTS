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

    def count(self,color):
        count=0
        for x in range(8):
            for y in range(8):
                if self.board[x][y]==color:
                    count+=1
        return count

    def get_winner(self):
        player1_count=self.count('X')
        player2_count=self.count('O')
        if player1_count>player2_count:
            return 0,player1_count-player2_count
        elif player1_count<player2_count:
            return 1,player2_count-player1_count
        elif player1_count==player2_count:
            return 2,0

    def is_on_board(self,x,y):
        return x>=0 and x<8 and y>=0 and y<8
    
    def can_fliped(self,action,color):
        x_start,y_start=action
        if not self.is_on_board(x_start,y_start) or self.board[x_start][y_start]!=self.empty:
            return False
        self.board[x_start][y_start]=color
        op_color="X" if color=="O" else "O"
        flipped_pos=[]
        flipped_pos_board=[]
        for x_direction,y_direction in self.dirs:
            x,y=x_start,y_start
            x+=x_direction
            y+=y_direction
            if self.is_on_board(x,y) and self.board[x][y]==op_color:
                x+=x_direction
                y+=y_direction
                if not self.is_on_board(x,y):
                    continue
                while self.board[x][y]==op_color:
                    x+=x_direction
                    y+=y_direction
                    if not self.is_on_board(x,y):
                        break
                if not self.is_on_board(x,y):
                    continue

    def get_legal_actions(self,color):
        
    def backpropagation():