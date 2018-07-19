from colorama import Fore, Style, init
from os import system, name
import random

class Card:
    def __init__(self,text,action):
        self.text=text
        self.action=action
    def doAction(self,player):
        if self.action[0]=="+":
            player.cash+=int(self.action[1:])
        elif self.action[0]=="-":
            player.cash+=int(self.action[1:])
        elif self.action[0]=="e":
            for p in board.players:
                p.cash-=int(self.action[1:])   
            player.cash+=(int(self.action[1:]) *(len(board.players)+1))      
        elif self.action=="go":
            player.position=1
            player.cash+=200
        elif self.action=="jail":
            player.position=11
            player.inJail=True
        elif self.action=="outJail":
            player.inJail=False
            player.getOutOfJailCard=True
        elif self.action=="IllinoisAve":
            player.position=25
        elif self.action=="nearestUtil":
            if player.position<13 or player.position>29:
                player.position=13
            else:
                player.position=29
        elif self.action=="StCharles":
            player.position=12
        elif self.action=="back3":
            player.position-=3
        elif self.action=="nearestRailRoad":
            if player.positon>36 or player.position<6:
                player.position=6
            elif player.position>6 or player.positon <16:
                player.positon=16
            elif player.positon>16 or player.position < 26:
                player.positon = 26
            else:
                player.positon=36
class Board:
    def __init__(self):
        self.board=[]
        self.properties=[]
        self.propertiesDict={}
        self.players=[]
        self.unpackProperties()
        self.initBoard()
        self.chanceCards=[]
        self.chanceCardsUsed=[]
        self.communityCards=[]
        self.communityCardsUsed=[]
        self.unpackCards()
    def unpackProperties(self):
        propertiesTXT=open("Properties.txt","r")
        propertiesLines=propertiesTXT.readlines()
        for x in range(0,len(propertiesLines),5):
            self.properties.append(Property(propertiesLines[x].rstrip("\n"), int(propertiesLines[x+1]), propertiesLines[x+2], propertiesLines[x+3], propertiesLines[x+4]))
        self.properties.append(Property("Go",1,"NA","NA","NA"))
        self.properties.append(Property("Income Tax",5,"NA","NA","NA"))
        self.properties.append(Property("Jail",11,"NA","NA","NA"))
        self.properties.append(Property("Free Parking",21,"NA","NA","NA"))
        self.properties.append(Property("Go To Jail",31,"NA","NA","NA"))
        self.properties.append(Property("Luxury Tax",39,"NA","NA","NA"))
        for p in self.properties:
            self.propertiesDict[p.position]=p
    def unpackCards(self):
        chanceCardsTXT=open("ChanceCards.txt","r")
        chanceLines=chanceCardsTXT.readlines()
        for line in chanceLines:
            self.chanceCards.append(Card(line.split(":")[0],line.split(":")[1]))
        random.shuffle(self.chanceCards)
        communityCardsTXT=open("CommunityChestCards.txt","r")
        communityLines=communityCardsTXT.readlines()
        for line in communityLines:
            self.communityCards.append(Card(line.split(":")[0],line.split(":")[1]))
        random.shuffle(self.chanceCards)
        
         
    def printBoard(self):
        for row in self.board:
            print self.colorRow(row)
        print "Position:Name\n-----------------------"
        for player in self.players:
            info=str(self.propertiesDict[player.position].name)+"["+str(player.position)+"]:"+str(player.name[:])
            print info+"\n-----------------------"
    def initBoard(self):
        self.board.append(["[11]","[12]","[13]","[14]","[15]","[16]","[17]","[18]","[19]","[20]","[21]"])
        self.board.append(["[10]","    ","    ","    ","    ","    ","    ","    ","    ","    ","[22]"])
        for i in range(1,9):
            self.board.append(["[ "+str(10-i)+"]","    ","    ","    ","    ","    ","    ","    ","    ","    ","["+str(22+i)+"]"])
        self.board.append(["[ 1]","[40]","[39]","[38]","[37]","[36]","[35]","[34]","[33]","[32]","[31]"])
    def colorRow(self,row):
        colorRowList=[]
        for i in row:
            color=""
            #print i
            if i !="    ":
                boardPos=int(i[1:-1])
                #print p.position, boardPos
                #print i
                for p in self.properties:
                    
                    if int(p.position)==boardPos:
                    
                        color=p.group
            #print color,"Violet"
            if("Violet" in color):
                colorRowList.append(Fore.MAGENTA+i+Style.RESET_ALL)
            elif("Dark-Green" in color):
                colorRowList.append(Fore.GREEN+i+Style.RESET_ALL)
            elif("Yellow" in color):
                colorRowList.append(Fore.YELLOW+Style.BRIGHT+i+Style.RESET_ALL)
            elif("Purple" in color):
                colorRowList.append(Fore.BLUE+i+Style.RESET_ALL)
            elif("Light-Blue" in color):
                colorRowList.append(Fore.CYAN+i+Style.RESET_ALL)
            elif("Red" in color):
                colorRowList.append(Fore.RED+i+Style.RESET_ALL)
            elif("Orange" in color):
                colorRowList.append(Fore.YELLOW+i+Style.RESET_ALL)            
            elif("Dark-Blue" in color):
                colorRowList.append(Fore.BLUE+Style.BRIGHT+i+Style.RESET_ALL)            
                
            
            else:
                colorRowList.append(Fore.WHITE+i+Style.RESET_ALL)
        return " ".join(colorRowList)
    def createPlayers(self):
        while True:
            try:
                numPlayers=raw_input("Please input number of players\n->")
                for i in range(int(numPlayers)):
                    name=raw_input("Please enter your name, Player "+str(i+1)+"\n->")
                    self.players.append(Player(name,i+1))
                    #print self.players[i].name
            except ValueError:
                pass
            else:
                break

    def takeTurns(self):
        while True:
            for player in self.players:
                while player.turnComplete == False:
                    player.presentOptions()
                player.turnComplete=False

