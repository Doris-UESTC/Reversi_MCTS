import copy
import math
import random

from Board import Board

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
        cnt_max=len(list(self.satte.get_legal_actions(self.color)))
        cnt_now=len(self.children)
        if cnt_max<=cnt_now:
            return True
        else:
            return False

class AIPlayer:
    def __init__(self,color):
        self.color=color

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
            if(len)
