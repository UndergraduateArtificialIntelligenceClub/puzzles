import random
import numpy as np
from scipy.stats import expon

def generate_IC(num_conditions, length, rho):
	"""Generates a number of conditions of a certain length, where each digit is drawn from a binomial distribution with probability rho"""
	conditions=[]
	for _ in range(num_conditions):
		item=[]
		counter=0
		for _ in range(length):
			rand=random.random()
			if rand>rho:
				item.append(0)
			else:
				counter+=1
				item.append(1)
		if counter>length/2:
			result=[1]*length
		else:
			result=[0]*length
		conditions.append([item, result])
	return conditions

def generate_IP(num_population):
	"""Generates an initial population of 32-bit digits to be used for our representation"""
	population=[]
	for _ in range(num_population):
		population.append(random.randrange(0, 2**32))
	return population

def step(bin_pop, initial_IC):
	"""Takes one step forward of an IC with a population"""
	new_IC=[]
	for i in range(len(initial_IC)):
		# if conditions for edge cases so it doesn't loop around (to avoid having information travel from one end to the other)
		if i==0:
			value=4*initial_IC[i]+2*initial_IC[i+1]+initial_IC[i+2]
		elif i==1:
			value=8*initial_IC[i-1]+4*initial_IC[i]+2*initial_IC[i+1]+initial_IC[i+2]
		elif i==len(initial_IC)-1:
			value=16*initial_IC[i-2]+8*initial_IC[i-1]+4*initial_IC[i]
		elif i==len(initial_IC)-2:
			value=16*initial_IC[i-2]+8*initial_IC[i-1]+4*initial_IC[i]+2*initial_IC[i+1]
		else:
			# Full case, convert the neighborhood to a digit from 0 to 31
			value=16*initial_IC[i-2]+8*initial_IC[i-1]+4*initial_IC[i]+2*initial_IC[i+1]+initial_IC[i+2]
		# binary population is a string represented in binary
		#print("bin pop", bin_pop)
		#print("value", value)
		new_value=int(bin_pop[31-value])
		#print("new_value", new_value)
		new_IC.append(new_value)
	return new_IC
def solve(IC, population, limit):
	"""Solves an IC with a population and a certain time limit"""
	initial_IC=IC[0]
	target=IC[1]
	bin_pop='{:032b}'.format(population)
	reverse_target=[1-i for i in target]
	for _ in range(limit):
		# Computation we're exhausting
		new_IC=step(bin_pop, initial_IC)
		print(initial_IC)
		if initial_IC==target and new_IC==initial_IC:
			print("solved")
			# We've gotten our initial IC to the target
			return 1
		else:
			# build up a new IC digit by digit
			initial_IC=new_IC
			# thinks it's the opposite of what it should be
			if initial_IC==reverse_target:
				return 0
	print("not solved")
	return 0
def compute_results(IP, length, cutoff):
	"""Test to see how well 100 IP's do on a list of randomly generated IC's"""
	a1=generate_IC(50, length, 0.1)
	a2=generate_IC(50, length, 0.2)
	a3=generate_IC(50, length, 0.3)
	a4=generate_IC(50, length, 0.4)
	#a5=generate_IC(10, length, 0.5)
	a6=generate_IC(50, length, 0.6)
	a7=generate_IC(50, length, 0.7)
	a8=generate_IC(50, length, 0.8)
	a9=generate_IC(50, length, 0.9)
	# Generated initial conditions
	IC_list=a1+a2+a3+a4+a6+a7+a8+a9
	# Result list to track how each population does
	result_list=[]
	for population in IP:
		# For each population, see how many of the initial conditions it solves!
		counter=0
		for IC in IC_list:
			counter+=solve(IC, population, length)
		result_list.append((population, counter))
	result_list.sort(key=lambda x: x[1], reverse=True)
	# return the best cutoff of the list
	best=result_list[:cutoff]
	print(best[:5])
	return [b[0] for b in best]

def mutate(bin_pop, rate):
	new_pop=''
	for i in range(32):
		if random.random()<rate:
			# Mutate it!
			if bin_pop[i]=='0':
				new_pop+='1'
			else:
				new_pop+='0'
		else:
			new_pop+=bin_pop[i]
	return new_pop
def evolve(IP, number, rate):
	"""Take in a list of IP's and cross-them over to produce a number of new IP's"""
	population=[]
	for _ in range(number):
		# Use an exponential random variable to weight with preference to earlier selections
		#choices=expon.rvs(scale=len(IP),loc=0,size=2)
		#choice0=int(round(choices[0]))
		#if choice0>=len(IP):
		#	choice0=len(IP)-1
		#choice1=int(round(choices[1]))
		#if choice1>=len(IP):
		#	choice1=len(IP)-1
		p=random.sample(IP, 2)
		p0=p[0]
		p1=p[1]
		# Crossover the two populations
		bin_pop0='{:032b}'.format(p0)
		bin_pop1='{:032b}'.format(p1)
		# draw cutoff somewhere around the middle
		cutoff=np.random.normal(0.5, 0.1, 1)[0]
		if cutoff>=1:
			cutoff=1
		elif cutoff<0:
			cutoff=0
		cutoff=int(round(32*cutoff))
		#do single-cutoff crosovver
		bin_pop=bin_pop0[0:cutoff]+bin_pop1[cutoff:32]
		other=bin_pop1[0:cutoff]+bin_pop0[cutoff:32]
		value=int(bin_pop, 2)
		other_value=int(other, 2)
		if value not in IP:
			population.append(value)
		elif other_value not in IP:
			population.append(other_value)
		else:
			new_pop=mutate(bin_pop, rate)
			new_value=int(new_pop, 2)
			population.append(new_value)
	return population
def main():
	IP=generate_IP(100)
	# 15 generations
	for _ in range(15):
		best=compute_results(IP, 39, 20)
		new=evolve(best, 80, 0.35)
		IP=best+new
#main()
compute_results([3548939912], 29, 1)
#compute_results([4219896520, 3493691528, 3641240712, 3641240456, 3548939912], 149, 5)