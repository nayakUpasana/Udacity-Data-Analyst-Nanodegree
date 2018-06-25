from imports import *

# Identifying problem characters
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        k_value = element.attrib['k']
        if lower.search(k_value):
            keys["lower"] += 1
        elif lower_colon.search(k_value):
            keys["lower_colon"] += 1
        elif problemchars.search(k_value):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

def test():
    keys = process_map('boston_massachusetts.osm')
    pprint.pprint(keys)

test()

###########################################
##################RESULT##################
###########################################

'''
problemchars -- 3
lower -- 398383
other -- 19787
lower_colon -- 37812
'''