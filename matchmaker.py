#!/usr/bin/env python

from stix.core import STIXPackage
import argparse
import sys

def main():
    parser = argparse.ArgumentParser ( description = "Take a set of Cybox patterns contained in STIX find Cybox instances matching them" 
    , formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument("stix_file", nargs='*', help="An input file containing Cybox observable instances and/or patterns", default = ["in.xml"])
    parser.add_argument("--digest",'-d', help="MD5 hash to find", default = 'e4d909c290d0fb1ca068ffaddf22cbd0')
    
    args = parser.parse_args()
    instances = []
    
    #  read in 1..n STIX XML files, assuming each one has a package
    for infile in args.stix_file:
        # parse each package in each file
        fd = open(infile)
        pkg = STIXPackage.from_xml(fd)
    
        # get all file objects in package
        for obs in pkg.observables:
            if "File" in obs.object_.id_: 
                #print "DBG" + str(obs)
                instances.append(obs.object_)
            for rel in obs.object_.related_objects:
                if "File" in rel.id_: 
                    instances.append(rel)
                  #  print "DBG" +  str(rel.properties) + " under " + str(obs.object_.id_)
        
        # search for hash in all instances    
        for obj in instances:
                for digest in obj.properties.hashes:
                    if str(digest) == args.digest:
                        print "Match - "  + str(obj.id_) + " - " + infile

if __name__ == '__main__':
    main()