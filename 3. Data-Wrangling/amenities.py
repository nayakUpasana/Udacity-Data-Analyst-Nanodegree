from imports import *

# List of amenities and their count
amenities = db.boston_massachusetts.aggregate([{"$match" : {"amenity" : {"$exists" : True}}},
                                               {"$group" : {"_id" : "$amenity",
                                                            "count" : {"$sum" : 1}}},
                                               {"$sort" : {"count" : -1}},
                                               {"$limit" : 10}])

print
print "LIST OF AMENITIES AND COUNT:"
print "----------------------------"
for data in amenities:
    print data['_id'], " --> ", data['count']
print

# Places of worship
places_of_worship = db.boston_massachusetts.aggregate([{"$match" : {"amenity" : {"$exists" : True}, "amenity" : "place_of_worship", "religion" : {"$exists" : True}}},
                                                       {"$group" : {"_id" : "$religion",
                                                                    "count" : {"$sum" : 1}}},
                                                       {"$sort" : {"count" : -1}}])

print "TOP 5 PLACES OF WORSHIP:"
print "------------------------"
for data in places_of_worship:
    print data['_id'], " --> ", data['count']
print

# Restaurants & cuisine
restaurants = db.boston_massachusetts.aggregate([{"$match" : {"amenity" : {"$exists" : True}, "amenity" : "restaurant", "cuisine" : {"$exists" : True}}},
                                                 {"$group" : {"_id" : "$cuisine",
                                                              "count" : {"$sum" : 1}}},
                                                 {"$sort" : {"count" : -1}},
                                                 {"$limit" : 5}])

print "TOP 5 CUISINES"
print "--------------"
for data in restaurants:
    print data['_id'], " --> ", data['count']

# Top 5 restaurants with highest capacity
top_capacity_restaurants = db.boston_massachusetts.find({"amenity" : "restaurant", "capacity" : {"$exists" : True}}).sort("capacity", -1).limit(5)

print
print "TOP 5 RESTAURANTS WITH HIGHEST CAPACITY:"
print "----------------------------------------"
for data in top_capacity_restaurants:
    print data['name'], "-->", data['capacity']

print
res_with_no_capacity_info = db.boston_massachusetts.find({"amenity" : {"$exists" : True}, "amenity" : "restaurant", "capacity" : {"$exists" : False}}).count()
print "Restaurants with no capacity info:", res_with_no_capacity_info
    
# As you can see, there are still over 300 restaurants with no capacity data. Having the this info for all the restaurants would have given us a better idea

###########################################
##################RESULT##################
###########################################

'''
LIST OF AMENITIES AND COUNT:
----------------------------
parking  -->  742
bench  -->  527
restaurant  -->  376
school  -->  339
parking_space  -->  224
place_of_worship  -->  212
library  -->  157
bicycle_parking  -->  155
cafe  -->  151
fast_food  -->  127

PLACES OF WORSHIP:
------------------
christian  -->  183
jewish  -->  9
unitarian_universalist  -->  4
muslim  -->  2
buddhist  -->  1

CUISINES
--------
pizza  -->  32
mexican  -->  20
chinese  -->  17
indian  -->  15
italian  -->  15

RESTAURANTS WITH HIGHEST CAPACITY
---------------------------------
The Haven --> 100
Chicago Pizza --> 40
Yume Wo Katare --> 20
Taco Party --> 20
All Star Pizza Bar --> 20

Restaurants with no capacity info: 367
'''