class Property:
    def __init__(self,name,position,price,rent,group):
        self.name=name
        self.position=position
        self.price=price
        self.rent=rent
        self.group=group
        self.owner="None"
    
board=Board()
class Player:
    def __init__(self,name,number):
        self.name=name
        self.number=number
        self.color=""
        self.cash=1500
        self.options=["Show All Player's Info", "Roll Dice And Move", "Buy Property", "Show Cards","Show Board Positions","End Turn"]
        self.properties=[]
        self.position=1
        self.turnComplete=False
        self.hasMoved=False
        self.lastRoll=[]
        self.getOutOfJailCard=False
        self.inJail=False
        self.turnsInJail=0
    def presentOptions(self):
        board.printBoard()
        print "Your turn,"+self.name
        for i in range(len(self.options)):
            print str(i+1),self.options[i]    
        while True:
            try:
                choice=int(raw_input("Please choose an option \n->"))
                if(choice==1):
                    clear()
                    for player in board.players:
                        print player.name
                        print "Cash: "+str(player.cash)
                        print "Properties:"+str(player.properties)
                        print "--"*6
                    raw_input("Press enter to continue\n->")
                    clear()
                elif(choice==2):
                    clear()
                    if self.hasMoved == False:
                        diceRoll=self.rollDice()
                        self.move(diceRoll)
                    else:
                        print "You have already moved"
                    raw_input("Press enter to continue\n->")
                    clear()
                elif(choice==3):
                    clear()
                    self.buyProperty()
                    raw_input("Press enter to continue\n->")
                    clear()
                elif(choice==4):
                    pass
                elif(choice==5):
                    clear()
                    for position in board.propertiesDict:
                        print "Position: "+str(board.propertiesDict[position].position)
                        print "Name: "+board.propertiesDict[position].name
                        print "Price: "+board.propertiesDict[position].price
                        print "Rent: "+board.propertiesDict[position].rent
                        print "Group: "+board.propertiesDict[position].group
                        if board.propertiesDict[position].owner==("None" or "NA"):
                            print "Owner: "+ board.propertiesDict[position].owner
                        else:
                            print "Owner: "+ board.propertiesDict[position].owner.name
                        print "----------------------------"
                    raw_input("Press enter to continue\n->")
                    clear()
                elif(choice==6):
                    if self.hasMoved==True:
                        self.turnComplete=True  
                        self.hasMoved=False
                        clear()
                else:
                    pass
            except ValueError:
                pass
            else:
                break
    def rollDice(self):
        self.lastRoll=[random.randint(1, 6),random.randint(1, 6)]
        return [8]#self.lastRoll
    def move(self,diceRoll):
        print "You rolled: "+str(diceRoll)
        self.position+=sum(diceRoll)
        self.position=self.position % 40
        self.hasMoved=True
        if self.position in [3,18,34]:
            print board.communityCards[0].text
            board.communityCardsUsed.append(board.communityCardsUsed[0])
            board.communityCards.remove(board.communityCardsUsed[0])
        elif self.position in [8,23,37]:#chance
            print board.chanceCards[0].text
            board.chanceCardsUsed.append(board.chanceCards[0])
            board.chanceCards.remove(board.chanceCards[0])
        elif self.position==(5 or 39):
            clear()
            print "You owe the bank 200 dollars."
            print raw_input("Press enter to continue\n->")
            clear()
        elif board.propertiesDict[self.position].owner!=(self and "None"):
            clear()
            print board.propertiesDict[self.position].owner
            print "You owe rent : "+board.propertiesDict[self.position].rent
            print raw_input("Press enter to continue\n->")
        elif self.position==31:
            clear()
            print "You landed on Go To Jail, take a guess what happens next?"
            self.position=11
            self.inJail=True
            self.turnsInJail=3
            print raw_input("Press enter to continue\n->")
    def buyProperty(self):
        try:
            if board.propertiesDict[self.position].price=="NA":
                raise KeyError
            if board.propertiesDict[self.position].owner=="None":
                print board.propertiesDict[self.position].name
                print "Position: "+str(board.propertiesDict[self.position].position)
                print "Price: " +str(board.propertiesDict[self.position].price)
                print "Group: "+board.propertiesDict[self.position].group
                print "Rent: "+str(board.propertiesDict[self.position].rent)
                purchase=raw_input("Would you like to purchase this property (y/n)?\n->")
                #print self.cash,board.propertiesDict[self.position].price,int(self.cash)>int(board.propertiesDict[self.position].price)
            
                if purchase[0].upper()=="Y":
                    if int(self.cash)>int(board.propertiesDict[self.position].price):
                        board.propertiesDict[self.position].owner=self
                        self.properties.append(board.propertiesDict[self.position].name)
                        self.cash-=int(board.propertiesDict[self.position].price)
                    else:
                        print "Sorry, you do not have the funds"
                
            elif board.propertiesDict[self.position].owner==self:
                print "You own this property!"
            else:
                print "This property is owned by:"+board.propertiesDict[self.position].owner.name
        except KeyError:
            print "Sorry, you can not purchase this spot."        
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
        
def main():
    init()
    board.createPlayers()
    clear()
    board.takeTurns()
    
main()