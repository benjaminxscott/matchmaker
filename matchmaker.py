#!/usr/bin/env python

from stix.core import STIXPackage
import argparse
import sys

def main():
    parser = argparse.ArgumentParser ( description = "Take a set of Cybox patterns contained in STIX find Cybox instances matching them" 
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
        for ind in pkg.indicators:
            # TODO for each obs in each indicator
            print ind.title
            # TODO check if embedded observable has condition
        #  if ()   print "IP "+ obs['object']['properties']['ip_address']['address_value']['condition']
            # patterns.append() 
        
        # store all instances
        for obs in pkg.observables:
            instances.append(obs)
        
    # when we don't have any patterns, no point in going further
    if not patterns:
        sys.exit ("Please specify at least one pattern - exiting")
        
# TODO for each pattern, search all instances for matches
    # XXX  decide whether to generalize search, or make custom logic for each cybox object type
    # BSS leaning towards former
    # i.e.  if (item.member contains pattern.member) 
        # OR switch (type): if (file.fileext is "" and file.filename contains pattern.member), etc
    
    # XXX handle Contains and Equals (either regex or exact match)

# TODO report each match
# > FOUND instance $ID with title "Blah" matches pattern $ID in instance.xml 


# stretch: link obs to top level object for use in output (i.e. "pattern Z found observable Y in campaign X "
# stretch: dereference related obs and sightings, other edge cases

if __name__ == '__main__':
    main()