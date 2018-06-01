"""
' ' = Position is empty
X = agent's move
O = opponents move
"""
from random import randint

class Node:
    def __init__(self, state, parent=None, nature = None, score = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.score = 0
        self.nature = nature

        if parent:
            self.parent.children.append(self)

#given a move i.e. 'O' or 'X', play the move in all empty spots available and append every state to a list.


# used when player makes a move.
def makeMove(board, index):
    if board[index] == ' ':
        board[index] = 'O'
        return True
    else:
        return False

#print the board
def display(board):
    print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
    print(' ---------')
    print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
    print(' ---------')

    print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
    print()

#check gameOver
def gameOver(board):
    if board.count(' ') == 0 or gameWon(board, 'X') or gameWon(board, 'O'):
        return True
    else:
        return False

#check the winner  
def gameWon(board, player):
    if ((board[0] == player and board[1] == player and board[2] == player) |
(board[3] == player and board[4] == player and board[5] == player) |
(board[6] == player and board[7] == player and board[8] == player) |
(board[0] == player and board[3] == player and board[6] == player) |
(board[1] == player and board[4] == player and board[7] == player) |
(board[2] == player and board[5] == player and board[8] == player) |
(board[0] == player and board[4] == player and board[8] == player) |
(board[2] == player and board[4] == player and board[6] == player)):
        return True
    else:
        return False
def getWinner(board):
    player = 'X'
    if ((board[0] == player and board[1] == player and board[2] == player) |
(board[3] == player and board[4] == player and board[5] == player) |
(board[6] == player and board[7] == player and board[8] == player) |
(board[0] == player and board[3] == player and board[6] == player) |
(board[1] == player and board[4] == player and board[7] == player) |
(board[2] == player and board[5] == player and board[8] == player) |
(board[0] == player and board[4] == player and board[8] == player) |
(board[2] == player and board[4] == player and board[6] == player)):
        return 'Agent Won'
    else:
        player = 'O'
        if ((board[0] == player and board[1] == player and board[2] == player) |
(board[3] == player and board[4] == player and board[5] == player) |
(board[6] == player and board[7] == player and board[8] == player) |
(board[0] == player and board[3] == player and board[6] == player) |
(board[1] == player and board[4] == player and board[7] == player) |
(board[2] == player and board[5] == player and board[8] == player) |
(board[0] == player and board[4] == player and board[8] == player) |
(board[2] == player and board[4] == player and board[6] == player)):
            return 'You Won'
        else:
            return 'Draw'
def getNextStates(state, move):
    if gameOver(state):
        return []
    else :
        empty = [i for i,x in enumerate(state) if x == ' ']
        nextStates = []
        for i in range(len(empty)):
            tmp = state[:]
            tmp[empty[i]] = move
            nextStates.append(tmp)
        return nextStates

#generate state space from a given state of game
def generateStateSpace(state):
    initState = Node(state, parent = None, nature = 'Max', score = -10)

    stack = [state]
    stackNodes = [initState]
    leaf = []
    #generating statespace
    while len(stack)!=0:
        node = stack.pop()
        prevNode = (stackNodes.pop())
        if prevNode.nature == 'Max':
            agent = 'X'
        else:
            agent = 'O'
        tmp = getNextStates(node,agent)
        stack = stack + tmp
        for nodes in tmp:
            tmpNode = (Node(nodes,parent = prevNode))
            if tmpNode.parent.nature == 'Max':
                tmpNode.nature = 'Min'
                tmpNode.score = 10
            elif tmpNode.parent.nature == 'Min':
                tmpNode.nature = 'Max'
                tmpNode.score = -10

            stackNodes.append(tmpNode)
            if gameOver(tmpNode.state):
                leaf.append(tmpNode)

    return initState, leaf

def assignLeafScores(leaf):
    #assigning score to leaf nodes
    for i in range(len(leaf)):
        if gameWon(leaf[i].state, 'X'):
            leaf[i].score = 1
        elif gameWon(leaf[i].state, 'O'):
            leaf[i].score = -1
        else:
            leaf[i].score = 0
    return leaf

#fault minMax
def minMax(initState, leaf):
    #minMax
    for aNode in leaf:
        while True:
            if aNode.parent is None:
                break
            if aNode.parent.nature == 'Max':
                if aNode.parent.score <= aNode.score:
                    aNode.parent.score = aNode.score
            elif aNode.parent.nature == 'Min':
                if aNode.parent.score >= aNode.score:
                    aNode.parent.score = aNode.score
            aNode = aNode.parent
            

    return max(initState.children, key=lambda x: x.score) #return the child with max score

#applying minMax 
def getScore(node, leaf):
    if node in leaf:
        return node.score
    elif node.nature == 'Max':
        return max(getScore(child,leaf) for child in node.children)
    elif node.nature == 'Min':
        return min(getScore(child,leaf) for child in node.children)

#get the best possible move
def minMaxv1(initState, leaf):
    for nodes in initState.children:
        nodes.score = getScore(nodes,leaf)
    return max(initState.children, key=lambda x: x.score) 

print('Welcome to Tic-Tac-Toe \nYour move is "O" ')
current = [' ',' ',' ',' ',' ',' ',' ',' ', ' ']
display(current)


choice = input('Enter 1 to make first move\n')
if choice == '1':
    move = input('Enter the position of your move\n') # horizontal 0-based indexing
    move = int(move)
    while makeMove(current,move) == False:
        move = input('Please enter a valid position to move\n')
        move = int(move)
    display(current)
    initState,leaf = generateStateSpace(current)
    leaf = assignLeafScores(leaf)
    current = minMaxv1(initState,leaf).state
    print('Agent\'s move')

    display(current)
    
else:
    print('Agent\'s move')
    current[randint(0, 8)] = 'X' #first move can be random since Max for every move is 0
    display(current)


while True:
    move = input('Enter the position of your move\n')
    move = int(move)

    while makeMove(current,move) == False:
        move = input('Please enter a valid position to move\n')
        move = int(move)

    display(current)
    if gameOver(current):
        print(getWinner(current))
        break
    
    initState,leaf = generateStateSpace(current)
    leaf = assignLeafScores(leaf)
    current = minMaxv1(initState,leaf).state
    display(current)
    if gameOver(current):
        print(getWinner(current))
        break