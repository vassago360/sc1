'''
Created on Jun 16, 2014

@author: user
'''

s = sys.stdout
sys.stdout = open("printOuts.txt", "r+") #redirect all prints
sys.stdout.seek(0,2)
#code in here...
sys.stdout.close()
sys.stdout = s