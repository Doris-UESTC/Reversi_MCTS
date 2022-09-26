from doctest import master
from operator import contains
import time
from http.client import OK
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.messagebox import *
from tokenize import String
from turtle import width
from PIL import Image, ImageTk
from math import *
from enum import Enum
import datetime
from Board import Board
from Game import Game
from MCTS import AIPlayer, HumanPlayer, RoxannePlayer


class ReversiGUI(Frame):
    """黑白棋GUI"""

    def __init__(self, master=None, layoutImages=None):
        super().__init__(master)
        self.master = master
        self.player1 = HumanPlayer("X")
        self.player2 = AIPlayer("O")
        self.game = Game(self.player1, self.player2)
        self.setImages(layoutImages)
        self.newGameStart = True
        self.stepCount = 0
        self.sumStepDealy = 0
        self.selectedPieceValue = tkinter.IntVar()  # 调用get()，值为 1 是黑棋，2 是白棋
        self.superParameter = float("{:0.12f}".format(sqrt(2)/2))
        self.board = Board()
        self.boardCanvas = ""
        self.playMode = PlayMode.NONE
        self.initialLayout()
        self.pack()

    def initialLayout(self):
        """初始化GUI布局"""
        # 棋盘区
        boardFrame = tkinter.Frame(master, bg="#13693B",
                                   width=720, height=720, relief='flat')
        boardFrame.pack(side=tkinter.LEFT)
        self.boardCanvas = tkinter.Canvas(boardFrame, bg="white", width=720,
                                          height=720, borderwidth=-2)

        # 设置区
        settingFrame = tkinter.Frame(
            master, bg="#13693B", width=200, height=720, relief='flat')
        settingFrame.pack(side=tkinter.RIGHT)

        # 设置区-标题-黑白棋
        titleFrame = tkinter.Frame(settingFrame, width=200, height=95)
        titleFrame.pack()

        titleFont = tkFont.Font(family="华文楷体", weight=tkFont.BOLD, size=32)
        titleLabel = tkinter.Label(titleFrame, bg="#DFAD01", text="黑白棋",
                                   font=titleFont, relief="ridge", padx=10)
        titleLabel.pack()

        # 设置区-计数
        countFrame = tkinter.Frame(settingFrame)
        countFrame.pack()

        pieceImage = tkinter.Canvas(countFrame, bg="#13693B", width=200,
                            height=130, borderwidth=-2)
        pieceImage.create_image((60, 55), image=images[0])
        pieceImage.create_image((140, 55), image=images[1])
        pieceImage.pack()

        countLabelFont = tkFont.Font(
            family="微软雅黑", weight=tkFont.BOLD, size=18)
        self.blackCountLabel = tkinter.Label(
            countFrame, bg="#13693B", text="02", font=countLabelFont)
        self.blackCountLabel.place(x=43, y=90)

        colonLabel = tkinter.Label(
            countFrame, bg="#13693B", text=":", font=countLabelFont, foreground="#DFAD01")
        colonLabel.place(x=95, y=88)

        self.whiteCountLabel = tkinter.Label(
            countFrame, bg="#13693B", text="02", font=countLabelFont, foreground="#fff")
        self.whiteCountLabel.place(x=123, y=90)

        # 设置区-游戏模式
        playModeFrame = tkinter.Frame(
            settingFrame, bg="#13693B", width=200, height=138)
        playModeFrame.pack()

        labelFrameFont = tkFont.Font(
            family="微软雅黑", weight=tkFont.BOLD, size=11)
        selectFrame = tkinter.LabelFrame(playModeFrame, text="执棋", bg="#13693B", relief="ridge",
                                         width=150, height=60, font=labelFrameFont, foreground="#fff")
        selectFrame.place(x=23)
        selectPieceFont = tkFont.Font(family="微软雅黑", size=11)
        self.selectBlackRadioBtn = tkinter.Radiobutton(selectFrame, bg="#13693B", text="黑棋", variable=self.selectedPieceValue, value=1,
                                                       font=selectPieceFont, activeforeground="#fff", activebackground="#13693B",
                                                       foreground="#fff", selectcolor="#13693B", highlightbackground="#13693B")
        self.selectBlackRadioBtn.place(x=10, y=0, width=60)
        self.selectWhiteRadioBtn = tkinter.Radiobutton(selectFrame, bg="#13693B", text="白棋", variable=self.selectedPieceValue, value=2,
                                                       font=selectPieceFont, activeforeground="#fff", activebackground="#13693B",
                                                       foreground="#fff", selectcolor="#13693B", highlightbackground="#13693B")
        self.selectWhiteRadioBtn.place(x=80, y=0, width=60)
        self.selectBlackRadioBtn.select()

        buttonFont = tkFont.Font(family="微软雅黑", size=11)
        humanAIButton = tkinter.Button(
            playModeFrame, text="人机战", font=buttonFont, pady=60)
        humanAIButton.place(x=24, y=70, width=72, height=25)
        aiButton = tkinter.Button(
            playModeFrame, text="AI对战", font=buttonFont)
        aiButton.place(x=101, y=70, width=72, height=25)
        newButton = tkinter.Button(playModeFrame, text="新一局", font=buttonFont)
        newButton.place(x=24, y=102, width=149, height=25)

        # 设置区-参数调整
        parameters = tkinter.Frame(
            settingFrame, bg="#13693B", width=200, height=352)
        parameters.pack()
        superParamFrame = tkinter.LabelFrame(parameters, text="超参", bg="#13693B", relief="ridge",
                                             width=150, height=95, font=labelFrameFont, foreground="#fff")
        superParamFrame.place(x=25, y=0)

        self.superParameterText = tkinter.Entry(
            superParamFrame, font=("微软雅黑", 10))
        self.superParameterText.place(x=10, y=5, width=125)
        self.superParameterText["textvariable"] = StringVar(
            self.superParameterText, str(self.superParameter))
        changeSuperParamBtn = tkinter.Button(
            superParamFrame, text="修改", font=buttonFont)
        changeSuperParamBtn.place(x=10, y=36, width=60, height=25)
        restoreSuperParamBtn = tkinter.Button(
            superParamFrame, text="复位", font=buttonFont)
        restoreSuperParamBtn.place(x=76, y=36, width=60, height=25)

        stapDelayFrame = tkinter.LabelFrame(parameters, text="步延", bg="#13693B", relief="ridge",
                                            width=150, height=247, font=labelFrameFont, foreground="#fff")
        stapDelayFrame.place(x=25, y=105)
        self.stepDelayMessage = tkinter.Text(stapDelayFrame, font=("微软雅黑", 10))
        self.stepDelayMessage.place(x=10, y=5, width=125, height=207)
        self.stepDelayMessage.insert("end", "各步延时为：\n")
        self.stepDelayMessage.config(state="disable")

        self.drawAll(board=self.board.board, boardCanvas=self.boardCanvas)

        self.boardCanvas.bind("<Button-1>", self.moveNext)
        self.selectBlackRadioBtn.config(command=self.selectedPieceChanged)
        self.selectWhiteRadioBtn.config(command=self.selectedPieceChanged)
        humanAIButton.config(command=self.humanAIButtonClicked)
        aiButton.config(command=self.aiButtonClicked)
        newButton.config(command=self.newGame)
        changeSuperParamBtn.config(command=self.changeSuperParamBtnClicked)
        restoreSuperParamBtn.config(command=self.restoreSuperParamBtnClicked)

    def game_over(self):
        player1_list = list(self.board.get_legal_actions("X"))
        player2_list = list(self.board.get_legal_actions("O"))
        is_over = len(player1_list) == 0 and len(player2_list) == 0
        return is_over

    def setImages(self, layoutImages):
        """设置图片属性
        : layoutImages：图像列表，列表中依次包含三个图像：黑棋、白棋、棋盘
        """
        self.blackImage = layoutImages[0]
        self.whiteImage = layoutImages[1]
        self.boardImage = layoutImages[2]

    def drawBoard(self, boardCanvas):
        """绘制棋盘"""
        boardCanvas.create_image((360, 360), image=self.boardImage)
        boardCanvas.pack()

    def drawAll(self, board, boardCanvas):
        """绘制棋子棋盘"""
        self.drawBoard(boardCanvas=boardCanvas)
        for x in range(8):
            for y in range(8):
                if board[x][y] == "X":
                    boardCanvas.create_image((y*80+80, x*80+80),
                                             image=self.blackImage)
                    boardCanvas.pack()
                elif board[x][y] == "O":
                    boardCanvas.create_image((y*80+80, x*80+80),
                                             image=self.whiteImage)
                    boardCanvas.pack()
        
        self.boardCanvas.update_idletasks()
        if self.game_over() == True:
            self.stepDelayMessage.config(state="normal")
            self.stepDelayMessage.insert(
                "end", "总时延：" + str(self.sumStepDealy) + "ms")
            self.stepDelayMessage.config(state="disable")
            self.gameOverMessage()

    def AIGo(self, color):
        # time.sleep(0.5)
        if self.newGameStart == True:
            return
        if self.playMode == PlayMode.HUMANVSAI and len(list(self.board.get_legal_actions(color))) == 0 and self.game_over() == False:
            if color == "X":
                messagebox.showinfo("说明", "黑棋无子可下，请白棋继续落子。")
            else:
                messagebox.showinfo("说明", "白棋无子可下，请黑棋继续落子。")
            self.stepCount = self.stepCount - 1
            return
        startTime = datetime.datetime.now()
        if color == "X":
            enemyColor = "O"
            action = self.player1.get_move(self.board)
            self.board.move(action, "X")
        else:
            enemyColor = "X"
            action = self.player2.get_move(self.board)
            self.board.move(action, "O")
        self.blackCountLabel['text'] = "{:0>2}".format(
            str(self.board.count("X")))
        self.whiteCountLabel['text'] = "{:0>2}".format(
            str(self.board.count("O")))
        overTime = datetime.datetime.now()
        timeConsuming = int((overTime-startTime).microseconds / 1000)
        self.printStepDealayMessage(timeConsuming=timeConsuming)
        self.sumStepDealy = self.sumStepDealy + timeConsuming
        self.drawAll(board=self.board.board, boardCanvas=self.boardCanvas)
        while self.playMode == PlayMode.HUMANVSAI and len(list(self.board.get_legal_actions(enemyColor))) == 0 and self.game_over() == False:
            if enemyColor == "X":
                messagebox.showinfo("说明", "黑棋无子可下，白棋将继续落子。")
            else:
                messagebox.showinfo("说明", "白棋无子可下，黑棋将继续落子。")
            self.stepCount = self.stepCount + 1
            self.AIGo(color)

    def judgeLegal(self, ans, location):
        """判断落子是否合法"""
        if location in ans:
            return True
        messagebox.showerror("警告", "棋子位置不合法，请重新选择落子位置！")
        return False

    def judgePlayMode(self):
        """判断对战模式"""
        if self.playMode == PlayMode.NONE:
            messagebox.showwarning("警告", "请选择执棋和对战模式！")
            return False
        return True

    def gameOverMessage(self):
        """游戏结束提示信息"""
        blackCount = self.board.count("X")
        whiteCount = self.board.count("O")
        if blackCount > whiteCount:
            resultStr = "黑棋胜利！"
        elif blackCount < whiteCount:
            resultStr = "白棋胜利！"
        elif blackCount == whiteCount:
            resultStr = "平局！"
        result = messagebox.askyesno(
            "游戏结束", "本局游戏已结束，" + resultStr + "\n是否开始新一局？")
        if result == True:
            self.newGame()

    def moveNext(self, event):
        """下棋"""
        if self.playMode == PlayMode.AIVSAI:
            return
        if self.judgePlayMode() == False:
            return
        if self.game_over() == True:
            self.gameOverMessage()
            return
        col = int((event.x - 40) / 80)
        row = int((event.y - 40) / 80)
        if row > 7 or col > 7:
            return
        ans = self.board.get_legal_actions(
            "O" if self.selectedPieceValue.get() == 2 else "X")
        if self.judgeLegal(ans, [row, col]) == False:
            return
        if self.board.board[row][col] == ".":
            self.stepCount = self.stepCount + 1
            if self.selectedPieceValue.get() == 1:
                self.board.move([row, col], "X")
                self.drawAll(board=self.board.board,
                             boardCanvas=self.boardCanvas)
                self.AIGo("O")
            else:
                self.board.move([row, col], "O")
                self.drawAll(board=self.board.board,
                             boardCanvas=self.boardCanvas)
                self.AIGo("X")
            self.blackCountLabel['text'] = "{:0>2}".format(str(self.board.count("X")))
            self.whiteCountLabel['text'] = "{:0>2}".format(str(self.board.count("O")))

    def printStepDealayMessage(self, timeConsuming):
        """打印每一步时延"""
        message = "第 " + \
            "{:0>2}".format(str(self.stepCount)) + " 步：" + \
            str(timeConsuming) + "ms\n"
        self.stepDelayMessage.config(state="normal")
        self.stepDelayMessage.insert("end", message)
        self.stepDelayMessage.config(state="disable")
        self.stepDelayMessage.see("end")

    def selectedPieceChanged(self):
        """执棋"""
        if self.selectedPieceValue.get() == 1:
            messagebox.showinfo(title="执棋", message="已选择黑棋，请开始游戏！")
        else:
            messagebox.showinfo(title="执棋", message="已选择白棋，请开始游戏！")

    def newGame(self):
        """新一局"""
        self.newGameStart = True
        if self.selectedPieceValue.get() == 1:
            self.selectWhiteRadioBtn.config(state="active")
        else:
            self.selectBlackRadioBtn.config(state="active")
        if self.board.count("X") == 2 and self.board.count("O") == 2:
            self.superParameter = float("{:0.12f}".format(sqrt(2)/2))
            self.superParameterText["textvariable"] = StringVar(
                self.superParameterText, str(self.superParameter))
            getNewGame = messagebox.showwarning(
                title="警告", message="当前已是新局！")
            return
        else:
            self.playMode = PlayMode.NONE
            self.stepCount = 0
            self.player1 = HumanPlayer("X")
            self.player2 = AIPlayer("O")
            self.game = Game(self.player1, self.player2)
            self.blackCountLabel["text"] = "02"
            self.whiteCountLabel["text"] = "02"
            self.boardCanvas.delete(tkinter.ALL)
            self.board = Board()
            self.drawAll(self.board.board, self.boardCanvas)
            self.stepDelayMessage.config(state="normal")
            self.stepDelayMessage.delete("1.0", "end")
            self.stepDelayMessage.insert("end", "各步延时为：\n")
            self.stepDelayMessage.config(state="disable")

    def changeSuperParamBtnClicked(self):
        """修改超参数"""
        tempSuperParameter = float(self.superParameterText.get())
        if tempSuperParameter == self.superParameter:
            return
        self.superParameter = tempSuperParameter
        messagebox.showinfo("超参设置", "超参数已修改为 " +
                            str(self.superParameter) + " ！")

    def restoreSuperParamBtnClicked(self):
        """复位超参"""
        if self.superParameter == float("{:0.12f}".format(sqrt(2)/2)):
            return
        self.superParameter = float("{:0.12f}".format(sqrt(2)/2))
        self.superParameterText["textvariable"] = StringVar(
            self.superParameterText, str(self.superParameter))
        messagebox.showinfo("超参设置", "超参数已复位为 " +
                            str(self.superParameter) + " ！")

    def humanAIButtonClicked(self):
        """人机战按钮点击事件"""
        self.newGameStart = False
        messagebox.showinfo("人机战", "当前模式为人机战")
        self.playMode = PlayMode.HUMANVSAI
        if self.selectedPieceValue.get() == 1:
            self.selectWhiteRadioBtn.config(state="disable")
            self.player1 = HumanPlayer("X")
            self.player2 = AIPlayer("O")
        else:
            self.stepCount = self.stepCount + 1
            self.selectBlackRadioBtn.config(state="disable")
            self.player1 = AIPlayer("X")
            self.player2 = HumanPlayer("O")
            self.AIGo("X")

    def aiButtonClicked(self):
        """人机战按钮点击事件"""
        self.newGameStart = False
        self.playMode = PlayMode.AIVSAI
        messagebox.showinfo("AI对战", "当前模式为AI对战")
        self.player1 = AIPlayer("X")
        self.player2 = AIPlayer("O")
        while self.game_over() == False:
            self.stepCount = self.stepCount + 1
            self.AIGo("X")
            self.stepCount = self.stepCount + 1
            self.AIGo("O")


class PlayMode(Enum):
    HUMANVSAI = 1
    AIVSAI = 2
    NONE = 3


def resizeImage(width, height, imagePath):
    """重设图像大小"""
    img = Image.open(imagePath)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)


if __name__ == "__main__":
    """初始化"""
    root = Tk()
    root.title("黑白棋")
    root.geometry("920x720+200+50")
    root.config(bg="#13693B")
    root.resizable(width=False, height=False)

    # 加载图片资源
    images = [resizeImage(60, 60, "./images/black-3d.png"),
              resizeImage(60, 60, "./images/white-3d.png"),
              resizeImage(720, 720, "./images/board-grayline.png"),
              resizeImage(720, 720, "./images/board-blackline.png"),
              resizeImage(720, 720, "./images/board-whiteline.png"),
              resizeImage(20, 20, "./images/icon.png")]

    # 设置窗体图标
    root.iconphoto(FALSE, images[5])

    layoutImages = [images[0], images[1], images[2]]
    reversiGUI = ReversiGUI(master=root, layoutImages=layoutImages)

    root.mainloop()
