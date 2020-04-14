import random

#0-null,1-X,2-O
q = []
board = []
trials = 50000
counter = 0

#Resets the board to start the game
def boardReset():
  board.clear()
  board.append([0,0,0])
  board.append([0,0,0])
  board.append([0,0,0])

#Board For Testing
def board2():
  board2 = []
  board2.clear()
  board2.append([0,0,0])
  board2.append([0,1,0])
  board2.append([0,0,0])
  return board2

#Returns a copy of the current board
def getBoard():
  return board.copy()

#Checks if all possible moves at a state are bad
def isNeg(temp):
  temp = findBoard(temp)
  for x in temp[1:]:
    if x[1]>=0:
      return False
  return True

#Checks if a move is positive at this state
def isPos(temp):
  temp = findBoard(temp)
  for x in temp[1:]:
    if x[1]>=0:
      return True
  return False

#Checks what reward to give
#If move led to positive, then positive
#If led to all negative, then negative
def getReward(temp):
  if findBoard(temp)==0:
    return 0
  if isPos(temp):
    return 1
  elif isNeg(temp):
    return -100
  else:
    return 0

#returns a copy of every list within a list
def cop(lis):
  ln = []
  ln.clear()
  if type(lis) == list:
    for x in lis:
      if type(x) == list:
        ln.append(cop(x))
      else:
        ln.append(x)
  return ln

#prints a list by item
def printList(lis):
  for x in lis:
    print(x)

#find q-entry by board state
def findBoard(state):
  for x in q:
    if(x[0]==state):
      return x
  return 0

def printFoundBoard(state):
  entry = findBoard(state)
  if entry==0:
    print("None Found")
  else:
    printList(entry[0])
    print()
    printList(entry[1:])

#check if won
def checkWin():
  lis = []
  shor = []
  shor2 = []
  shor3 = []
  shor4 = []
  for x in range(3):
    shor = []
    shor2 = []
    for y in range(3):
      shor.append(board[x][y])
      shor2.append(board[y][x])
    lis.append(shor.copy())
    lis.append(shor2.copy())
    shor3.append(board[x][x])
    shor4.append(board[x][2-x])
  lis.append(shor3.copy())
  lis.append(shor4.copy())
  for x in lis:
    if(x.count(1)==3):
      return -100
    elif(x.count(2)==3):
      return 1
  return 0

#moves
def move(move,num):
  move1 = move.copy()
  x = move1[0]
  y = move1[1]
  board[x][y]=num

#does a random move from enterest values
def randMove(num,valid):
  val = valid.copy()
  if (len(val)==1):
    rand1 = 0
  else:
    rand1 = random.randrange(0,len(val))
  move(val[rand1],num)
  return val[rand1]

#Calculates the best move to do
def calcMove(cur):
  temp = findBoard(cur)
  neg = []
  zero = []
  pos = []
  out = []
  if temp==0:
    out = randMove(2,getMoves(cur))
    return out
  for x in temp[1:]:
    if x[1]>0:
      pos.append(x[0])
    elif x[1]==0:
      zero.append(x[0])
    else:
      neg.append(x[0])
  if len(pos)>0:
    out = randMove(2,pos)
  elif len(zero)>0:
    out = randMove(2,zero)
  else:
    out = randMove(2,neg)
  return out

#Gets all possible moves
def getMoves(cur):
  pos = []
  for x in range(3):
    for y in range(3):
      if(cur[x][y]==0):
        row = x
        column = y
        pos.append([row,column])
  return pos

#Gets all possible moves in string form
def getMovesStr(cur):
  out = []
  for x in getMoves(cur):
    out.append(str(x[0])+","+str(x[1]))
  return out

#Picks least done move at state
def learnMove(num,valid):
  if findBoard(getBoard()) == 0:
    return randMove(num,getMoves(getBoard()))
  counters = []
  for x in findBoard(getBoard())[1:]:
    counters.append(x[2])
  mindex = counters.index(min(counters))
  valid = [findBoard(getBoard())[1+mindex][0]]
  return randMove(num,valid)

#Records a value into the q-table
def record(move,cur,reward):
  global q
  global counter
  if reward==0:
    reward = checkWin()
  temp = findBoard(cur)
  if temp == 0:
    counter = 0
    print("New")
    lis = [cur]
    for x in getMoves(cur):
      lis.append([x,0,0])
    for x in lis[1:]:
      if(x[0]==move):
        x[1]+=reward
        x[2]+=1
        break
    q.append(lis)
  else:
    for x in temp[1:]:
      if(x[0]==move):
        if x[1]==0 and reward != 0:
          print("New")
          counter = 0
        elif x[2]==0:
          print("New")
          counter = 0
        else:
          counter += 1
          print("Repeat")
        x[1]+=reward
        x[2]+=1
        break

#Gets a player move
def playerMove(cur):
  moveP = input("Move: ")
  while moveP not in getMovesStr(cur):
    print("Try Again")
    moveP = input("Move: ")
  moveP = moveP.split(",")
  moveP[0]=int(moveP[0])
  moveP[1]=int(moveP[1])
  return moveP

#Test game for player
def testGame():
  boardReset()
  printList(board)
  move(playerMove(getBoard()),1)
  printList(board)
  while (checkWin()==0)and(len(getMoves(getBoard()))>0):
    print()
    calcMove(getBoard()).copy()
    printList(getBoard())
    if (checkWin()!=0)or(len(getMoves(getBoard()))==0):
      break
    move(playerMove(getBoard()),1)
    printList(board)
  print(checkWin())

#Computer game for learning
def computerGame():
  boardReset()
  randMove(1,getMoves(getBoard()))
  while (checkWin()==0)and(len(getMoves(getBoard()))>0):
    temp = cop(getBoard())
    move = learnMove(2,getMoves(getBoard()))
    if (checkWin()!=0)or(len(getMoves(getBoard()))==0):
      break
    randMove(1,getMoves(getBoard()))
    record(move,temp,getReward(getBoard()))
  record(move,temp,0)

#test code
def testCode():
  for x in range(trials):
    computerGame()
  printFoundBoard(board2())
  play = input("Play a game? [y]: ")
  while play == "y":
    testGame()
    play = input("Play a game? [y]: ")

testCode()