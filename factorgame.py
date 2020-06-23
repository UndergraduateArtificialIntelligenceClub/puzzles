INFINITY = 1000000

import sys
import re
sys.setrecursionlimit(1500)

class Board():
	def __init__(self, n):
		self.b=list(range(1, n+1))
		self.backtrack=[]
		# 1 represents Alice is to play
		self.toplay=1
		self.alice=0
		self.bob=0
	def is_terminal(self):
		"""Check to see if any two numbers divide each other"""
		for i in range(len(self.b)-1):
			for j in range(i+1, len(self.b)):
				if self.b[j]%self.b[i]==0:
					return False
		return True
	def play_move(self, m):
		#self.b.remove(m)
		removed=[]
		for num in self.b:
			if m%num==0:
				removed.append(num)
		if len(removed)>1:
			self.b=[x for x in self.b if x not in removed]
		else:
			return 0
		self.backtrack.append(removed)
		if(self.toplay):
			self.alice+=m
			self.bob+=sum(removed)-m
		else:
			self.alice+=sum(removed)-m
			self.bob+=m
		self.toplay=self.toplay ^ 1
		return 1
	def undo_move(self):
		removed=self.backtrack.pop()

		# update scores accordingly
		m=removed[-1]
		if(self.toplay):
			self.alice-=(sum(removed)-m)
			self.bob-=m
		else:
			self.alice-=m
			self.bob-=(sum(removed)-m)
		self.toplay=self.toplay ^ 1
		# update board position
		self.b=self.b+removed
		self.b.sort()

	def gen_all_moves(self):
		legal_moves=[]
		for i in range(len(self.b)):
			for j in range(i):
				if self.b[i]%self.b[j]==0:
					legal_moves.append(self.b[i])
					break 
		return legal_moves

	def compute_move(self, m):
		removed=[]
		for num in self.b:
			if m%num==0:
				removed.append(num)
		return 2*m-sum(removed)

	def gen_greedy_move(self, num):
		value=[]
		for move in self.gen_all_moves():
			value.append((move, self.compute_move(move)))
		value.sort(key=lambda x: x[1], reverse=True)
		return [l[0] for l in value[:num]]

	def staticallyEvaluate(self):
		if self.toplay:
			return self.alice-self.bob
		else:
			return self.bob-self.alice

# Code below adapted from Martin Muller

big_dict={}

def minimaxOR(state, alpha, beta):
	"""Alice tries to maximize her score"""
	bestMove=0
	diff=state.alice-state.bob
	key=list_to_key(state.b)
	if state.is_terminal():
		#print("reached end of game")
		return state.staticallyEvaluate(), 0
	#elif key in big_dict:
	#	return big_dict[key]+(diff), 0
	for m in state.gen_greedy_move(1):
		state.play_move(m)
		value = -minimaxAND(state, -beta, -alpha)[0]
		#new_key=list_to_key(state.b)
		big_dict[key]=value-(diff)
		state.undo_move()
		if value > alpha:
			alpha = value
			bestMove=m
		if value>=beta:
			return beta, 0
	return alpha, bestMove

def minimaxAND(state, alpha, beta):
	"""Bob tries to minimize Alice's score"""
	bestMove=0
	diff=state.bob-state.alice
	key=list_to_key(state.b)
	if state.is_terminal():
		#print("reached end of game")
		return state.staticallyEvaluate(), 0
	#elif key in big_dict:
	#	return big_dict[key]+diff, 0
	for m in state.gen_all_moves():
		state.play_move(m)
		value = -minimaxOR(state, -beta, -alpha)[0]
		#new_key=list_to_key(state.b)
		big_dict[key]=value-diff
		state.undo_move()
		if value > alpha:
			alpha = value
			bestMove=m
		if value>=beta:
			return beta, 0
	return alpha, bestMove

def list_to_key(lst):
	value=0
	for i in lst:
		value+=(2**(i-1))
	return value

def key_to_list(key):
	"""Function isn't actually needed"""
	binary='{:042b}'.format(key)
	# reverse the string
	binary=binary[::-1]

	matches=re.finditer('1', binary)
	match_pos=[match.start()+1 for match in matches]
	return match_pos

def main(): 
	for j in range(2, 35):
		#print(big_dict)
		game=Board(j)
		print(j, minimaxOR(game, -INFINITY, INFINITY))
main()
