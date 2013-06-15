#!/usr/bin/python


from random import *
from numpy import *
import logging

logging.root.setLevel(logging.INFO)

def sigmoid(theta,x):
	x= transpose(x)
	z= matrix(theta)*x
	z= z.item()*(-1.0)
	#logging.info('this is what sigmoid returns {0}'.format((1.0/(1+exp(-z)))))
	return 1.0/(1.0+exp(z)) #return prediction

def cost(x,y,theta):
	minimum = 0.000
        for i in range(8):
                #minimum+=(y[i]*log10(sigmoid(theta,x[i])) + (1-y[i])*log10(1-sigmoid(theta,x[i])))
		if y[i]==0 and 1-sigmoid(theta,x[i])==0 or y[i]==1 and sigmoid(theta,x[i])==0:
			logging.info("error caught")
			continue
		if y[i]==0:
			minimum+= (1-y[i])*log(1-sigmoid(theta,x[i]))
			#logging.info(minimum)
		else:
			minimum+= y[i]*log(sigmoid(theta,x[i]))
			#logging.info(minimum)
	return -minimum/8.0

def summation(theta,x,y,j,mat):
	add = 0
	for i in range(8):
		add+=(sigmoid(theta,x[i])-y[i])*mat[i][j]
	return  add


def main():
	x=matrix([[6.0, 1.8, 12.0],[5.92, 1.9, 11.0],[5.58, 1.7, 12.0],[5.92, 1.65, 10.0],[5.0, 1.0, 6.0],[5.5, 1.5, 8.0],[5.42, 1.3, 7.0],[5.75, 1.5, 9.0]])
	y=[1,1,1,1,0,0,0,0]
	theta=[1.0,2.0,3.0]
	print '{0}'.format(theta)

	jmin = cost(x,y,theta)
	temp=theta
	alpha = 0.1
	n=0
	i=0
	print '{0} is the initial cost'.format(jmin)
	mat=array(x)
	for i in range(100): 	
		temp[0]=temp[0] - (alpha/(n+1))*summation(temp,x,y,0,mat)
		temp[1]=temp[1] - (alpha/(n+1))*summation(temp,x,y,1,mat)
		temp[2]=temp[2] - (alpha/(n+1))*summation(temp,x,y,2,mat)
		logging.info('theta 1:{0} \n theta 2:{1} \n theta 3:{2}'.format(temp[0],temp[1],temp[2]))
		print '{0} is cost'.format(cost(x,y,temp))
		if cost(x,y,temp)<jmin:
			jmin = cost(x,y,temp)
			theta = temp
			n+=1
	#	elif i>30 and cost(x,y,temp)>jmin:
	#		logging.info(" Logistic regression Gradient Descent obtained")


	print ' Final parameters {0} and cost {1}'.format(theta,jmin)
	
	h1 = input('enter height:')
	w1 = input('enter weight:')
	f1 = input('enter foot size:')
	sample = matrix([[h1,w1,f1]])
	if sigmoid(theta,sample) > 0.5:
		print 'Male predicted'
	else:
		print 'Female predicted'


if __name__=='__main__':
	main()
