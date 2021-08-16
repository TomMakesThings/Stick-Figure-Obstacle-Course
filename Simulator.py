import random, time
from tkinter import *

buttonRoot = Tk()
backgroundRoot = Tk()   
tableRoot = Tk()

obstacleNumber = 100
generationSize = 10
buttonNotClicked = True
backgroundCanvas = None
startImage = None

class Person():
    def __init__(self, generationNumber, referenceNumber): #Class attributes
        self.genNumber = generationNumber #References for identification
        self.refNumber = referenceNumber
        self.distance = 0 #Distance travelled
        self.appearance = None #Stores image file name
        self.instinct = [] 
        self.instinctPlace = 0
        self.health = 100
        self.vectorPosition = [0, 0] #Position in environment
        self.fall = False #Checks if fall should occur
        self.damaged = False
        self.stop = False #Checks if movement stopped
        
    def createInstinct(self): 
        self.instinct.append(random.choice(['J', 'W', 'S'])) #Randomly adds either a 'J', 'W' or 'S' to instinct
        if self.genNumber == 1:
            for i in range(3):
                self.instinct.append(random.choice(['J', 'W', 'S'])) #Adds 3 more if first generation
        return self.instinct
                
    def mixGenetics(self, VictorInstinct1, VictorInstinct2):
        for i in range(len(VictorInstinct1)): #Randomly picks one element from either
            try:
                self.instinct.append(random.choice([VictorInstinct1[i], VictorInstinct2[i]]))
            except:
                self.instinct.append(VictorInstinct2[i % len(VictorInstinct2)])
        return self.instinct
    
    def mutateGenetics(self):
        chance = random.randint(0, 6) #1 in 7 chance
        if chance == 0: #Changes action
            self.instinct[random.randint(0, len(self.instinct)-1)] = random.choice(['J', 'W', 'S'])        
        else: #Increases chances of mutation further into instinct
            self.instinct[random.randint(len(self.instinct)//2 + len(self.instinct)//2.5,
                                         len(self.instinct)-1)] = random.choice(['J', 'W', 'S'])
        if chance == 1: #Removes and replaces action shifting all values in instinct to the left
            self.instinct.remove(self.instinct[random.randint(0, len(self.instinct)-1)])
            self.createInstinct()
    
    def changeHealth(self, DamageValue):
        self.health = self.health - DamageValue
        if self.health > 100: #Checks health is between 0 - 100
            self.health = 100
        if self.health < 0:
            self.health = 0
    
    def changeAppearance(self):
        imgName = 'People/Person' + str(self.refNumber%20)
        if self.instinct[self.instinctPlace] == 'J':
            self.appearance = imgName + 'J' + '.png'
        if self.instinct[self.instinctPlace] == 'W':
            self.appearance = imgName + 'W' + '.gif'
        if self.instinct[self.instinctPlace] == 'S':
            self.appearance = imgName + 'S' + '.png'
            
    def runInstinct(self):
        currentInstinct =  self.instinct[self.instinctPlace]
        self.changeAppearance()
        self.instinctPlace += 1
        if self.instinctPlace > len(self.instinct)-1:
            self.instinctPlace = 0 #Resets counter so that currentInstinct loops
        return currentInstinct
    
    def setVectorPosition(self, vectorPosition):
        self.vectorPosition = vectorPosition

