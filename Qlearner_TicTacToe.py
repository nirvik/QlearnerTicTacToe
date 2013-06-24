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
epsilon = 0.9

#check if grid is full
def isGridFull(grid):
	flag = 1
	for i in range(3):
		for j in range(3):
			if grid[i][j]==None:
				flag =0 
				break
	return flag

#return reward by checking  if won lost or draw 
def reward_fun(grid):
	for i in range(3):
		if len(set(grid[:,i]))==1:
			if grid[:,i][0]=='x':
				return 1.0
			elif grid[:,i][0]=='o':
				return -1.0
	for i in range(3):
		if len(set(grid[i,:]))==1:
			if grid[i,:][0]=='x':
                                return 1.0
                        elif grid[i,:][0]=='o':
                                return -1.0
			else:
				pass

	if len(set(grid.diagonal()))==1:
		element = list(set(grid.diagonal()))
		if element[0]=='x':
			return 1.0
		elif element[0]=='o':
			return -1.0
		else:
			pass
	return 0.0

#if key not in dict then return the values of the key 
def create_actions(grid):
	for i in range(3):
		for j in range(3):
			if grid[i][j]==None:
				actions[(i,j)]=uniform(-0.15,0.15)
			else:
				actions[(i,j)]=-0.15
	
	return actions



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
	state = start_state
	
	while game<max_games:
		state_key=(state,player)
		print '{0} Turn '.format(player)
		if state_key not in table:
			table[state_key]=create_actions(grid)
			logging.info('Entry added')
		act = choose(state_key,grid)#choosing a particular action using epsilon greedy
		#logging.info('{0} is the action'.format(act))
		if not action_valid(act,grid):
			if isGridFull(grid):
				print 'Grid full ABORT ABORT'
			logging.error('action not valid {0}'.format(act))
			pass
		else:
			next_state = execute(state) # function that returns the state after taking the action
			grid[act[0]][act[1]]=player # adding the player to the board
			display(grid)
			next_state_key = (next_state,opp)
			r = reward_fun(array(grid))
		#	logging.info('{0} is the reward for this move'.format(r))
			if next_state_key not in table:
				table[next_state_key]=create_actions(grid)
				logging.info('Entry of opp added')
			updateQvalues(state_key,r,act,next_state_key,grid) # update the Q values of state action pair reward 
			if gameover(grid):
				logging.info('Game over and rewarded awared {0}'.format(r))
				display(grid)
				grid = [[None for j in range(3)]for i in range(3)]
				state=start_state
				player,opp = opp,player
				game+=1
			else:
				player,opp=opp,player # switch players
				state = next_state
				#logging.info("now its {0}'s turn".format(player))
		
def execute(state):
	if state>0:
		return state-1
	else:
		logging.info('something went wrong')	
def choose(state_key,grid):
	temp = random()
	action_dict = table[state_key]
	count = 0
	best_list = sorted(action_dict.iteritems(),key= itemgetter(1),reverse=True)
	while not action_valid(best_list[count][0],grid): #sorting the action list and giving the best action 
		count+=1
	#logging.info('the best action list for this state {0}'.format(best_list))
	#logging.info('optimal action {0}'.format(best_list[0][0]))
	if temp<epsilon:
		logging.info('Best action taken {0}'.format(best_list[count][0]))
		return best_list[count][0]
	else:
		random_action = choice(best_list)
		logging.info('random action taken {0}'.format(random_action))
		return random_action[0]
	
def lowestQvalue(next_key): # return the lowest Q value of a particular state
	low = []
	for i in table[next_key].itervalues():
		low.append(i)

	return min(low)
		

def highestQvalue(next_key): # returns the highest Q value of a particular state
	high = []
	for i in table[next_key].itervalues():
		high.append(i)
	return max(high)

def updateQvalues(state_key,r,act,next_key,grid):
	if gameover(grid):
		
		expected = r
	else:

		if state_key[1] == 'x': # its x's turn . so 'o' thinks of all possible movements of x so as to minimize the reward
			expected = r + gamma*lowestQvalue(next_key)
		else: # its 'o's turn . so 'x' thinks of the optimal action in the next state which maximises his chance of winning 
			expected = r + gamma*highestQvalue(next_key)
	change = alpha * (expected - table[state_key][act])
	table[state_key][act]+=change

			

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
	
