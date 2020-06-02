def gen_move(IC, max_elements):
	best_value=-1
	best_index=None
	for i in range(max_elements):
		if i not in IC:
			difference=max([abs(i-s) for s in IC])
			if difference>best_value:
				best_value=difference
				best_index=i
	return best_index

a=gen_move([7], 13)
print(a)