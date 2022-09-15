from copy import deepcopy
from Board import Board
class Game(object):
    def __init__(self,player1,player2):
        self.board=Board()
        self.current_player=None
        self.player1=player1
        self.player2=player2
        self.player1.color="X"
        self.player2.color="O"
    
    def switch_player(self):
        if self.current_player is None:
            return self.player1
        else:
            if self.current_player==self.player1:
                return self.player2
            else:
                return self.player1

    def force_loss(self,is_board=False,is_legal=False):
        if self.current_player==self.player1:
            win_color="O"
            loss_color="X"
            winner=2
        else:
            win_color="X"
            loss_color="O"
            winner=1
        diff=0
        return winner,diff

    def run(self):
        winner=None
        diff=-1
        self.board.display()
        while True:
            self.current_player=self.switch_player()
            color="X" if self.current_player==self.player1 else "O"
            legal_actions=list(self.board.get_legal_actions(color))
            if len(legal_actions)==0:
                if self.game_over():
                    winner,diff=self.board.get_winner()
                    break
                else:
                    continue
            board=deepcopy(self.board.board)
            action=self.current_player.get_action(board)
            if action is None:
                continue
            else:
                self.board.move(action,color)
                board.board.display()
                if self.game_over():
                    winner,diff=self.board.get_winner()
                    break
        self.board.display()
        self.print_winner(winner)
        if winner is not None and diff>-1:
            result={0:'player1_win',1:'player2_win',2:'draw'}[winner]

    def game_over(self):
        player1_list=list(self.get_legal_actions("X"))
        player2_list=list(self.get_legal_actions("O"))
        is_over=len(player1_list)==0 and len(player2_list)==0
        return is_over

    
    
    
    

