#!/usr/bin/env python

#   Import required modules from standard Python library
import os
import sys
import re

#   Import functions from the multiprocessing module
from multiprocessing import Process, Lock

#   Import functions defined in another script bundled with this package
import Pseudoscaffold_Utilities.pseudoscaffold_tools as pseudoscaffold_tools
import Miscellaneous_Utilities.argument_utilities as argument_utilities
import Miscellaneous_Utilities.annotation_utilities as annotation_utilities

#   Create two regex objects for determining given and desired file extensions
gff = re.compile(ur'(.*\.gff$)')
bed = re.compile(ur'(.*\.bed$)')


#   Annotate the pseudoscaffold
#       Method dependent on the input and output annotation files
def pseudoscaffold_annotator(args, temppath, rootpath):
    """Start annotating the pseudoscaffold"""
    if not os.getcwd() == temppath:
        os.chdir(temppath)
    seq_list = annotation_utilities.extraction_sh(args['reference'], args['annotation'], rootpath)
    annotation, reference, pseudoscaffold = annotation_utilities.opener(args['annotation'], args['reference'], args['pseudoscaffold'])
    find_gff, find_bed = annotation_utilities.extension_searcher(gff, bed, args['annotation'])
    create_gff, create_bed = annotation_utilities.extension_creator(gff, bed, args['outfile'])
    if find_gff and create_gff:
        print "Found GFF file, making GFF file"
        import GFF_Utilities.gff_to_gff as gff_to_gff
        import GFF_Utilities.gff_extracter as gff_extracter
        contig_original, length_final = gff_extracter.contig_extracter(annotation)
        if __name__ == '__main__':
            lock = Lock()
            for unique in contig_original:
                out=str(unique+"_out.gff")
                print out
                Process(target=gff_to_gff.gff_to_gff, args=(lock, seq_list, unique, reference, annotation, pseudoscaffold, out, temppath)).start()
    elif find_gff and create_bed:
        print "Found GFF file, making BED file"
        import GFF_Utilities.gff_to_bed as gff_to_bed
        import GFF_Utilities.gff_extracter as gff_extracter
        contig_original, length_checker = gff_extracter.contig_extracter(reference, annotation)
        if __name__ == '__main__':
            lock = Lock()
            for unique in contig_original:
                out = str(unique+"_out.bed")
                pass
        pass
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

#   Do the work here
def main():
    """Read arguments, determine which subroutine to run, and run it"""
    #   No arguments give, display usage message
    if not sys.argv[1:]:
        argument_utilities.Usage()
        exit(1)
    #   Create a dictionary of arguments
    args = vars(argument_utilities.set_args())
    print(args)
    #   Run the 'fix' subroutine
    if args['command'] == 'fix':
        import Pseudoscaffold_Utilities.pseudoscaffold_fixer as pseudoscaffold_fixer
        pseudoscaffold_fixer.main(args['pseudoscaffold'], args['new_pseudoscaffold'])
    #   Run the 'blast-config' subroutine
    elif args['command'] == 'blast-config':
        import Miscellaneous_Utilities.blast_utilities as blast_utilities
        blast_utilities.make_blast_config(args)
    #   Run the 'annotate' subroutine
    elif args['command'] == 'annotate':
        rootpath, tempdir, temppath = annotation_utilities.tempdir_creator()
        pseudoscaffold_annotator(args, temppath, rootpath)
        annotation_utilities.annotation_builder(rootpath, tempdir, temppath, args['outfile'])
    #   Incorrect subroutine specified, display usage message
    else:
        argument_utilities.Usage()
        exit(1)

main()