class Generation():
    def __init__(self, Number, generationSize):
        self.generationNumber = Number #Reference number
        self.size = generationSize #Number of people within generation
        self.peopleArray = [] #Records people within generation
        self.winningOrder = []
        
    def createGeneration(self, victor1=None, victor2=None, champion=None): #Creates a new set of people
        for i in range(self.size):
            invalid = True 
            while invalid: #Checks for no duplicates
                self.peopleArray.append(Person(self.generationNumber, i))
                if self.generationNumber != 1:
                    if self.peopleArray[i].refNumber % 3 == 0: #Increases chance of success within Generation
                        self.peopleArray[i].mixGenetics(victor1, victor2)
                    else: 
                        self.peopleArray[i].mixGenetics(victor1, champion) 
                    for a in range(len(victor1) // 10 + 1): #Makes mutations occur more with longer instincts
                        self.peopleArray[i].mutateGenetics()
                self.peopleArray[i].createInstinct()
                instinctList = []
                for x in range(len(self.peopleArray)): #Checks no instincts are the same
                    instinctList.append(str(self.peopleArray[x].instinct))
                if len(set(instinctList)) == len(instinctList) and len(set(self.peopleArray[i].instinct)) != 1:
                    invalid = False
                else: #Removes duplicates
                    self.peopleArray.remove(self.peopleArray[i])
            self.peopleArray[i].changeAppearance()
            
    def addWin(self, personRef):
        self.winningOrder.append(self.peopleArray[personRef])
        return self.winningOrder

class Environment():
    def __init__(self):
        self.obstacleOrder = []
        self.currentGen = [] #Keeps a reference of alive members of a generation
        self.messages = {} #Used to display messages showing furthest generation
        
    def createEnvironment(self):
        vectorPos = [5, 0]
        for x in range(0, obstacleNumber*10, 12): #Adds random obstacles
            self.obstacleOrder.append(random.choice([Pit([vectorPos[0] + x, vectorPos[1]]),
                                                     Spike([vectorPos[0] + x, vectorPos[1]]), 
                                                     Cave([vectorPos[0] + x, vectorPos[1]])]))
        
    def removeDead(self): #Removes dead from currentGen
        dead = []
        p = 0 #Index
        while p <= len(self.currentGen)-1:
            if self.currentGen[p].health == 0:
                dead.append(self.currentGen[p])
                self.currentGen.remove(self.currentGen[p])
            else:
                p += 1 #Adds index if no element removed
        return dead
                
class Obstacle():
    def __init__(self, vectorPosition):
        self.vectorPosition = vectorPosition
        self.sizeX = 0 #Width value
        self.sizeY = 0 #Height value
        self.damage = 0
        self.appearance = ''
        
    def isPersonTouching(self, personVector): #Checks the differences in distance
        if abs(personVector[0] - self.vectorPosition[0]) <= self.sizeX: #Compares distance X
            if abs(personVector[1] - self.vectorPosition[1]) <= self.sizeY: #Compares distance Y
                return True
        return False #Returns false if distance too far
    
class Pit(Obstacle):
    def __init__(self, vectorPosition):
        super().__init__(vectorPosition)
        self.damage = 100
        self.appearance = ''
        self.sizeX = 4 #Must be less than half walk / jump x value
        self.sizeY = 2 #Must be less than jump y value
        
class Spike(Obstacle):
    def __init__(self, vectorPosition):
        super().__init__(vectorPosition)
        self.damage = 25
        self.appearance = ''
        self.sizeX = 4 #Must be less than half walk / jump x value
        self.sizeY = 4 #Must be less than jump y value
        
class Cave(Obstacle):
    def __init__(self, vectorPosition):
        super().__init__(vectorPosition)
        self.jumpDamage = 5
        self.appearance = ''
        self.sizeX = 5 #Must be equal to half walk / jump x value
        self.sizeY = 9 #Must be greater than jump y value
        
    def preventJump(self, currentInstinct, person):
        if currentInstinct == 'J': #Calls upon self until different instinct value found
            person.changeHealth(self.jumpDamage)
            currentInstinct = person.runInstinct()
            currentInstinct = self.preventJump(currentInstinct, person)
        return currentInstinct

def createButton(): #Creates start button
    button = Button(buttonRoot, text='START', font=("Lucida console", 70), fg='black', bg='yellow', 
                    height=2, width=10, borderwidth=10)
    button.grid(row=0, sticky=W)
    button.bind('<Button-1>', startSimulation)

def startSimulation(event): #Runs when start button clicked
    global buttonNotClicked, startImage, backgroundCanvas
    buttonNotClicked = False
    backgroundCanvas.delete(startImage)
    generationCount = 1 #Used to set generation Number
    buttonRoot.destroy() #Destroys button GUI
    Env = Environment()
    Env.createEnvironment()
    GUIObstacles(Env) #Places obstacles within GUI
    Gen = Generation(1, generationSize)
    Gen.createGeneration()
    Env.currentGen = Gen.peopleArray
    personPhotos, personImages = GUIPeople(Env) #Creates generation images
    distanceTable, healthTable = GUITable(Env, Gen) #Sets up table
    runSimulation(Env, Gen, personPhotos, personImages, distanceTable, healthTable)
    currentChampion = Gen.winningOrder[0]
    while isWinner(Gen.winningOrder) == False: #Runs until winner found    
        ranking = rank(Gen)   
        if ranking[0].vectorPosition[0] > currentChampion.vectorPosition[0]:
            currentChampion = ranking[0]
        generationCount += 1
        Gen = Generation(generationCount, generationSize)
        Gen.createGeneration(ranking[0].instinct, ranking[1].instinct, currentChampion.instinct)
        Env.currentGen = Gen.peopleArray
        personPhotos, personImages = GUIPeople(Env)
        distanceTable, healthTable = GUITable(Env, Gen) #Sets up table
        runSimulation(Env, Gen, personPhotos, personImages, distanceTable, healthTable)
    print('Winner')
    
def rank(Gen):
    ranking = [] #Records the ranking order
    refDictionary = {} #Keeps a reference of people and vectorPositions
    for p in Gen.winningOrder:
        ranking.append([p.vectorPosition, p.refNumber])
        refDictionary.update({p.refNumber:p})
    ranking.sort()
    for i in range(len(ranking)):
        ranking[i] = refDictionary[ranking[i][1]]
    ranking.reverse() #Victors are added last so list is reversed
    return ranking
    
def runSimulation(Env, Gen, personPhotos, personImages, distanceTable, healthTable):
    while len(Env.currentGen) != 0: #Runs while members of a Generation are still alive
        for p in Env.currentGen:
            while p in Env.currentGen:
                for step in range(12): #Number of steps per action
                    for o in Env.obstacleOrder:
                        if o.isPersonTouching(p.vectorPosition): #Checks for collisions
                            if step == 6: #Checks health updated only once per action
                                p.changeHealth(o.damage) 
                            if o.__class__.__name__ == 'Cave': 
                                if p.instinct[p.instinctPlace] == 'J':
                                    o.preventJump(p.instinct[p.instinctPlace], p)
                                    p.stop = True #Stops movement occuring before step can reset to 0                         
                            if o.__class__.__name__ == 'Pit' and step == 1:
                                p.fall = True                       
                    dead = Env.removeDead()  #Removes dead from environment
                    for d in dead:
                        Gen.winningOrder.append(d)
                        GUIDead(Env, Gen, d, personPhotos, personImages) #Removes dead                    
                    if p.health > 0 and p.stop == False: #Stops movement of dead
                        if p.instinct[p.instinctPlace] == 'W': #Action for walk
                            p.setVectorPosition([p.vectorPosition[0] + 1, p.vectorPosition[1]]) 
                        if p.instinct[p.instinctPlace] == 'J': #Action for jump
                            if step < 6: #Allows jump to move up and down
                                p.setVectorPosition([p.vectorPosition[0] + 1, p.vectorPosition[1] + 1])
                            else:
                                p.setVectorPosition([p.vectorPosition[0] + 1, p.vectorPosition[1] - 1])
                        GUIMove(p, personPhotos, personImages, step)   
                    if p.instinct[p.instinctPlace] == 'S': #Speeds up standing action
                        break
                p.fall = False
                p.stop = False
                GUITableUpdate(p, distanceTable, healthTable)
                if p.vectorPosition[0] >= obstacleNumber*12 + 5: #Checks if reached winning distance
                    Env.currentGen.remove(p)
                    Gen.winningOrder.append(p)
                else:
                    p.runInstinct() #Updates instinct
    
def isWinner(currentPeople):
    winnerFound = False
    for p in currentPeople: #Checks if all obstacles complete
        if p.vectorPosition[0] >= obstacleNumber*12 + 5:
            winnerFound = True #Winner reaches set distance
    return winnerFound
        
def GUIBackground():
    global obstacleNumber
    createButton()
    scroll = Scrollbar(backgroundRoot, orient=HORIZONTAL) #Creates scrollbar
    scroll.pack(side=BOTTOM, fill=X) #Positions scrollbar
    sky = Canvas(backgroundRoot, xscrollcommand = scroll, bg = 'SkyBlue1', 
                 height = backgroundRoot.winfo_screenheight(), width = backgroundRoot.winfo_screenwidth())
    sky.pack(side = TOP) #Makes blue background
    scroll.config(command=sky.xview) #Binds scrollbar to window 'sky'
    grass = sky.create_rectangle(-3000, backgroundRoot.winfo_screenheight(), 
                                 obstacleNumber * 600 + backgroundRoot.winfo_screenwidth(), 700, 
                                 fill = 'yellow green', width = 7) 
    global backgroundCanvas
    backgroundCanvas = sky #Keeps record of Canvas        
    frames = [] #Stores GIF frames
    randomImg = random.randint(0, 19) #Displays random person image
    for i in range(12): #Creates frames
        frames.append(PhotoImage(master = sky, file='People/Person' + str(randomImg) + 'W.gif', 
                                 format="gif -index " +str(i)))
    img = sky.create_image(100, 517, image = frames[0])
    global startImage
    startImage = img
    sky.image = frames[0]
    while buttonNotClicked: #Runs in background until 'START' pressed
        for i in range(12):
            sky.itemconfigure(img, image = frames[i]) #Changes GIF frame
            backgroundRoot.update()        
            backgroundRoot.after(1)
            time.sleep(0.08)
            sky.move(img, 10, 0) #Moves image across screen
            if sky.coords(img)[0] > backgroundRoot.winfo_screenwidth() + 50:
                sky.move(img, -backgroundRoot.winfo_screenwidth() - 50, 0)
    
def GUIObstacles(Env):
    global backgroundCanvas #Uses global variables
    global obstacleNumber
    for o in range(len(Env.obstacleOrder)): #Places obstacles into given environment using widgits
        if Env.obstacleOrder[o].__class__.__name__ == 'Pit': #Pits made using rectangles
            pit = backgroundCanvas.create_rectangle(Env.obstacleOrder[o].vectorPosition[0] * 60 + 0, 
                                                    backgroundRoot.winfo_screenheight(), 
                                                    Env.obstacleOrder[o].vectorPosition[0] * 60 + 400, 700, 
                                                    fill = 'SkyBlue1', width = 7)
            pit = backgroundCanvas.create_rectangle(Env.obstacleOrder[o].vectorPosition[0] * 60 + 4, 607, 
                                                    Env.obstacleOrder[o].vectorPosition[0] * 60 + 397, 707, 
                                                    fill = 'SkyBlue1', width = 0)
        if Env.obstacleOrder[o].__class__.__name__ == 'Spike': #Spikes made using polygons
            spike = backgroundCanvas.create_polygon((Env.obstacleOrder[o].vectorPosition[0] * 60 + 100, 700, 
                                                     Env.obstacleOrder[o].vectorPosition[0] * 60 + 150, 600, 
                                                     Env.obstacleOrder[o].vectorPosition[0] * 60 + 200, 700), 
                                                    fill="red", outline = 'black', width = 7)
        if Env.obstacleOrder[o].__class__.__name__ == 'Cave': #Caves made using rectangles
            cave = backgroundCanvas.create_rectangle(Env.obstacleOrder[o].vectorPosition[0] * 60 - 100, 700, 
                                                     Env.obstacleOrder[o].vectorPosition[0] * 60 + 500, 0, 
                                                     fill = 'gray23', width = 7)
            cave = backgroundCanvas.create_rectangle(Env.obstacleOrder[o].vectorPosition[0] * 60 -100, 350, 
                                                     Env.obstacleOrder[o].vectorPosition[0] * 60 + 500, 0, 
                                                     fill = 'gray65', width = 7)
        startSign = backgroundCanvas.create_rectangle(0, 180, -300, 120, fill='white', width=5), #Creates signs for reference
        startSign = backgroundCanvas.create_text(-150, 150, font=("Lucida console", 30), fill = 'gray10', 
                                            text='Start'),
        startSign = backgroundCanvas.create_rectangle(-25, 120, -35, 0, fill='gray93', width=5),
        startSign = backgroundCanvas.create_rectangle(-285, 120, -275, 0, fill='gray93', width=5)  
        finishSign = backgroundCanvas.create_rectangle(obstacleNumber*600 + 750, 180, obstacleNumber*600 + 450, 120, 
                                                       fill='white', width=5),
        finishSign = backgroundCanvas.create_text(obstacleNumber*600 + 600, 150, font=("Lucida console", 30), fill = 'gray10', 
                                                     text='Finish'),
        finishSign = backgroundCanvas.create_rectangle(obstacleNumber*600 + 725, 120, obstacleNumber*600 + 715, 0, 
                                                       fill='gray93', width=5),
        finishSign = backgroundCanvas.create_rectangle(obstacleNumber*600 + 485, 120, obstacleNumber*600 + 475, 0, 
                                                       fill='gray93', width=5)         
        
def GUIPeople(Env): #Sets up Canvas images
    global backgroundCanvas
    personPhotos = {}
    personImages = {}
    for p in Env.currentGen:
        personPhotos[p.refNumber] = PhotoImage(master = backgroundCanvas, file = 'People/Person' + str(p.refNumber%20) + 'W.gif')
        personImages[p.refNumber] = backgroundCanvas.create_image(p.refNumber * -100 - 100, p.vectorPosition[1] * 60 + 517, 
                                                                  image = personPhotos[p.refNumber])
        backgroundCanvas.canvasImage = personPhotos[p.refNumber]
    return personPhotos, personImages
        
def GUIMove(person, personPhotos, personImages, step):
    global backgroundCanvas 
    personPhotos[person.refNumber] = PhotoImage(master = backgroundCanvas, file = person.appearance)
    backgroundCanvas.itemconfigure(personImages[person.refNumber], image = personPhotos[person.refNumber])
    if person.instinct[person.instinctPlace] == 'W': #Movement for walk
        frames = []
        for i in range(12): #Creates animation
            frames.append(PhotoImage(master = backgroundCanvas, file='People/Person' + str(person.refNumber%20) + 'W.gif', 
                                     format="gif -index " +str(i)))   
        backgroundCanvas.itemconfigure(personImages[person.refNumber], image = frames[step])
        backgroundCanvas.coords(personImages[person.refNumber], person.vectorPosition[0] * 60 + 200, 
                                person.vectorPosition[1] * 60 + 517)
        if person.fall == True: #Falling
            backgroundCanvas.move(personImages[person.refNumber], 10, step*100)
    if person.instinct[person.instinctPlace] == 'J': #Movement for jump
        backgroundCanvas.coords(personImages[person.refNumber], person.vectorPosition[0] * 60 + 200, 
                                person.vectorPosition[1] * -25 + 517)   
    if person.instinct[person.instinctPlace] == 'S': #Movement for stand
        backgroundCanvas.coords(personImages[person.refNumber], person.vectorPosition[0] * 60 + 200, 
                                person.vectorPosition[1] * 60 + 517)
    backgroundCanvas.update()
    backgroundCanvas.after(1)
    time.sleep(0.05)    
                
def GUIDead(Env, Gen, person, personPhotos, personImages):
    global backgroundCanvas
    backgroundCanvas.delete(personImages[person.refNumber])
    ranking = rank(Gen)
    if ranking[0].refNumber == person.refNumber: #Checks if new record reached in generation
        try: #Moves sign GUI
            backgroundCanvas.coords(Env.messages[person.genNumber][0], person.vectorPosition[0] * 60 + 360, 180,
                                    person.vectorPosition[0] * 60 + 40, 120)
            backgroundCanvas.coords(Env.messages[person.genNumber][1], person.vectorPosition[0] * 60 + 200, 150)
            backgroundCanvas.coords(Env.messages[person.genNumber][2], person.vectorPosition[0] * 60 + 335, 120,
                                    person.vectorPosition[0] * 60 + 325, 0)
            backgroundCanvas.coords(Env.messages[person.genNumber][3], person.vectorPosition[0] * 60 + 75, 120,
                                    person.vectorPosition[0] * 60 + 65, 0)
        except: #Creates new sign GUI
            Env.messages[person.genNumber] = [backgroundCanvas.create_rectangle(person.vectorPosition[0] * 60 + 360, 180,
                                                                               person.vectorPosition[0] * 60 + 40, 120, 
                                                                               fill='white', width=5),
                                              backgroundCanvas.create_text(person.vectorPosition[0] * 60 + 200, 150, 
                                                                          font=("Lucida console", 30), fill = 'gray10', 
                                                                          text='Generation ' + str(person.genNumber)),
                                              backgroundCanvas.create_rectangle(person.vectorPosition[0] * 60 + 335, 120,
                                                                                person.vectorPosition[0] * 60 + 325, 0, 
                                                                                fill='gray93', width=5),
                                              backgroundCanvas.create_rectangle(person.vectorPosition[0] * 60 + 75, 120,
                                                                                person.vectorPosition[0] * 60 + 65, 0, 
                                                                                fill='gray93', width=5)]
    
def GUITable(Env, Gen):
    numberTable = {}
    distanceTable = {}
    healthTable = {}
    colours = {0:'turquoise3', 1:'yellow', 2:'IndianRed2', 3:'gray47', 4:'green3', 5:'LightSkyBlue1', 6:'MediumPurple2',
               7:'dark orange', 8:'blue2', 9:'magenta', 10:'gray12', 11:'lawn green', 12:'purple3', 13:'red2',
               14:'DarkGoldenRod1', 15:'saddle brown', 16:'orchid1', 17:'snow', 18:'IndianRed3', 19:'plum3'}
    GenName = Label(tableRoot, text='Generation ' + str(Gen.generationNumber), font=("Lucida console", 30), 
                 fg='black', bg='white', height=2, width=30, borderwidth=2, relief="solid", padx=5, pady=2)
    GenName.grid(row=0, sticky=W)
    Title1 = Label(tableRoot, text='Number', font=("Lucida console", 30), fg='black', bg='white', borderwidth=2, 
                   relief="solid", padx=5, pady=5, width=10)
    Title1.grid(row=1, stick=W)
    Title2 = Label(tableRoot, text='Distance', font=("Lucida console", 30), fg='black', bg='white', borderwidth=2, 
                   relief="solid", padx=5, pady=5, width=10)
    Title2.grid(row=1)
    Title3 = Label(tableRoot, text='Health', font=("Lucida console", 30), fg='black', bg='white', borderwidth=2, 
                   relief="solid", padx=5, pady=5, width=10)
    Title3.grid(row=1, stick=E)    
    for p in Env.currentGen: #Sets up table records
        numberTable[p.refNumber] = Label(tableRoot, text=str(p.refNumber), font=("Lucida console", 20), bg=colours[p.refNumber%20],
                                            borderwidth=2, relief="solid", padx=5, pady=2, width=15)
        numberTable[p.refNumber].grid(row=p.refNumber+2, sticky=W)        
        distanceTable[p.refNumber] = Label(tableRoot, text=str(p.vectorPosition[0]), font=("Lucida console", 20), bg=colours[p.refNumber%20],
                                              borderwidth=2, relief="solid", padx=5, pady=2, width=15)
        distanceTable[p.refNumber].grid(row=p.refNumber+2)
        healthTable[p.refNumber] = Label(tableRoot, text=str(p.health), font=("Lucida console", 20), bg=colours[p.refNumber%20],
                                   borderwidth=2, relief="solid", padx=5, pady=2, width=15)
        healthTable[p.refNumber].grid(row=p.refNumber+2, sticky=E)  
    return distanceTable, healthTable

def GUITableUpdate(person, distanceTable, healthTable):
    distanceTable[person.refNumber].config(text=str(person.vectorPosition[0]))
    healthTable[person.refNumber].config(text=str(person.health))

GUIBackground()

buttonRoot.mainloop()
backgroundRoot.mainloop()
tableRoot.mainloop()