from imports import *

# Most mentioned cities
most_mentioned_city = db.boston_massachusetts.aggregate([{"$match" : {"address.city" : {"$exists" : True}}},
																										  {"$group" : {"_id" : "$address.city",
																															   "count" : {"$sum" : 1}}},
																										  {"$sort" : {"count" : -1}},
																										  {"$limit" : 10}])


print
print "10 Most mentioned cities"
print "------------------------"
for data in most_mentioned_city:
    print data['_id'], " --> ", data['count']

# Mostly true to the dataset, "Boston" has the highest mentions in the documents but as we can see we have names of surrounding
# cities as well like "Cambridge", "Malden" etc. which, explains why we have about 35 of zip codes outside of Boston area.

###########################################
##################RESULT##################
###########################################

'''
10 Most mentioned cities
------------------------
Boston  -->  572
Cambridge  -->  287
Malden  -->  191
Arlington  -->  136
Somerville  -->  134
Jamaica Plain  -->  50
Chelsea  -->  37
Quincy  -->  28
Medford  -->  25
Brookline  -->  22
'''