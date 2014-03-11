#! /usr/bin/env python

i=0
for c in "my secret message":
	if c == ' ':
		print str(i) + " " + str(i+1) + " space"
	else:
		print str(i) + " " + str(i+1) + " " + c
	i += 1
print i