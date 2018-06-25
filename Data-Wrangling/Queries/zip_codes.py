from imports import *

# Zip codes

# All the zip codes in the Boston area
boston_zip_codes = ['01841', '02101', '02108', '02109', '02110', '02111', '02112', '02113', '02114', '02115', '02116', '02117',
									'02118', '02119', '02120', '02121', '02122', '02123', '02124', '02125', '02126', '02127', '02128', '02129',
									'02130', '02131', '02132', '02133', '02134', '02135', '02136', '02137', '02141', '02149', '02150', '02151',
									'02152', '02163', '02171', '02196', '02199', '02201', '02203', '02204', '02205', '02206', '02210', '02211',
									'02212', '02215', '02217', '02222', '02228', '02241', '02266', '02283', '02284', '02293', '02297', '02298',
									'02445', '02467']

print
# Documents with "postcode" in the "address" section
docs_with_postcode = db.boston_massachusetts.find({'address.postcode' : {"$exists" : True}}).count()
print "Documents with \"postcode\" in the \"address\" section:", docs_with_postcode

# Documents with "postcode" in Boston area
docs_with_postcode_in_boston = db.boston_massachusetts.find({'address' : {"$exists" : True}, 'address.postcode' : {"$in" : boston_zip_codes}}).count()
print "Documents with \"postcode\" in the Boston area:", docs_with_postcode_in_boston

# Documents with "postcode" not in the Boston area
docs_with_postcode_outside = db.boston_massachusetts.find({'address' : {"$exists" : True}, 'address.postcode' : {"$exists" : True, "$nin" : boston_zip_codes}}).count()
print "Documents with \"postcode\" outside the Boston area:", docs_with_postcode_outside

docs_with_postcode_outside_details = db.boston_massachusetts.find({'address' : {"$exists" : True}, 'address.postcode' : {"$exists" : True, "$nin" : boston_zip_codes}})

# On further expansion of the "docs_with_postcode_outside" the Boston area, we can see some that of the postcodes have been
# formatted differently, for e.g. "02110-1301", and thus needs to be edited to get an accurate count.
set_code = set()
for index, area in zip(range(200), docs_with_postcode_outside_details):
    address = area['address']
    if 'postcode' in address:
        set_code.add(address['postcode'])

# You can uncomment the below print statement to view a sample of such zip codes
# pprint.pprint(set_code)

# Edit the zip codes to 5-digit values by removing any hypens or any preceding characters like "MA", to get a count on unique zip codes from the documents
set_postcodes = set()
for area in db.boston_massachusetts.find({"address.postcode" : {"$exists" : True}}):
    postcode = area['address']['postcode']
    type_1 = re.compile("-")
    type_2 = re.compile("MA ")
    if type_1.search(postcode):
        pos = type_1.search(postcode).start()
        postcode = postcode[:pos]
    if type_2.search(postcode):
        postcode = postcode[3:]
    set_postcodes.add(postcode)

print
print "Unique postcodes in the documents:", len(set_postcodes)
print "All of the Boston area postcodes:", len(boston_zip_codes)
print "Postcodes from the documents belonging to the Boston area:", len(set_postcodes.intersection(boston_zip_codes))
print "Postcodes not belonging to the Boston area:", len((set_postcodes) - set(boston_zip_codes))
print

# Most mentioned postal codes in the documents
most_mentioned_postal_codes = db.boston_massachusetts.aggregate([{"$match" : {"address.postcode" : {"$exists" : True}}},
                                                                 {"$group" : {"_id" : "$address.postcode",
                                                                              "count" : {"$sum" : 1}}},
                                                                 {"$sort" : {"count" : -1}},
                                                                 {"$limit" : 10}])

print "10 most mentioned zip codes:"
print "----------------------------"
for data in most_mentioned_postal_codes:
    print data['_id'], " --> ", data['count']

# The most mentioned postal code - 02139, doesn't come under Boston but is actually in Cambridge, MA.

###########################################
##################RESULT##################
###########################################

'''
Documents with "postcode" in the "address" section: 1593
Documents with "postcode" in the Boston area: 833
Documents with "postcode" outside the Boston area: 760

Unique postcodes in the documents: 75
All of the Boston area postcodes: 62
Postcodes from the documents belonging to the Boston area: 40
Postcodes not belonging to the Boston area: 35

10 most mentioned zip codes:
----------------------------
02139  -->  218
02135  -->  161
02130  -->  105
02144  -->  63
02474  -->  63
02114  -->  49
02215  -->  46
02116  -->  43
02143  -->  40
02138  -->  39
'''