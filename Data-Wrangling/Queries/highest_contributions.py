from imports import *
from no_of_docs import total

# Users with highest contributions & percentage
max_contributors = db.boston_massachusetts.aggregate([{"$group" : {"_id" : "$created.user", 
																														 "contributions" : {"$sum" : 1}}},
																									{"$sort" : {"contributions" : -1}},
																									{"$limit" : 10}])

print "DOCS SUBMITTED, (contribution %ge) -->  USERS"
print "----------------------------------      -----"
top_ten_docs = 0
for contributor in max_contributors:
    top_ten_docs += contributor['contributions']
    print contributor['contributions'], ", (%.2f)" % float(contributor['contributions'] * 100.0/total), '                  -->   ',contributor['_id']

print
print "TOTAL DOCS SUBMITTED BY THE TOP 10 USERS, (contribution %ge)"
print "---------------------------------------------------------------"
print top_ten_docs, ", (%.2f)" % float(top_ten_docs * 100.0/total)

###########################################
##################RESULT##################
###########################################

'''
DOCS SUBMITTED, (contribution %ge) -->  USERS
----------------------------------      -----
597677 , (52.77)                   -->    crschmidt
214329 , (18.92)                   -->    jremillard-massgis
55587 , (4.91)                   -->    wambag
45447 , (4.01)                   -->    OceanVortex
33690 , (2.97)                   -->    morganwahl
32991 , (2.91)                   -->    ryebread
29291 , (2.59)                   -->    MassGIS Import
16220 , (1.43)                   -->    ingalls_imports
14125 , (1.25)                   -->    Ahlzen
7363 , (0.65)                   -->    mapper999

TOTAL DOCS SUBMITTED BY THE TOP 10 USERS, (contribution %ge)
---------------------------------------------------------------
1046720 , (92.42)
'''