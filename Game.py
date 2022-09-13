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
    
        

    def game_over(self):
        player1_list=list(self.get_legal_actions("X"))
        player2_list=list(self.get_legal_actions("O"))
        is_over=len(player1_list)==0 and len(player2_list)==0
        return is_over

    
    
    

