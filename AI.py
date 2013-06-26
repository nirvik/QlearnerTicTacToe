#!/usr/bin/python

from numpy import *
from random import *
from operator import *
import logging


logging.root.setLevel(logging.INFO)

table = {}
smart_table = {}
player = 'x'
opp = 'o'
alpha=0.5
gamma=0.6
count=0
epsilon=0.5
player ='x'
opp ='o'


def check(grid):
	if None not in grid:
		return 1
	else:
		return 0
def free_positions(grid):
 	pos = []
        for i in range(3):
                for j in range(3):
                        if grid[i][j]==None:
                                pos.append((i,j))
        return pos
def checkNone(grid):
	if None in grid:
		return 1
	else:
		return 0

def danger(grid):
	#danger condition
	enemy_dia = list(grid.diagonal()).count(opp)
	if enemy_dia==2 and checkNone(list(grid.diagonal())):
		return 'Danger'
	for i in range(3):
		if list(grid[:,i]).count(opp)==2 and checkNone(list(grid[:,i])):
			return 'Danger'
	for i in range(3):
		if list(grid[i,:]).count(opp)==2 and checkNone(list(grid[i,:])):
			return 'Danger'
	if  diagonalsignal(list(grid)).count(opp)==2 and checkNone(diagonalsignal(list(grid))):
		return 'Danger'
	
	return 'NoDanger'

def one_in_row(grid): #own player
	for i in range(3):
		if list(grid[i,:]).count(player)==1 and list(grid[i,:]).count(None)==2:
			return 'one_in_row'
	return 'no'

def two_in_row(grid): #own player
	for i in range(3):
		if list(grid[i,:]).count(player)==2 and list(grid[i,:]).count(None)==1:
			return 'two_in_row'
	return 'no'

def empty(grid):
	flag = 1
	for i in range(3):
		for j in range(3):
			if grid[i][j]!=None:
				flag = 0
				break
	if flag == 0:
		return 'notEmpty'
	else:
		return 'Empty'
			
def diagonalsignal(grid):
        col = 2
        row =0
        x=[]
        while row<=3 and col>=0:
                x.append(grid[row][col])
                row+=1
                col-=1
        return x

# the next 5 functions used for rewards 


def inTwoRow(grid):
	logging.error('inTwoRow Reched ')	
	grid = array(grid)
	for i in range(3):
                if list(grid[i,:]).count(player)==2:
			logging.info('InOwnRow: Row elements:{0}'.format(grid[i,:]))
			if  checkNone(list(grid[i,:])):
				logging.info('SATISFIED 2 IN A ROW {0}'.format(grid[:,i]))
                        	return list(grid[i,:])
def inOwnRow(grid):
	
	logging.error('inOwnRow reached')
	grid = array(grid)
	for i in range(3):
                if list(grid[i,:]).count(player)==1:
			logging.error('SATISFIED AND ELEMENT :{0}'.format(grid[i,:]))
			if list(grid[i,:]).count(None)==2:
				logging.error('SATISFIED AND NONE IS PRESENT')
                        	return list(grid[i,:])
 
       
def DangerControlRow(grid):
	grid = array(grid)
	enemy_dia = list(grid.diagonal()).count(opp)
	logging.error('INSIDE DANGERCONTROL: Diagonal elements: {0} and its count {1}'.format(grid.diagonal(),enemy_dia))
        if enemy_dia==2 and checkNone(list(grid.diagonal())):
		logging.info('SATISFIED')
                return list(grid.diagonal())
        for i in range(3):
		logging.error('INSIDE DANGERCONTROL: Column elements: {0} and its count {1}'.format(list(grid[:,i]),list(grid[:,i]).count(opp)))
                if list(grid[:,i]).count(opp)==2 and checkNone(list(grid[:,i])):
                        logging.info('SATISFIED')
			return list(grid[:,i])
        for i in range(3):
		logging.error('INSIDE DANGERCONTROL: Horizontal elements: {0} and its count {1}'.format(list(grid[i,:]),list(grid[i,:]).count(opp)))
                if list(grid[i,:]).count(opp)==2 and checkNone(list(grid[i,:])):
                        logging.info('SATISFIED')
			return list(grid[i,:])
        if diagonalsignal(list(grid)).count(opp)==2 and checkNone(diagonalsignal(list(grid))):
                return diagonalsignal(list(grid))

def danger_action_check(pos,act):
		logging.info('Danger action reached')
		global player
		if act in pos:                      
			if player=='x':
				return 5
                      
			elif player=='o':
                                return -5
                    
		else:
			if player=='x':
                   		return -10
                        elif player =='o':
                              	return 10


