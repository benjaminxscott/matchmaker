#!/usr/bin/env python

from stix.core import STIXPackage
import argparse
import sys

from cybox.core import Observable

def is_pattern(item):
    found = False
    if isinstance(item,dict) and found == False:
        for thing in item.keys():
            #print "DBG: " + "|" + str(thing) + "|"
            if str(thing) == 'condition':
                found = True
                break
            else :
                found = is_pattern( item[thing] )
    return found

def main():
    parser = argparse.ArgumentParser ( description = "Take a set of Cybox patterns contained in STIX and find Cybox instances matching them" 
    , formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument("stix_file", nargs='*', help="An input file containing Cybox observable instances and/or patterns", default = ["in.xml"])
    args = parser.parse_args()

    #  read in 1..n STIX XML files, assuming each one has a package
    patterns = []
    instances = []
    for infile in args.stix_file:
        # parse each package in each file
        fd = open(infile)
        pkg = STIXPackage.from_xml(fd)
        
        # store all patterns
        for node in pkg.walk():
            
            if isinstance (node, Observable):
                obs = node.to_dict()['object']
                #print obs
                
                if is_pattern(obs['properties']):
                    patterns.append(obs) 
                else:
                    instances.append(obs)
            
    
    
    print "DBG " + str(len(patterns)) + " | " + str(len(instances))
                
    # if no patterns given, no point in going further
    if not patterns:
        sys.exit ("Please specify at least one pattern - exiting")
        
# TODO for each pattern, search all instances for matches
    for thing in patterns:
        
        for doodad in instances:
            match = True
            if thing['properties']['xsi:type'] == doodad['properties']['xsi:type']:
                # check each field to see if they are the same (complete match)
                print thing
                print doodad
                for field in thing['properties'].keys():
                    # TODO if it's a dictionary, iterate through its keys
                    # else attempt to match the value
                    if str(doodad['properties'][field]) != str(thing['properties'][field]):
                        match = False
                        break
                    else:
                        print "DBG: matched on " + str(field)
                        
                print match
    
    # XXX handle partial match, if one of the fields is the same
    # XXX handle Contains as condition
    # i.e.  if (item.member contains pattern.member) 

    # XXX handle other conditions like "startswith", etc
    # XXX handle apply_condition and lists with '##comma##'
    

if __name__ == '__main__':
    main()