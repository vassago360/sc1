'''
Created on Aug 5, 2014

@author: user
'''
from derivedClasses import *
import createInitialDatabase


subprocess.call(r"rm taxonomyRelations.db backUpTaxonomy.db badWikipediaArticles.p transported*.* ", shell=True)
createInitialDatabase.run()
badURLs = []
pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))