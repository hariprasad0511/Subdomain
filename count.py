

import string

fname = str(raw_input("Enter the Output File Name >>> "))
file1 = open(fname,'r')
strTot = file1.read()
file1.close()
print ("Total items found is: ", strTot.count("-"))
