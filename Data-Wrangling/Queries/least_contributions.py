from imports import *
from unique_contributors import unique_contributors

# No. of users with 10 or less contributions
min_contributors = db.boston_massachusetts.aggregate([{"$group" : {"_id" : "$created.user",
                                                                   "contributions" : {"$sum" : 1}}},
                                                      {"$group" : {"_id" : "$contributions",
                                                                   "users_count" : {"$sum" : 1}}},
                                                      {"$sort" : {"_id" : 1}},
                                                      {"$limit" : 10}])
print "DOCUMENTS --> NO. OF USERS, (%ge of users)"
print "---------     ----------------------------"
bottom_ten_users = 0
for contributor in min_contributors:
    bottom_ten_users += contributor['users_count']
    print contributor['_id'], '        -->        ', contributor['users_count'], ", (%.2f)" % float(contributor['users_count'] * 100.0/unique_contributors)

print
print "TOTAL, (%ge of users with 10 docs or less)"
print "------------------------------------------"
print bottom_ten_users, ", (%.2f)" % float(bottom_ten_users * 100.0/unique_contributors)

###########################################
##################RESULT##################
###########################################

'''
DOCUMENTS --> NO. OF USERS, (%ge of users)
---------     ----------------------------
1         -->         338 , (28.24)
2         -->         128 , (10.69)
3         -->         88 , (7.35)
4         -->         60 , (5.01)
5         -->         50 , (4.18)
6         -->         36 , (3.01)
7         -->         24 , (2.01)
8         -->         23 , (1.92)
9         -->         20 , (1.67)
10         -->         15 , (1.25)

TOTAL, (%ge of users with 10 docs or less)
------------------------------------------
782 , (65.33)
'''