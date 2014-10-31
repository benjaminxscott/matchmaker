#!/usr/bin/env python

from stix.core import STIXPackage
import argparse

def group_observables(pkg):
# get all objects in package 
    for obs in pkg.observables:
        pick_observables(obs)
    
    for ind in pkg.indicators:
        # handle compositions of indicators - iterate 
        if ind.composite_indicator_expression:
            for item in ind.composite_indicator_expression:
                for nest_obs in item.observables:
                    pick_observables(nest_obs)
            
        else:  
            for obs in ind.observables:
                pick_observables(obs)
    

def pick_observables(obs):
    if obs.observable_composition :
        for item in obs.observable_composition.observables:
            instances.append(item.object_)
    else:
        # it's just a raw observable
        instances.append(obs.object_)
        
    # check related objects
    if (obs.object_) and obs.object_.related_objects :
        for rel in obs.object_.related_objects:
            instances.append(rel)
    
def match_observable(value):
    for obj in instances:
            # we only care about files with hash values
            if "File" in obj.properties._XSI_TYPE: 
                if obj.properties.hashes:
                    for digest in obj.properties.hashes:
                        # if a pattern, only check if "Equals" condition
                        if (not digest.simple_hash_value.condition) or  (digest.simple_hash_value.condition == "Equals"):
                            if str(digest) == value:
                                print "Match - "  + str(obj.id_) 

def main():
    parser = argparse.ArgumentParser ( description = "Take a set of Cybox patterns contained in STIX find Cybox instances matching them" 
    , formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument("stix_file", nargs='*', help="An input file containing Cybox observable instances and/or patterns", default = ["in.xml"])
    parser.add_argument("--digest",'-d', help="MD5 hash to find", default = '7c2ac20e179fc78f71b2aa93c744f4765ea32e30403784beaef58f20ed015be5')
    
    args = parser.parse_args()
    
    global instances
    instances = []

    #  read in 1..n STIX XML files, parsing each package
    for infile in args.stix_file:
        fd = open(infile)
        pkg = STIXPackage.from_xml(fd)
        group_observables(pkg)
        
    match_observable(args.digest)

if __name__ == '__main__':
    main()