def winner_action_check(pos,act):
	logging.error('INSIDE WINNER')
	if act in pos:
		if player =='x':
			return 10
		elif player == 'o':
			return -10
	
	else:
		if player =='x':
			return -10
		elif player=='o':
			return 10

def strategy_action_check(pos,act):
	logging.error('INSIDE STATEGY BUILDUP')
	if act in pos:
		if player =='x':
			return 1
		elif player =='o':
			return -1
	else:
		if player =='x':
			return -1
		elif player == 'o':
			return 1
def isWinner(grid):
	if (len(set(array(grid).diagonal()))==1 and array(grid).diagonal()[0]!=None)  or horizontal(array(grid)) or vertical(array(grid)) or diagonal(grid) or diagonal(grid):
		return 1
	else:
		return 0


def return_smart_pos(signal,grid):

	elements = []
        pos=[]
	grid = array(grid)

        #top most priority to Danger 

        if signal == 'Danger':
                elements = DangerControlRow(grid) #get the danger now identify it
                logging.info('Danger detected : {0}'.format(elements))
                if list(grid.diagonal())==elements: #the diagonal elements
                        for i in range(3):
                                pos.append((i,i))
			return pos
		for i in range(3):
                        if elements == list(grid[i,:]):
                                for j in range(3):
                                        pos.append((i,j))
                                return pos
                for i in range(3):
                        if elements == list(grid[:,i]):
                                for j in range(3):
                                        pos.append((j,i))
                                return pos
                if elements == diagonalsignal(list(grid)):
                        logging.info('Yes Opp diagonal works {0}'.format(elements))
           		pos =diagonal_opp_pos(grid)
			logging.error('Opp diagonal positions {0}'.format(pos))
                 	return pos
        if signal == 'two_in_row':
                elements = inTwoRow(grid)
                for i in range(3):
                        if list(array(grid[i,:]))==elements:
                                for j in range(3):
                                        pos.append((i,j))
                                return pos

        if signal == 'one_in_row':
                elements =inOwnRow(grid)
                logging.error('elements in inOwnRow: {0} and type of grid {1}'.format(elements,type(grid)))
                for i in range(3):
                        if list(array(grid[i,:]))==elements:
                                for j in range(3):
                                        pos.append((i,j))
                                return pos
        elif signal == 'no':
                return free_positions(grid)

def diagonal_opp_pos(grid):
        col = 2
        row =0
        x=[]
        while row<=3 and col>=0:
                x.append((row,col))
                row+=1
                col-=1
        return x



def filter_smart_pos(pos,grid):
	#filtering out the smart recommended positions
	index = []
	for i in pos:
		if grid[i[0]][i[1]]==None:
			index.append(i)
	return index

def reward(signal,act,grid):
	elements = [] 
	pos=return_smart_pos(signal,grid)
	

	#top most priority to Danger 
	
	if signal == 'Danger':
		
		return danger_action_check(pos,act)
			
	if signal == 'two_in_row':
		return winner_action_check(pos,act)

	if signal == 'one_in_row':
		return strategy_action_check(pos,act)

	elif signal == 'no':
		if player=='x':
			return 1
		elif player=='o':
			return -1

def isGridFull(grid):
        flag = 1
        for i in range(3):
                for j in range(3):
                        if grid[i][j]==None:
                                flag =0
                                break
        return flag

def horizontal(grid):
        for i in range(3):
                if len(set(grid[i,:]))==1:
                        if grid[i,:][0]==None:
                #               logging.error('Horizontal: None detected')
                                pass
                        else:
                                return 1

        return 0

def vertical(grid):
        for i in range(3):
                if len(set(grid[:,i]))==1:
                        if grid[:,i][0]==None:
                #               logging.error('Vertical: None detected')
                                pass
                        else:
                                return 1
        return 0

def diagonal(grid):
        col = 2
        row =0
        x=[]
        while row<=3 and col>=0:
                x.append(grid[row][col])
                row+=1
                col-=1
        if len(set(x))==1 and None not in x:
                #logging.error('Diagonal is reason for error')
                return 1
        else:
                return 0

def display(grid):

        for i in range(3):
                for j in range(3):
                        print '{0}        '.format(grid[i][j]),

                print '\n'
        print '\n\n'

def gameover(grid):
        if (len(set(array(grid).diagonal()))==1 and array(grid).diagonal()[0]!=None)  or horizontal(array(grid)) or vertical(array(grid)) or diagonal(grid) or diagonal(grid) or isGridFull(grid):
                return 1
        else:
                return 0 



