from Game import Game
from MCTS import AIPlayer, HumanPlayer,RoxannePlayer
from Board import Board
#player1=RoxannePlayer("X")
#player2=RoxannePlayer("O")
#player1=RoxannePlayer("X")
#player2=HumanPlayer("O")
#game=Game(player1,player2)
#game.run()
win1=0
win2=0
win3=0
for i in range(100):
    player1=RoxannePlayer("X")
    player2=RoxannePlayer("O")
    #player1=RoxannePlayer("X")
    #player2=HumanPlayer("O")
    game=Game(player1,player2)
    who=game.run()
    if who==0:
        win1+=1
    elif who==1:
        win2+=1
    else:
        win3+=1    
    print(win1)
    print(win2)
    print(win3)

