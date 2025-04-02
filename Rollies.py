from random import randrange as rand

class DNDRoller:
    def __init__(self):
        self.dice=[]
        self.total=0

    # the parser will fill rolls with information about each roll
    def parser(self,unParsed):
        # understands the user input for number of dice, 
        # number of sides, and modifiers

        # n is number of dice
        # m is sides of die
         #a is modifier
        for uP in unParsed:
            # if no d is found
            if(uP.find("d")==-1): 
                n="1" # 1 die needs to be rolled
                m=uP # and die is the input
            else: # if d is found
                # if multiple d error
                if(uP.count("d")>1):
                    print("Individual input can not contain more than one 'd'.")
                    return True
                # before d is how many die need to be rolled
                n=uP.split("d")[0] 
                m=uP.split("d")[1]

            # if n is not numeric error
            if(not n.isdigit()):
                print("Number of die must be positive integer.")
                return True
            n=int(n)

            # if multiple modifiers error
            modCount=0
            modList=["A","D","E"]
            for i in modList:
                modCount+=m.count(i);
            if(modCount>1):
                print("Only one modifier can be applied at once.")
                return True

            # setting modifier
            if(m.find("A")!=-1): # advantage
                a="advantage"
                m=m.split("A")[0]
            elif(m.find("D")!=-1): # disadvantage
                a="disadvantage"
                m=m.split("D")[0]
            elif(m.find("E")!=-1): # emphasis
                a="emphasis"
                m=m.split("E")[0]
            else:
                a="none"

            # if m is not numeric error
            if(not m.isdigit()):
                print("Number of faces must be a positive integer.")
                return True
            m=int(m)

            self.dice.append(Die(n,m,a))
            return False

    def release(self):
        # release the die to roll all of them

        for d in self.dice:
            d.roll()

    def result(self):
        # creates a result string to be printed in main

        result=""
        for d in self.dice:
            # special print for 1 die being rolled
            if(d.n==1):
                result+=f"Result for {d.m}"
            else:
                result+=f"Result for {d.n}d{d.m}"
            # special print events
            if(d.a=="advantage"): # advantage
                result+=" with advantage"
            elif(d.a=="disadvantage"): # disadvantage
                result+=" with disadvantage"
            elif(d.a=="emphasis"): # emphasis
                result+=" with emphasis"
            result+=".\n"

            # if there are bad values
            if(d.a!="none" and d.n>1):
                # print row of bad values
                result+="\tUnused rolls: "
                width=[];
                for i in range(len(d.badValues)):
                    width.append(len(str(max(d.values[i],d.badValues[i]))))
                    result+=f"{d.badValues[i]:>{width[i]}} "
                result+="\n"
                # print row of good values
                result+="\tUsed rolls:   "
                for i in range(len(d.values)):
                    result+=f"{d.values[i]:>{width[i]}} "
            # if there are only good values
            elif(d.n>1): 
                result+="\tRolls: "
                for i in range(len(d.values)):
                    result+=f"{d.values[i]} "
            # only 1 roll with bad roll
            elif(d.a!="none"): 
                # print bad value
                result+="\tUnused roll: "
                width=len(str(max(d.values[0],d.badValues[0])))
                result+=f"{d.badValues[0]:>{width}} "
                result+="\n"
                # print good value
                result+="\tUsed roll:   "
                result+=f"{d.values[0]:>{width}} "
            # only 1 roll, no bad roll
            else: 
                result+="\tRoll: "
                result+=f"{d.values[0]}"

            # print subtotal of rolls
            d.totaler()
            if(d.n>1 and len(self.dice)>1):
                result+=f"\tSubtotal: {d.total}\n"
                self.total+=d.total
            else:
                result+="\n"
                self.total+=d.total     
        
        # print final total
        result+=f"Total: {self.total}\n"  
        return result

    def help(self):
        # return DND help string

        helpStr="""
    This app can perform roles for DND. These include single, multi die, advantage, disadvantage, and emphasis rolls.

    Basic Rolls:
    To perform a single roll enter a single number.
    To perform a multroll enter the number of dice and then the number of die sides seperated by a "d". Example: 5d6

    Roll Modifiers:
    To perform a roll with advantage, append an "A" to a basic roll.
    To perform a roll with disadvantage, append a "D" to a basic roll.
    To perform a roll with emphasis, append an "E" to a basic roll.

    Multiple rolls can be performed at once by adding a space between them. However, only one modifier can be applied to each roll.
"""
        return helpStr

