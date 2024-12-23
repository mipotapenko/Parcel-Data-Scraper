import pickle
import os.path
import re

def parse_municipality(parcel_string):
    municipality_match = re.search(r'Municipality of (.*)\n', parcel_string)
    print(municipality_match.group(1))
    return municipality_match.group(1)

def parse_swis(parcel_string):
    swis_match = re.search(r'SWIS:(.*) Tax.*', parcel_string)
    print(swis_match.group(1))
    return swis_match.group(1)

if __name__ == '__main__':
    dumpfile_name = os.path.join(os.path.realpath(os.path.dirname(__file__)), "IndexPageCorningEstimates.pickle")
    with open(dumpfile_name, 'rb') as file:
        parcel_data = pickle.load(file)

    parse_municipality(parcel_data[0])
    #print(parcel_data[0])
