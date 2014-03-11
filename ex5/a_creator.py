#! /usr/bin/env python

for i in range(ord('a'), ord('z')+1):
	print "0 0 " + chr(i) + " " + chr(ord('a') + ((i+20) % 26))

print "0 0 space space"
print "0"
