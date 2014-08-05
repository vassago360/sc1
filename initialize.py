'''
Created on Aug 5, 2014

@author: user
'''
from derivedClasses import *
import createInitialDatabase

createInitialDatabase.run()
badURLs = []
pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))