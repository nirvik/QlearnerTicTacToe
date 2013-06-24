#!/usr/bin/python

from numpy import *
from random import *
from operator import *
#from __future__ import print_function
import logging

logging.root.setLevel(logging.INFO)
#  create a table of dictionary type
# keys : states eg 1(1 piece on the board),2(2 pieces on the board) etc till 9
# values: a dictionary containing actions and its associated rewards
# actions are basically the postitions you would move to
# table = { 1 : {a1:val1,a2:val2,a3:val3,a4:val4} } 

table = {}
actions={}
gamma  = 0.6
alpha = 0.5
r = 1
k = 0.05
epsilon = 0.85

#check if grid is full
def isGridFull(grid):
	flag = 1
	for i in range(3):
		for j in range(3):
			if grid[i][j]==None:
				flag =0 
				break
	return flag

#caluclate the free postions
def free_positions(grid):
	pos = []
	for i in range(3):
		for j in range(3):
			if grid[i][j]==None:
				pos.append((i,j))
	return pos

#return reward by checking  if won lost or draw 
def reward_fun(grid):
	for i in range(3):
		if len(set(grid[:,i]))==1:
			if grid[:,i][0]=='x':
				return 10.0
			elif grid[:,i][0]=='o':
				return -10.0
	for i in range(3):
		if len(set(grid[i,:]))==1:
			if grid[i,:][0]=='x':
                                return 10.0
                        elif grid[i,:][0]=='o':
                                return -10.0
			else:
				pass

	if len(set(grid.diagonal()))==1:
		element = list(set(grid.diagonal()))
		if element[0]=='x':
			return 10.0
		elif element[0]=='o':
			return -10.0
		else:
			pass
	
	#if diagonal(list(grid)):
			
	return 0

#if key not in dict then return the values of the key 
def create_actions(grid):
	#for i in range(3):
	#	for j in range(3):
	#		if grid[i][j]==None:
	#			actions[(i,j)]=uniform(-0.15,0.15)
	#		else:
	#			actions[(i,j)]=-0.15
	
	#return actions
	return 0


#checking if the move is valid
def action_valid(act,grid):
	if grid[act[0]][act[1]]==None:
		return 1
	else:
		return 0
#displaying board
def display(grid):

	for i in range(3):
		for j in range(3):
			print '{0}        '.format(grid[i][j]),

		print '\n'
	print '\n\n'
def horizontal(grid):
        for i in range(3):
                if len(set(grid[i,:]))==1:
			if grid[i,:][0]==None:
		#		logging.error('Horizontal: None detected')
				pass
			else:
                        	return 1

        return 0

def vertical(grid):
        for i in range(3):
                if len(set(grid[:,i]))==1:
			if grid[:,i][0]==None:
		#		logging.error('Vertical: None detected')
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

def gameover(grid):
	if (len(set(array(grid).diagonal()))==1 and array(grid).diagonal()[0]!=None)  or horizontal(array(grid)) or vertical(array(grid)) or diagonal(grid) or diagonal(grid) or isGridFull(grid):
                return 1
        else:
                return 0 #draw


