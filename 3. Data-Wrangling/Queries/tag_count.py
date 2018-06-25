from imports import *

# To count tags - Nodes, Ways, Relations
def count_tags(filename):
    tag_dictionary = {}
    attrib_value_dictionary = {}
    for event, element in ET.iterparse(filename, events = ("start",)):
        key = element.tag
        if key in tag_dictionary:
            tag_dictionary[key] += 1
        else:
            tag_dictionary[key] = 1
    
    return tag_dictionary

tags = count_tags("boston_massachusetts.osm")
print "Nodes =", tags['node']
print "Ways =", tags['way']
print "Relations =", tags['relation']

###########################################
##################RESULT##################
###########################################

'''
Nodes = 976373
Ways = 155519
Relations = 663
'''