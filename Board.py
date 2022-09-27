from turtle import pos


class Board(object):
    def __init__(self):
        self.empty='.'
        self.board=[['.' for _ in range(8)]for _ in range(8)]
        self.board[3][4]='X'
        self.board[4][3]='X'
        self.board[3][3]='O'
        self.board[4][4]='O'
        self.dirs=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    
    def display(self):
        print(' 0 1 2 3 4 5 6 7')
        board=self.board
        for i in range(8):
            print(str(i)+' '.join(board[i]))
        print('\n')

    def count(self,color):
        count=0
        for x in range(8):
            for y in range(8):
                if self.board[x][y]==color:
                    count+=1
        return count

    def move(self,action,color):
        fliped=self.can_fliped(action,color)
        if fliped:
            for flip in fliped:
                self.board[flip[0]][flip[1]]=color
            
            x,y=action
            self.board[x][y]=color
            return fliped
        else:
            return False

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
                if self.board[x][y]==color:
                    while True:
                        x-=x_direction
                        y-=y_direction
                        if x==x_start and y==y_start:
                            break
                        flipped_pos.append([x,y])
        self.board[x_start][y_start]=self.empty
        if len(flipped_pos)==0:
            return False
        for position in flipped_pos:
            flipped_pos_board.append(position)
        return flipped_pos_board
    def get_legal_actions(self,color):
        ans=[]
        op_color="O" if color=="X" else "X"
        op_color_near_points=[]
        board=self.board
        for i in range(8):
            for j in range(8):
                if board[i][j]==op_color:
                    for dx,dy in self.dirs:
                        x,y=i+dx,j+dy
                        if 0<=x<=7 and 0<=y<=7 and board[x][y]==self.empty and (x,y) not in op_color_near_points:
                            op_color_near_points.append((x,y))
        l=[0,1,2,3,4,5,6,7]
        for p in op_color_near_points:
            if self.can_fliped(p,color):
                if p[0] in l and p[1] in l:
                    ans.append([p[0],p[1]])
        return ans
                
    def backpropagation(self,action,flipped_pos,color):
        self.board[action[0]][action[1]]=self.empty
        op_color="O" if color=="X" else "X"
        for position in flipped_pos:
            self.board[position[0]][position[1]]=op_color
