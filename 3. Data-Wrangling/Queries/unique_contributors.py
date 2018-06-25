from imports import *

# No. of unique contributors
unique_contributors = len(db.boston_massachusetts.distinct("created.uid"))
print
print "No. of unique contributors:", unique_contributors
print

###########################################
##################RESULT##################
###########################################

'''
No. of unique contributors: 1197
'''