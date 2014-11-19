#!/usr/bin/env python

from stix.core import STIXPackage
import argparse
import sys

from cybox.core import Observable

def is_pattern(obj):
# cybox 'patterns' must have conditions on all fields
    has_conditions = False
    #  return a dict of fields with a condition, and the type of condition
    if isinstance(obj,dict):
        for key in obj.keys():
            #print "DBG: " + "|" + str(key) + "|"
            if str(key) == 'condition':
#                print "DBG found condition " + obj[key]
                return True
            else :
                has_conditions = is_pattern( obj[key] ) or has_conditions
    return has_conditions

def compare_objects(pattern, instance):
    # attempt to match each field in pattern on accompanying field in instance
    # this includes the "Type", for apples/apples comparison
    match = False

    for field in pattern.keys():

        # XXX handle lists of things under a single property (multiple IPs)
        if isinstance (pattern[field], list):
            pat_item = pattern[field][0] 
            ins_item = instance[field][0]
        elif isinstance(pattern[field],dict):
            pat_item = pattern[field]
            ins_item = instance[field]
        else:
            # not a dictionary, so no 'condition' to be had
            continue
        
        if not 'value' in pat_item:
            # this is a wrapper element, need to go deeper
            compare_objects(pat_item,ins_item)
            continue
        else:
            # can meaningfully compare fields
            patval = str(pat_item['value'])
            cond = str(pat_item['condition'])
            insval = str(ins_item)
        
            # handle conditions ExclusiveBetween, or InclusiveBetween)
            # XXX handle apply_condition
    
            if cond == 'Equals':
                if insval == patval:
                    match = True

            
            elif cond == 'Contains':
                if insval in patval:
                    match = True

            elif cond == "StartsWith":
                if insval.startswith (patval):
                    match = True

            elif cond == "EndsWith":
                if insval.endswith (patval):
                    match = True

            elif cond == "GreaterThan":
                if  insval > patval:
                    match = True

            elif cond == "GreaterThanOrEqual":
                if  insval >= patval:
                    match = True

            elif cond == "LessThan":
                if  insval < patval:
                    match = True

            elif cond == "LessThanOrEqual":
                if  insval <= patval:
                    match = True

            else:
                    print "DBG: no match on " + patval
                    break

    return match

def main():
    parser = argparse.ArgumentParser ( description = "Take a set of Cybox patterns and find Cybox instances matching them" 
    , formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument("stix_file", nargs='*', help="An input file with a STIX package containing Cybox observable instances and/or patterns", default = ["in.xml"])
    args = parser.parse_args()

    #  read in 1..n STIX XML files, assuming each one has a package
    patterns = []
    instances = []
    for infile in args.stix_file:
        # parse each package in each file
        fd = open(infile)
        pkg = STIXPackage.from_xml(fd)
        
        # store all patterns from input xml file
        for node in pkg.walk():
            if isinstance (node, Observable):
                obs = node.to_dict()
                if 'observable_composition' in obs:
                    print "LOG Ignoring observable wrapper " + obs['id']
                else:
                    obj = obs['object']
                
                    has_conditions = is_pattern(obj) 
                      
                    if has_conditions:
                        patterns.append(obj)
                    else:
                        instances.append(obj)
    if not patterns:
        sys.exit ("Please specify at least one pattern - exiting")
        
    for pattern in patterns:
        for instance in instances:
            match = compare_objects(pattern['properties'],instance['properties'])
            if match:
                print "OUT: matched " +  str(pattern['id']) + " on " + instance['id']
            
        
if __name__ == '__main__':
    main()
