from imports import *

# Data cleanup and convert it to JSON
CREATED = ["version", "changeset", "timestamp", "user", "uid"]
mapping = {"St": "Street",
            "St.": "Street",
            "Ave" : "Avenue",
            "Ave." : "Avenue",
            "Rd." : "Road",
            "Rd" : "Road",
            "Blvd" : "Boulevard",
            "Dr" : "Drive",
            "pkwy" : "Parkway",
            "Pkwy" : "Parkway",
            "Trl" : "Trail",
            "Ln" : "Lane",
            "ct" : "Court",
            "Ct" : "Court"}

def create_dictionary(element):
    node = {}
    if element.tag == "node" or element.tag == "way" or element.tag == "relation":
        node['node_id'] = element.attrib['id']
        node['node_type'] = element.tag
        node['created'] = {}
        # The "created" attribute will store info on the 'id', 'date-time stamp', 'version' etc.
        for attributes in CREATED:
            if element.attrib[attributes]:
                node['created'][attributes] = element.attrib[attributes]
        # We check if the current tag contains "latitude" or "longitude" values, if yes then we create their respective attributes
        if 'lat' in element.attrib or 'lon' in element.attrib:
            node['pos'] = []
            latitude = element.attrib['lat']
            longitude = element.attrib['lon']
            node['pos'].append(latitude)
            node['pos'].append(longitude)
        # The "address" attribute
        node['address'] = {}
        for tag in element.iter("tag"):
            # We'll use the following, "addr_pattern" & "colon_pattern", regexes to filter out the "tags" that might contain any address related data
            addr_pattern = re.compile("addr:") # Addresses that match the "addr:" prefix, for e.g., <tag k="addr:postcode" v="02126" />
            colon_pattern = re.compile(":") # It will check if the address type begins with a colon, like <tag k=":postcode" v="02126" /> and also to check for any additional colons in the address type
            k_attrib = tag.attrib['k'] # To store the k-attribute
            value = tag.attrib['v'] # Stores the value for the k-attribute
            if k_attrib == "addr:street": # This condition will perform any kind of clean up related to street name abbreviation based on the "mapping" dictionary provided, like converting "St." to "Street" or "Ave" to "Avenue"
                name_split = value.split(' ')
                for key in mapping:
                    for word in name_split:
                        if key == word:
                            value = re.sub(r'\b%s[.,\b]?' %key, mapping[key], value)
            # If the regexes don't match with the attributes
            if addr_pattern.match(k_attrib) == None and colon_pattern.match(k_attrib) == None:
                # The following condition is to check for the attributes stored as "address" instead of "addr:", like <tag k="address" v="888 Broadway, Everett MA 02149-3199" />, here we save the postcode as a separate entity
                if k_attrib == "address":
                    node['address']['location'] = value
                    zip_code_1 = re.compile("MA, ")
                    zip_code_2 = re.compile("MA ")
                    zip_pos = 10000
                    if zip_code_1.search(value):
                        zip_pos = zip_code_1.search(value).start()+4
                    if zip_code_2.search(value):
                        zip_pos = zip_code_2.search(value).start()+3
                    zip_code = value[zip_pos:].strip(' ')
                    if len(zip_code) >= 5:
                        node['address']['postcode'] = zip_code
                else:
                    # To convert the value for "capacity" attribute from String type to Integer
                    if k_attrib == "capacity":
                        special_pattern = re.compile("~")
                        if special_pattern.match(value):
                            node[k_attrib] = int(value[1:])
                        else:
                            node[k_attrib] = int(value)
                    else:
                        node[k_attrib] = value
            # If the regexes do match, then the matched prefixes will be removed saving just the address type with their corresponding values
            else:
                if addr_pattern.match(k_attrib):
                    addr_type = k_attrib[5:]
                elif colon_pattern.match(k_attrib):
                    addr_type = k_attrib[1:]
                if not colon_pattern.search(addr_type):
                    node['address'][addr_type] = value
        # If no addresses are found for a particular tag, then it will be dropped from the dictionary
        if node['address'] == {}:
            node.pop('address', None)
        # If the tag is "way", then all of it's node references, like <nd ref="240167956" />, will be saved as a list
        if element.tag == "way":
            node['node_refs'] = []
            for tag in element.iter("nd"):
                node_refs = tag.attrib['ref']
                node['node_refs'].append(node_refs)
        # Same with "relation", all it's members, like <member ref="244444287" role="across" type="way" /> will be saved as a dictionary
        if element.tag == "relation":
            node['member_values'] = {}
            for tag in element.iter("member"):
                node['member_values']['ref'] = tag.attrib['ref']
                node['member_values']['role'] = tag.attrib['role']
                node['member_values']['type'] = tag.attrib['type']
        return node
    else:
        return None

def process_map(file_in):
    file_out = "boston_massachusetts.json".format(file_in)
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = create_dictionary(element)
            if el:
                fo.write(json.dumps(el) + "\n")

process_map('boston_massachusetts.osm')