import copy
import math
import random
from secrets import choice
from turtle import color

from Board import Board
class RandomPlayer:
    def __init__(self,color):
        self.color=color
    
    def random_choice(self,board):
        action_list=list(board.get_legal_actions(self.color))
        if len(action_list)==0:
            return None
        else:
            return random.choice(action_list)
        
    def get_move(self,board):
        if self.color=='X':
            player_name="player1"
        else:
            player_name="player2"
        action=self.random_choice(board)
        return action

class HumanPlayer:
    def __init__(self,color):
        self.color=color
    def get_move(self,board):
        if self.color=="X":
            player="player1"
        else:
            player="player2"
        while True:
            action=[]
            m, n = map(int, input().split())
            action.append(m)
            action.append(n)
            print(board.get_legal_actions(self.color))
            if action == "Q" or action == 'q':
                return "Q"
            else:
                row, col = int(action[1]), int(action[0])
                if row in [0,1,2,3,4,5,6,7] and col in [0,1,2,3,4,5,6,7]:
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("你的输入不合法，请重新输入!")
class Node:
    def __init__(self,state,color,parent=None,action=None):
        self.visit=0
        self.player1_value=0
        self.player2_value=0
        self.reward=0.0
        self.state=state
        self.parent=parent
        self.children=[]
        self.action=action
        self.color=color
    
    def add_child(self,new_state,action,color):
        child_node=Node(new_state,color,self,action)
        self.children.append(child_node)

    def if_fully_expand(self):
        cnt_max=len(list(self.state.get_legal_actions(self.color)))
        cnt_now=len(self.children)
        if cnt_max<=cnt_now:
            return True
        else:
            return False

class AIPlayer:
    def __init__(self,color):
        self.color=color
        self.d={}
        self.roxanne_table = [[[0, 0], [7, 0], [0, 7], [7, 7]], [[2, 2], [5, 2], [2, 5], [5, 5]], [[2, 3], [5, 3], [2, 4], [5, 4], [3, 2], [4, 2], [3, 5], [4, 5]], [[0, 2], [7, 2], [0, 5], [7, 5], [2, 0], [5, 0], [2, 7], [5, 7]], [[0, 3], [7, 3], [0, 4], [7, 4], [3, 0], [4, 0], [3, 7], [4, 7]], [[1, 2], [6, 2], [1, 5], [6, 5], [2, 1], [5, 1], [2, 6], [5, 6]], [[1, 3], [6, 3], [1, 4], [6, 4], [3, 1], [4, 1], [3, 6], [4, 6]], [[1, 1], [6, 1], [1, 6], [6, 6]], [[0, 1], [7, 1], [0, 6], [7, 6], [1, 0], [6, 0], [1, 7], [6, 7]]]
        count=0
        for t in self.roxanne_table:
            count+=1
            for num in t:
                self.d[num[0],num[1]]=count
    def if_terminal(self,state):
        action_player1=list(state.get_legal_actions("X"))
        action_player2=list(state.get_legal_actions("O"))
        if len(action_player1)==0 and len(action_player2)==0:
            return True
        else:
            return False
    
    def backpropagate(sel,node,player1_val,player2_val):
        while node is not None:
            node.visit+=1
            node.player1_value+=player1_val
            node.player2_value+=player2_val
            node=node.parent
        return 0

    def reverse_color(self,color):
        return 'O' if color=='X' else 'X'

    def stimulate_policy(self,node):
        board=copy.deepcopy(node.state)
        color=copy.deepcopy(node.color)
        cnt=0
        while not self.if_terminal(board):
            actions=list(node.state.get_legal_actions(color))
            if len(actions)==0:
                color=self.reverse_color(color)
            else:
                action=random.choice(actions)
                board.move(action,color)
                color=self.reverse_color(color)
            cnt+=1
            if cnt>20:
                break
        return board.count('X'),board.count('O')
    
    def ucb(self,node,uct_scalar=1.0):
        max=-float('inf')
        max_set=[]
        for c in node.children:
            exploit=0
            if c.color=='O':
                exploit=c.player1_value/(c.player1_value+c.player2_value)
            else:
                exploit=c.player1_value/(c.player1_value+c.player2_value)
            explore=math.sqrt(2*math.log(node.visit)/float(c.visit))
            uct_score=exploit+explore*uct_scalar
            if uct_score==max:
                max_set.append(c)
            elif uct_score>max:
                max_set=[c]
                max=uct_score
        sum=[t.action for t in max_set]
        print(sum)
        if len(max_set)==0:
            return node.parent
        else:
            return random.choice(max_set)
    
    def expand(self,node):
        actions_legal=list(node.state.get_legal_actions(node.color))
        actions_already=[c.action for c in node.children]
        action=random.choice(actions_legal)
        while action in actions_already:
            action=random.choice(actions_legal)
        new_state=copy.deepcopy(node.state)
        new_state.move(action,node.color)
        new_color=self.reverse_color(node.color)
        node.add_child(new_state,action=action,color=new_color)
        return node.children[-1]

    def select_policy(self,node):
        while(not self.if_terminal(node.state)):
            if len(list(node.state.get_legal_actions(node.color)))==0:
                return node
            elif not node.if_fully_expand():
                new_node=self.expand(node)
                return new_node
            else:
                node=self.ucb(node)
        return node

    def MCTS_search(self,root,maxt=100):
        for t in range(maxt):
            leave=self.select_policy(root)
            player1_count,player2_count=self.stimulate_policy(leave)
            self.backpropagate(leave,player1_count,player2_count)
        return self.ucb(root).action

    def get_move(self,board):
        if self.color=='X':
            player_name='player1'
        else:
            player_name='player2'
        action=None
        root_board=copy.deepcopy(board)
        root=Node(state=root_board,color=self.color)
        action=self.MCTS_search(root)
        return action

class RoxannePlayer(object):

    def __init__(self, color):
        self.roxanne_table = priority_table = [[[0, 0], [0, 7], [7, 0], [7, 7]],
                  [[0, 2], [0, 5], [2, 0], [5, 0], [2, 7], [5, 7], [7, 2], [7, 5]],
                  [[2, 2], [2, 5], [5, 2], [5, 5]],
                  [[3, 0], [4, 0], [0, 3], [0, 4], [7, 3], [7, 4], [3, 7], [4, 7]],
                  [[3, 2], [4, 2], [2, 3], [2, 4], [3, 5], [4, 5], [5, 3], [5, 4]],
                  [[3, 3], [4, 4], [3, 4], [4, 3]],
                  [[1, 3], [1, 4], [3, 1], [4, 1], [6, 3], [6, 4], [3, 6], [4, 6]],
                  [[1, 2], [1, 5], [2, 1], [5, 1], [6, 2], [6, 5], [2, 6], [5, 6]],
                  [[0, 1], [0, 6], [7, 1], [7, 6], [1, 0], [6, 0], [1, 7], [6, 7]],
                  [[1, 1], [6, 6], [1, 6], [6, 1]]]
        self.color = color

    def roxanne_select(self, board):

        action_list = list(board.get_legal_actions(self.color))
        if len(action_list) == 0:
            return None
        else:
            for move_list in self.roxanne_table:
                random.shuffle(move_list)
                for move in move_list:
                    if move in action_list:
                        return move

    def get_move(self, board):

        if self.color == 'X':
            player_name = 'player1'
        else:
            player_name = 'player2'
        # print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        action = self.roxanne_select(board)
        return action


