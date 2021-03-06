#!/usr/bin/env python

#   Import required modules from standard Python library
import os
import sys
import re
import itertools
from multiprocessing import Pool

#   Import functions defined in another script bundled with this package
import Miscellaneous_Utilities.annotation_utilities as annotation_utilities

#   Create two regex objects for determining given and desired file extensions
gff = re.compile(ur'(.*\.gff$)')
bed = re.compile(ur'(.*\.bed$)')


#   Determine how to annotate the pseudoscaffold and do so
def parallelized_wrapper(seq_list, unique, annotation, pseudoscaffold, reference, temppath, bconf, database_name, pseudopath, args):
    #   Figure out what reference annotation file we have
    find_gff, find_bed = annotation_utilities.extension_searcher(gff, bed, args['annotation'])
    #   Figure out what pseudoscaffold annotation file we are making
    create_gff, create_bed = annotation_utilities.extension_creator(gff, bed, args['outfile'])
    """Annotate the pseudoscaffold"""
    annotation, reference, pseudoscaffold = annotation_utilities.opener(args['annotation'], args['reference'], args['pseudoscaffold'])
    if find_gff and create_gff:
        print "Found GFF file, making GFF file"
        import GFF_Utilities.gff_to_gff as gff_to_gff
        out = str(unique + '_out.gff')
        gff_annotate = gff_to_gff.gffGFF(eq_list, unique, reference, annotation, pseudoscaffold, out, temppath, bconf, database_name, pseudopath)
        gff_annotate.gff_to_gff()
    elif find_gff and create_bed:
        print "Found GFF file, making BED file"
        import GFF_Utilities.gff_to_bed as gff_to_bed
        out = str(unique + '_out.bed')
        bed_annotate = gff_to_bed.gffBED(seq_list, unique, reference, annotation, pseudoscaffold, out, temppath, bconf, database_name, pseudopath)
        bed_annotate.gff_to_bed()
    elif find_bed and create_gff:
        print "Found BED file, making GFF file"
        import BED_Utilities.bed_to_gff as bed_to_gff
        pass
    elif find_bed and create_bed:
        print "Found BED file, making BED file"
        import BED_Utilities.bed_to_bed as bed_to_bed
        pass
    else:
        sys.exit("Could determine neither file format of input nor desired format of output file. Please make sure extensions are typed out fully.")


#   Split the arguments
def args_wrapper(args):
    """Split the arguments"""
    return(parallelized_wrapper(*args))
    # return(test_wrapper(*args))



def test_wrapper(seq_list, unique, annotation, pseudoscaffold, reference, temppath, bconf, database_name, pseudopath, args):
    print seq_list
    print unique
    print temppath
    print bconf
    print database_name
    print pseudopath
    print args
    return