def gamelearner(grid,start_state,max_games):
	games =0
	no_pos_left = start_state
	global player,opp,epsilon
	while games<max_games:
		if games>150:
			epsilon=0.5
		if games>200:
			episilon=0.8
		if games>300:
			epsilon = 0.9
		
		signal = two_in_row(array(grid))
		logging.info('{0} making the move'.format(player))
		if signal=='no': #giving priority to danger 
			signal = danger(array(grid))
			if signal == 'NoDanger':
				signal = one_in_row(array(grid))

		pos = return_smart_pos(signal,grid)
		pos = filter_smart_pos(pos,grid)
		state_key = []
		for i in pos:
			state_key.append((no_pos_left,i,player))
		for states in state_key:
			if states not in table:
				table[states]=uniform(-2,2)
			if states not in smart_table:
				smart_table[states]=uniform(-2,2)	
		
		logging.info('SIGNAL {0}'.format(signal))
		logging.info('Smart table recommended positions : {0}'.format(pos))
		act = choose(state_key) # passing the key sequence. getting the pos 
		logging.error('The action {0}'.format(act))	
		r = reward(signal,act,array(grid))
		logging.info('Reward for this move {0}'.format(r))
		chosen_state=(no_pos_left,act,player)
		grid[act[0]][act[1]]=player
		display(grid)
		if isWinner(grid):
			if player=='o':
				r=-20
				logging.info('WE HAVE A WINNER {0} and scores {1}'.format(player,r))
			elif player =='x':
				r=20
				logging.info('WE HAVE A WINNER {0} and scores {1}'.format(player,r))
		next_state=execute(no_pos_left)
		next_pos=free_positions(grid)
		next_state_key = []
		for i in next_pos:
			next_state_key.append((next_state,i,opp))
		for next_states in next_state_key:
			if next_states not in table:
				table[next_states]=uniform(-2,2)

		#logging.error('Problem with no of pos left {0} '.format(no_pos_left))
		updateQvalues(chosen_state,r,act,next_state_key,grid)
		print '**************************************************'
		if gameover(grid):
			logging.info('game over')
			grid = [[None for j in range(3)] for i in range(3)]
			player,opp=opp,player
			games+=1
			no_pos_left=start_state
		else:
			player,opp = opp,player
			no_pos_left-=1

def execute(no_pos_left):
	if no_pos_left > 0:
			return no_pos_left-1
	else:
		logging.error('Some shit happened')
	#	return 0

def choose(state_key):
	temp = random()
	action_dict = {}
	
	for state in state_key:
		#action_dict[state]=table[state]
		if smart_table[state]==[]:
			action_dict[state]=table[state]
			logging.error('Taking decisions from normal table')
		else:
			action_dict[state]=smart_table[state]
			logging.error('Using smart table')
		
	#logging.info('dict created for actions {0}'.format(action_dict))
	if state_key[0][-1]=='x':
		best = sorted(action_dict.iteritems(),key= itemgetter(1),reverse=True)
	elif state_key[0][-1]=='o':	
		best = sorted(action_dict.iteritems(),key= itemgetter(1),reverse=False)
	#logging.error('List error {0}'.format(best))
	if temp<epsilon:
		logging.info('The BEST ACTION TAKEN')
		logging.info('Action info:{0}'.format(best[0]))
		return best[0][0][1]
	else:
		random_action = choice(best)[0]
		logging.info('RANDOM ACTION TAKEN :{0}'.format(random_action))
		return random_action[1]

def lowestQvalue(next_key): # return the lowest Q value of a particular state
        low = []
	#logging.info('this is the next_key:{0}'.format(next_key))
        for i in next_key:
                low.append(table[i])
	
        return min(low)


def highestQvalue(next_key): # returns the highest Q value of a particular state
        high = []
        for i in next_key:
                high.append(table[i])

        return max(high)


def updateQvalues(state_key,r,act,next_key,grid):
        global alpha,count
        if gameover(grid):
                alpha = 1
                expected = r
                count =0
        else:

                if state_key[-1] == 'x': # its x's turn . so 'o' thinks of all possible movements of x so as to minimize the reward
                        expected = r + gamma*lowestQvalue(next_key)
                else: # its 'o's turn . so 'x' thinks of the optimal action in the next state which maximises his chance of winning 
                        expected = r + gamma*highestQvalue(next_key)
        change = alpha * (expected - table[state_key])
        table[state_key]+=change

def main():
	global player,opp
	grid = [[None for j in range(3)]for i in range(3)]
	player = 'x'
	opp = 'o'
	start_state= 9 
	max_games=input('enter the max no of games:')
	gamelearner(grid,start_state,max_games)
	for i in table.iteritems():
		print i[0],':',i[1]
	

if __name__=='__main__':
	main()
