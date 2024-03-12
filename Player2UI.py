from cProfile import label
from sqlite3 import connect
import tkinter as tk
import socket 
from tkinter import messagebox as mb
from GUIBoard import BoardGame

'''This is the player2 which is connecting(client)'''
class Player2():
    def __init__(self):
        self.canvasCreate()
        self.username()
        self.s= None


#creating the body and canvas(UI)
    def canvasCreate(self):
        self.root= tk.Tk()
        self.canvas= tk.Canvas(self.root, height= 1000, width= 1000)
        self.canvas.pack()
        self.root.title("Michael's TicTacToe Program")
        self.frame= tk.Frame(self.canvas, bg="white")
        self.frame.place(relheight= 0.8, relwidth= 0.8, relx= 0.1, rely= 0.1)
        self.Lable1= tk.Label(self.frame, text= "Enter Your IP Info")
        self.Lable1.pack()
        self.HostInfo= tk.Entry(self.frame)
        self.HostInfo.pack()
        self.HostInfo.insert(0, 'localhost')#automatically has the host info inserted
        self.Lable2= tk.Label(self.frame, text= "Enter Your Port Info")
        self.Lable2.pack()
        self.PortInfo= tk.Entry(self.frame, text='Please Enter Your Port Info')
        self.PortInfo.pack()
        self.PortInfo.insert(0, '5670') #automatically has the port info inserted 
        self.ConnButton= tk.Button(self.frame, text= "Connect", command= lambda: self.GetConnected())
        self.ConnButton.pack()
        self.root.mainloop()

#creating a socket:
    def GetConnected(self):
        '''client(receives) server this is player2'''    
        p= int(self.PortInfo.get())
        h= str(self.HostInfo.get())
        self.s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((h, p))
        print(p)
        print('connected! ')
        server_uname = self.s.recv(1024)  
        print('playing against:', str(server_uname.decode()))
        self.Label3= tk.Label(self.frame, text= "Enter Your Username Info")
        self.Label3.pack()
        self.UserInfo= tk.Entry(self.frame)
        self.UserInfo.pack()
        self.ConnButton2= tk.Button(self.frame, text= "Enter", command= lambda: self.username())
        self.ConnButton2.pack()
        connected = True
        return self.s
   
    def username(self):
        SC = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '-', '\ |', ']', '[', '}', '{', '.', '/',
          '<', '>', '?', '~']
        user= self.UserInfo.get() 
        connected = True
        while connected:
            count= 0
            for i in user:
                if i in SC:
                    count +=1
                    if count >0:
                        connected = False
                        raise ValueError
            for i in user:
                SecCount= 0
                if count== 0 :
                    print(user,'!!')
                    SecCount+= 1
                    self.Label4= tk.Label(self.frame, text= "Would you like to send your username?")
                    self.Label4.pack()
                    self.ConnButton3= tk.Button(self.frame, text= "Send", command= lambda: self.sendUsername(self.UserInfo.get()))
                    self.ConnButton3.pack()
                    if SecCount >0:
                        connected = False
                        break
        return print('PRINTED:',user)

    def hide(self):
        self.Lable1.pack_forget()
        self.Lable2.pack_forget()
        self.HostInfo.pack_forget()
        self.PortInfo.pack_forget()
        self.ConnButton.pack_forget()
        self.Label3.pack_forget()
        self.UserInfo.pack_forget()
        self.ConnButton2.pack_forget()
        self.root.destroy()
        self.gui = GUI(self)
        return True 
    
    def sendUsername(self, msg):
        #user= str(self.UserInfo.get())
        self.s.sendall(str(msg).encode())
        print('name sent!!')
        self.ConnButton4= tk.Button(self.frame, text= "Start Game!", command= lambda: self.hide())
        self.ConnButton4.pack()



class GUI():
    def __init__(self, Player):
        self.canvasCreate()
        self.player= Player
        self.gameBoard= BoardGame('Player2', 'Player2','x','o', 0, 0,0)
        self.Wins()
        self.Board()


    def canvasCreate(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height= 1000, width= 1000)
        self.canvas.grid()
        self.root.title("TicTacToe Program O-side")
        
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
        self.player.root.update()
        mark= self.player.s.recv(1024).decode()
        print('row and col:', mark)
        row= int(mark[0])
        col= int(mark[1])
        self.button[row][col]['text']= 'x'
        self.gameBoard.updateGameBoard(row, col, 'x')
        self.gameBoard.isWinner()
        self.Wins()

    def mark(self, row, col):
            #print(self.button[row][col].text)
            self.button[row][col]['text']= 'o'
            self.gameBoard.updateGameBoard(row, col, 'o')
            #self.gameBoard.isWinner()
            sendm= self.player.s.sendall((str(row) + str(col)).encode())
            if self.Wins() == True:
                mark= self.player.s.recv(1024).decode()
                print('row and col:', mark)
                row= int(mark[0])
                col= int(mark[1])
                self.button[row][col]['text']= 'x'
                self.gameBoard.updateGameBoard(row, col, 'x')
                return 
            print('sent:', row, col)
            self.root.update()
            mark= self.player.s.recv(1024).decode()
            print('row and col:', mark)
            row= int(mark[0])
            col= int(mark[1])
            self.button[row][col]['text']= 'x'
            self.gameBoard.updateGameBoard(row, col, 'x')
            #self.gameBoard.isWinner()
            if self.Wins() == True:
                mark= self.player.s.recv(1024).decode()
                print('row and col:', mark)
                row= int(mark[0])
                col= int(mark[1])
                self.button[row][col]['text']= 'x'
                self.gameBoard.updateGameBoard(row, col, 'x')
                return 

    def Wins(self):
        if self.gameBoard.isWinner() == True:
            self.gameBoard.GPlayed +=1
            msg= self.player.s.recv(1024).decode()
            if msg == 'yes' :
                self.gameBoard.resetGameBoard()
                for i in range(0,3):
                    for j in range(0,3):
                        self.button[i][j]['text']= ''
                self.root.update()
                return True
            elif msg == 'no' :
                print(self.gameBoard.printStats())
                self.root.destroy()
        return False

if __name__ == '__main__':
    Player2() 
    

'''when a player(players will be assigned marks x or o) presses a button on the frame the button will put that
mark on that stop  '''