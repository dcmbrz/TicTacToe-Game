from cProfile import label
from sqlite3 import connect
from telnetlib import GA
import tkinter as tk
import socket 
from tkinter import W, Label, ttk
from tkinter import messagebox as mb
from GUIBoard import BoardGame
from PIL import ImageTk,Image

'''This is the player1 which is waiting for the connection(server)
this is the first moduel that needs to be ran
must either be ran in the command promt first while Player2 is ran regularly or visversa
first enter in "localhost" next enter in the port number(can be any number in a specific range but we will use 5670) '''
class Player1():
    def __init__(self):
        self.canvasCreate()
        self.s= None
        self.ReceiveName()
        self.Player2= None

#creating the body and canvas
    def canvasCreate(self):
        self.root= tk.Tk()
        self.canvas= tk.Canvas(self.root, height= 1000, width= 1000)
        self.canvas.pack()
        self.root.title("Michael's TicTacToe Program")
        self.root.iconbitmap('C:\\Users\\Miekw\\Downloads\\Python 3.11\\python projects(protfolio stuff)\\lab4(original)\\tictactoe. icon2.jpg')
        self.frame= tk.Frame(self.canvas, bg="white")
        self.frame.place(relheight= 0.8, relwidth= 0.8, relx= 0.1, rely= 0.1)
        self.Lable1= tk.Label(self.frame, text= "Enter IP Info")
        self.Lable1.pack()
        self.HostInfo= tk.Entry(self.frame)
        self.HostInfo.pack()
        self.HostInfo.insert(0, 'localhost') #automatically has the host info inserted
        self.Lable2= tk.Label(self.frame, text= "Enter Your Port Info")
        self.Lable2.pack()
        self.PortInfo= tk.Entry(self.frame, text='Please Enter Your Port Info')
        self.PortInfo.pack()
        self.PortInfo.insert(0, "5670") #automatically has the port info inserted
        self.Lable3= tk.Label(self.frame, text= "Would you like to send your username?")
        self.Lable3.pack()
        self.UserInfo= tk.Entry(self.frame)
        self.UserInfo.pack()
        self.ConnButton= tk.Button(self.frame, text= "Connect", command= lambda:[GameStart(self), self.GetConnected()]) 
        self.ConnButton.pack()
        self.Image1 = ImageTk.PhotoImage(Image.open('C:\\Users\\Miekw\\Downloads\\Python 3.11\\python projects(protfolio stuff)\\lab4(original)\\tictactoe2 gif(lab4).gif'))
        self.game_image = Label(self.frame, image= self.Image1)
        self.game_image.pack()
        self.root.mainloop()
    

#creating a socket:
    def GetConnected(self):
        Connected= True
        count= 0
        p= int(self.PortInfo.get())
        h= str(self.HostInfo.get())
        while Connected:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((h, p))
            self.s.listen(1)
            #Player info:
            username= self.UserInfo.get()
            self.conn, addr= self.s.accept()
            self.conn.sendall(username.encode())
            self.Player2= self.conn.recv(1024).decode()
            print('this is:', self.Player2)
            print('Waiting for connection....')
            self.root.destroy()  
        return self.conn

    def username(self):
        Pusername= self.UserInfo.get()
        return Pusername

    def ReceiveName(self, name):
        for i in name:
            if name.isalnum():
                GameStart()
                return True
        return True

def GameStart(p):
    p= GUI(p)
    

class GUI(Player1):
    def __init__(self, Player):
        self.canvasCreate()
        self.oppenent = Player1
        self.P1U= None
        self.Board()
        self.player= Player #the parameter holding the socket 
        self.gameBoard= BoardGame('Player1', 'Player1','x','o', 0, 0,0)
        self.Wins()
       

    def canvasCreate(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height= 1000, width= 1000)
        self.canvas.grid()
        self.game_status = Label(self.root, text = "game: 1")
        self.game_status.grid(row=3, column=0, columnspan=3)
        #self.game_opp = Label(self.root, text = "game:" + self.oppenent.Player2)
        #elf.game_opp.grid(row=3, column=1, columnspan=3)
        self.Image1 = ImageTk.PhotoImage(Image.open('C:\\Users\\Miekw\\Downloads\\Python 3.11\\python projects(protfolio stuff)\\lab4(original)\\tictactoe gif(lab4).gif'))
        self.game_image = Label(image= self.Image1)
        self.game_image.pack()
        self.root.title("TicTacToe Program X-side")
        
    def Board(self):
        #button creation
        self.frame= tk.Frame(self.canvas, bg="black")
        self.frame.grid(row=10 , column= 10)
        self.root.geometry('500x500')
        b1= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(0,0)])
        b1.grid(row=0, column=0)
        b2= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(0,1)])
        b2.grid(row=0, column=1)
        b3= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(0,2)])
        b3.grid(row=0, column=2)
        b4= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(1,0)])
        b4.grid(row=1, column=0)
        b5= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(1,1)])
        b5.grid(row=1, column=1)
        b6= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(1,2)])
        b6.grid(row=1, column=2)
        b7= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(2,0)])
        b7.grid(row=2, column=0)
        b8= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(2,1)])
        b8.grid(row=2, column=1)
        b9= tk.Button(self.frame, text='', height= 3, width= 6, command=lambda:[self.mark(2,2)])
        b9.grid(row=2, column=2)
        self.button= [[b1,b2,b3],[b4,b5,b6],[b7,b8,b9]]
        
        
    def mark(self, row, col):
        self.button[row][col]['text']= 'x'
        self.gameBoard.updateGameBoard(row, col, 'x')
        print(self.gameBoard.board)
        sendm= self.player.conn.sendall((str(row) + str(col)).encode())
        if self.Wins() == True:
            return 
        self.root.update()
        mark= self.player.conn.recv(1024).decode()
        print('sent:', row, col)
        print('row and col:', mark)
        row= int(mark[0])
        col= int(mark[1])
        self.button[row][col]['text']= 'o'
        self.gameBoard.updateGameBoard(row, col, 'o')
        if self.Wins() == True:
            return 

    def Wins(self):
        if self.gameBoard.isWinner() == True:
            self.gameBoard.GPlayed +=1
            print('games played:', self.gameBoard.GPlayed)
            res=mb.askquestion('Winner!!!', 'Do you really want to play again?')
            if res == 'yes' :
                msg= self.player.conn.sendall('yes'.encode())
                self.gameBoard.resetGameBoard()
                for i in range(0,3):
                    for j in range(0,3):
                        self.button[i][j]['text']= ''
                self.root.update()
                return True
            else :
                msg= self.player.conn.sendall('no'.encode()) 
                self.stats()
                print('status:', self.gameBoard.printStats())
                self.root.destroy()
        return False


if __name__ == "__main__":
    P = Player1()
    GameStart(P)
    print('PLAYER2:, self.Player.2')
   