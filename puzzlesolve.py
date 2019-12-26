## Author: Justin Stevens
## Date: December 26th, 2019
## Purpose: Solves a YouTube puzzle (secret sauce riddle)
## Link: https://www.youtube.com/watch?v=HyRjuPP9S3o

import math
# Range of Numbers: 13 to 1300
# Interrogators trying to guess Chef's number
# Chef Lies about the Number Being Less than 500
# Chef Lies about whether the Number is a Perfect Square
# Chef Tells truth about whether the number is a perfect cube
# Final Stipulation: Interogators say: if you tell us if the second-to-last digit is a 1 we'd be done here
# Don't know about the last question, if the second digit is a 1

def flip_key(item):
	return (item[0], item[1], item[2], not item[3])
def reverse_key(item):
	return (not item[0], not item[1], item[2], item[3])

# Dictionary to correspond to the items that generated only one value
only_values={}
truth_values=[(a,b,c,d) for a in range(0,2) for b in range(0,2) for c in range(0,2) for d in range(0,2)]
for item in truth_values:
	values=set(range(13, 1301))
	if(item[0]):
		# number is less than 500
		values-=set(range(501, 1301))
	else:
		# number is not less than 500
		values-=set(range(13, 501))
	if(item[1]):
		# number is a perfect square
		values=set([a for a in values if int(math.sqrt(a)+0.5)**2==a])
	else:
		# number is not a perfect square
		values-=set([x**2 for x in range(4, 37)])
	if(item[2]):
		# number is a perfect cube
		values=set([a for a in values if int(a**(1/3)+0.5)**3==a])
	else:
		# number is not a perfect cube
		values-=set([x**3 for x in range(3, 12)])
	if(item[3]):
		# number's second digit is a 1
		values=set([a for a in values if int(a/10)%10==1])
	else:
		# number's second digit is not a 1
		values-=set([a for a in values if int(a/10)%10==1])
	if(len(values))==1:
		only_values[item]=values
# Check the values that only occurred once
for item in only_values.keys():
	# If the flipped version is also in only_values, this is the key the interrogator got
	if flip_key(item) in only_values:
		# You use your detective skills to reverse it
		desired=reverse_key(item)
		# If it's already in the dictionary, return value at that key
		if desired in only_values:
			print(only_values[desired])
		else:
		# Otherwise, flip the key and print out (if no print then puzzle is impossible)
			desired=flip_key(desired)
			print(only_values[desired])
		break