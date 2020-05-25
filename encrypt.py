# Implements a very basic cipher... I'll leave it to the reader to figure out what's going on :-)
from math import ceil
def encrypt(message):
	even_message=message[0:len(message):2]
	odd_message=message[1:len(message):2]
	return even_message+odd_message
def decrypt(message):
	new_message=''
	split=ceil(len(message)/2)
	for i in range(split):
		new_message+=message[i]
		if (split+i)<len(message):
			new_message+=message[i+split]
	return new_message
assert(encrypt(decrypt('helloworld'))=='helloworld')
print(encrypt('THYSECRETISTHYPRISONERIFTHOULETITGOTHOUARTAPRISONER'))
print(decrypt('TYERTSHPIOEITOLTTOHURARSNRHSCEITYRSNRFHUEIGTOATPIOE'))