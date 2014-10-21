#!/usr/bin/env python

import stix
import argparse

def main():
    parser = argparse.ArgumentParser ( description = "Take a set of Cybox patterns contained in STIX find Cybox instances matching them" 
    , formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument("stix_file", nargs='*', help="An input file containing Cybox observable instances and/or patterns", default = "in.xml")
    args = parser.parse_args()

# TODO read in 1..n files - at least one must have at least one pattern. 
    # XXX parse each package in each file
    
    print args.stix_file
# TODO build dict of all observable patterns (and dict of instances) in files
    # XXX use from_xml to turn into object, then check each for condition
    # for each file, for each package: instances.append(pkg.observables), patterns.append(pkg.indicators.observables)

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