class AnimonRoller:
    def __init__(self):
        self.dice=[]
        self.total=0
        self.b=0
        self.s=0

    # the parser will fill rolls with information about each roll
    def parser(self,unParsed):
        # understands the user input for number of dice and modifiers

        # n is number of dice
        # a is modifier
        for uP in unParsed:
            self.b=uP.count("B")
            self.s=uP.count("S")
            n=uP.split("B")[0]
            n=uP.split("S")[0]

            # if n is not numeric error
            if(not n.isdigit()):
                print("Number of die must be positive integer.")
                return True
            n=int(n)

            animonDieSides=6
            a="none"
            self.dice.append(Die(n,animonDieSides,a))
        return False

    def release(self):
        # release the die to roll all of them

        for d in self.dice:
            d.roll()

    def result(self):
        # creates a result string to be printed in main

        result=""
        #d=self.dice[0]
        for d in self.dice:
            # special print for 1 die being rolled
            result+=f"Result for {d.n} rolls"

            # special print events
            offset=self.b-self.s
            if(offset>0): # totall boost
                if(offset==1):
                    result+=f" with {self.s} boost."
                else:
                    result+=f" with {self.s} boosts."
            elif(offset<0): # total setback
                if(offset==-11):
                    result+=f" with {self.s} setback."
                else:
                    result+=f" with {self.s} setbackss."
            result+=".\n"

            # if there are only good values
            if(d.n>1): 
                result+="\tRolls: "
                for i in range(len(d.values)):
                    result+=f"{d.values[i]} "
            # only 1 roll, no bad roll
            else: 
                result+="\tRoll: "
                result+=f"{d.values[0]}"

            # print number of successes of rolls
            successes=0
            for i in range(len(d.values)):
                if d.values[i]>3-offset:
                    successes+=1
            result+=f"Successes: {successes}\n"

        return result

    def help(self):
        # return Animon help string

        helpStr="""
    This app can perform roles for Animon.
    All roles are performed with a d6. So the user must enter the number of d6 to roll.

    Roll Modifiers:
    To perform a roll with a setback, append an "S" to a basic roll.
    To perform a roll with boost, append a "B" to a basic roll.
    Multiple can be appended and the effective number of setbacks or boosts will be caluclated.

    Multiple rolls can be performed at once by adding a space between them.
"""
        return helpStr

class Die:
    def __init__(self,n,m,a):
        self.n=n # number of die
        self.m=m # sides on die
        self.a=a # modifier
        self.badValues=[]
        self.values=[]
        self.total=0

    def roll(self):
        # rolls the dice

        # if no advantage or disadvantage
        if(self.a=="none"):
            for i in range(self.n):
                self.values.append(rand(1,self.m+1))
            return
        # has a modifier
        for i in range(self.n):
            a=rand(1,self.m+1)
            b=rand(1,self.m+1)
            # advantage
            if(self.a=="advantage"):
                self.badValues.append(min(a,b))
                self.values.append(max(a,b))
            # disadvantage
            elif(self.a=="disadvantage"):
                self.badValues.append(max(a,b))
                self.values.append(min(a,b))
            # emphasis
            elif(self.a=="emphasis"):
                d1=abs(a-self.m/2)
                d2=abs(b-self.m/2)
                # if both are equivalent you take that roll
                if(a==b):
                    self.values.append(a)
                    self.badValues.append(b)
                # if both are equidistant from (number of sides)/2
                # then must reroll 1 and take its result
                elif(d1==d2):
                    self.values.append(rand(1,self.m+1))
                    self.badValues.append(0)
                elif(d1>d2):
                    self.values.append(a)
                    self.badValues.append(b)
                else:
                    self.values.append(b)
                    self.badValues.append(a)

    def totaler(self):
        # finds the total of that roll

        for i in self.values:
            self.total+=i

def getGame():
    # ensures the user enters a valid game
    game=""
    validGames=["DND","ANIMON"]
    while(game.upper() not in validGames):
        game=input("Enter game: ")
        game=game.split(" ")[0]
        if(game.upper()=="DND"):
            game=game.upper()
        else:
            game=game.title()   
    return game

def main():
    # setup of the program
    print("Enter DND or Animon to select game.")
    game=getGame()
    print("Game set to",game,".")
    print('\tEnter "help" for an explanation of how to roll in this game.')
    print('\tEnter "select" to change game.')
    print('\tEnter "exit" to exit the program.')
    # main program loop
    while(True):
        # initalize the game roller
        if(game.upper()=="DND"):
            tray=DNDRoller()
        elif(game.upper()=="ANIMON"):
            tray=AnimonRoller()

        userIn=input("Enter dice roll(s): ")
        # special cases for user non roll inputs
        if(userIn.upper()=="HELP"):
            print(tray.help())
            continue
        elif(userIn.upper()=="SELECT"):
            game=getGame()
            print("Game changed to",game,".")
            continue
        elif(userIn.upper()=="EXIT"):
            quit()

        # split input for each roll
        individualUP=userIn.split(" ")
        # parse the input
        if(tray.parser(individualUP)): # has an errors
            continue
        # roll all the dice
        tray.release()
        # print the result of the rolls
        print(tray.result())
        print()        

if __name__=="__main__":
    main()