#The Game Learner
def game_learner(grid,player,opp,start_state,max_games):
	game = 0
	no_pos_left = start_state
	state_key = [] #list containing all the possible states of the board
	while game<max_games:

		#calculate all the free postitions
		#therefore the state will be defined as (no of free pos,pos,player)
		pos = free_positions(grid)
		state_key = []
		for i in pos:
			state_key.append((no_pos_left,i,player)) #created all the possible states for that config
		#print '{0} Turn '.format(player)
		for states in state_key:
			if states not in table:
				table[states]=create_actions(grid)
			#	logging.info('entry added')
		act = choose(state_key,grid)#choosing a particular action using epsilon greedy
		logging.info('{0} is the action'.format(act))
		if not action_valid(act,grid):
			if isGridFull(grid):
				print 'Grid full ABORT ABORT'
			logging.error('action not valid {0}'.format(act))
			pass
		else:
			chosen_state=(no_pos_left,act,player)
			next_state = execute(no_pos_left) # function that returns the state after taking the action
			grid[act[0]][act[1]]=player # adding the player to the board
			display(grid)
			next_pos = free_positions(grid)
			next_state_key=[]
			for i in next_pos:
				next_state_key.append((next_state,i,opp))

			r = reward_fun(array(grid))
			if isGridFull(grid):
				if player=='x':
					r=5
				elif player == 'o':
					r=-5
				logging.info('its a draw')
			#logging.info('{0} is the reward for this move'.format(r))
			for next_states in next_state_key:	
				if next_states not in table:
					table[next_states]=create_actions(grid)
				#	logging.info('Entry of opp added')
			updateQvalues(chosen_state,r,act,next_state_key,grid) # update the Q values of state action pair reward 
			if gameover(grid):
				logging.info('Game over and rewarded awared {0} and winner is {1}'.format(r,player))
				display(grid)
				grid = [[None for j in range(3)]for i in range(3)]
				
				player,opp = opp,player
				no_pos_left = start_state
				#state = start_state,player
				game+=1
			else:
				player,opp=opp,player # switch players
				no_pos_left-=1
				#state = next_state
				#logging.info("now its {0}'s turn".format(player))
	
		
	grid = [[None for j in range(3)]for i in range(3)]	
	player = raw_input(' enter character(x):')
	no_pos_left = 9
	opp = 'o'
	while not gameover(grid):
		pos = input('enter position:')
		grid[pos[0]][pos[1]]=player
		display(grid)
		no_pos_left = no_pos_left-1
		free = free_positions(grid)
		state_key = []
		for i in free:
			state_key.append((no_pos_left,i,opp))
		act = choose(state_key,grid)
		grid[act[0]][act[1]]=opp
		display(grid)

def execute(no_pos_left):
	if no_pos_left>0:
		return no_pos_left-1
	else:
		logging.info('something went wrong')	
def choose(state_key,grid):
	temp = random()
	count = 0
	action_dict = {}
	for state in state_key:
		action_dict[state]=table[state]
	if state_key[0][-1]=='x':	
		best_list = sorted(action_dict.iteritems(),key= itemgetter(1),reverse=True)#get the highest
	elif state_key[0][-1]=='o':
		best_list = sorted(action_dict.iteritems(),key= itemgetter(1),reverse=False) # get the lowest
	print best_list
	if	temp<epsilon:
		logging.info('Best action taken {0}'.format(best_list[0][0][1]))
		return best_list[0][0][1]
	else:
		random_action = choice(best_list)[0][1]
		logging.info('random action taken {0}'.format(random_action))	
		return random_action

def lowestQvalue(next_key): # return the lowest Q value of a particular state
	low = []
	for i in next_key:
		low.append(table[i])

	return min(low)
		

def highestQvalue(next_key): # returns the highest Q value of a particular state
	high = []
	for i in next_key:
		high.append(table[i])

	return max(high)
count =0
def updateQvalues(state_key,r,act,next_key,grid):
	global alpha,count
	if gameover(grid):
		alpha = 0.5
		expected = r
		count =0
	else:

		if state_key[-1] == 'x': # its x's turn . so 'o' thinks of all possible movements of x so as to minimize the reward
			expected = r + gamma*lowestQvalue(next_key)
		else: # its 'o's turn . so 'x' thinks of the optimal action in the next state which maximises his chance of winning 
			expected = r + gamma*highestQvalue(next_key)
	change = alpha * (expected - table[state_key])
	alpha = alpha/(count+1)
	table[state_key]+=change

			

def main():
	grid = [[None for j in range(3)] for i in range(3)]
	player = 'x'
	opp = 'o'
	start_state = 9 # 9 positions remaining 
	max_games= input('enter the max no of games for the game to learn:')
	

	game_learner(grid,player,opp,start_state,max_games)
	print 'Okay The comp is intelligent enough to play you ! bring it on!'
	for i in table.iteritems():
		print i[0],':',i[1]
	
if __name__=='__main__':
	main()
	
