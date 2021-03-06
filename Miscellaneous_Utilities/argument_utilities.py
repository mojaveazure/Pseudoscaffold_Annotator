#!/usr/bin/env python

#   Import required modules from standard Python library
import argparse
import os


#   Set rootpath to current working directory
rootpath = os.getcwd()


#   Set and parse arguments
def set_args():
    """Set and parse the arguments here. There are three subroutines for this package:
        fix             Fix a pseudoscaffold file to be used by the annotator
        blast-config    Set the default arguments for BLAST to be used by the annotator
        annotate        Run the annotator itself"""
    #   Define the arguments
    Arguments = argparse.ArgumentParser(add_help=True)
    Sub_Args = Arguments.add_subparsers(help='Choose what to do', dest='command')
    #   Add parser for fixing pseudoscaffold
    Fix_Arguments = Sub_Args.add_parser('fix', help='Fix an input pseudoscaffold for use with the annotator')
    Fix_Arguments.add_argument('-p',
        '--pseudoscaffold',
        dest='pseudoscaffold',
        type=str,
        default=None,
        metavar='PSEUDOSCAFFOLD FASTA',
        help="Pseudoscaffold to be fixed")
    Fix_Arguments.add_argument('-n',
        '--new-pseudoscaffold',
        dest='new_pseudoscaffold',
        type=str,
        default='fixed_pseudoscaffolds.fasta',
        metavar='FIXED PSEUDOSCAFFOLD',
        help="Name of fixed pseudoscaffold. Please put full file name, inlcuding extension. Default is 'fixed_pseudoscaffolds.fasta'")
    #   Add parser for setting BLAST defaults
    Blast_Arguments = Sub_Args.add_parser('blast-config', help='Set defaults for BLAST to be used by the annotator')
    Blast_Arguments.add_argument('-o',
        '--outfile',
        type=str,
        dest='outfile',
        default=None,
        metavar='BLAST RESULTS',
        help="Path to BLAST results if you wish to keep them, defaults to a temporary file")
    Blast_Arguments.add_argument('-d',
        '--database-name',
        type=str,
        dest='db_name',
        default=None,
        metavar='DATABASE NAME',
        help='Name of BLAST database, defaults to name of pseudoscaffold')
    Blast_Arguments.add_argument('-v',
        '--override',
        type=bool,
        dest='override',
        default=False,
        metavar='OVERRIDE',
        help="Override a blast database if found? Defaults to 'False'")
    Blast_Arguments.add_argument('-c',
        '--config',
        dest='config',
        default=rootpath+'/blast_config',
        metavar='BLAST CONFIG FILE',
        help="Full path to the BLAST configuration file. Defaults to "+rootpath+"/blast_config")
    #   Add parser for the annotator
    Annotate_Arguments = Sub_Args.add_parser('annotate', help='Annotate an input pseudoscaffold')
    Annotate_Arguments.add_argument('-r',
        '--reference',
        type=str,
        dest='reference',
        default=None,
        metavar='REFERENCE FASTA',
        help="Input reference FASTA file")
    Annotate_Arguments.add_argument('-a',
        '--annotation',
        type=str,
        dest='annotation',
        default=None,
        metavar='ANNOTATION',
        help="Annotation file for reference FASTA")
    Annotate_Arguments.add_argument('-p',
        '--pseudoscaffold',
        type=str,
        dest='pseudoscaffold',
        default=None,
        metavar='PSEUDOSCAFFOLD FASTA',
        help="Pseudoscaffold to be annotated")
    Annotate_Arguments.add_argument('-o',
        '--outfile',
        type=str,
        dest='outfile',
        default='pseudoscaffold_annotations.gff',
        metavar='OUTFILE',
        help="Desired name of output annotation file. Please put full file name, including extension. Defalt is 'pseudoscaffold_annotations.gff'")
    Annotate_Arguments.add_argument('-c',
        '--config',
        dest='cfile',
        default=rootpath+'/blast_config',
        metavar='BLAST CONFIG FILE',
        help="Full path the BLAST configuration file.")
    Annotate_Arguments.add_argument('-t',
        '--threads',
        dest='procs',
        type=int,
        default=2,
        metavar='NUMBER OF PROCESSES',
        help="How many processes are we starting to run in parallel?")
    #   Add parser for the subsetter
    Subset_Arguments = Sub_Args.add_parser('subset', help='Subset an annotation file randomly')
    Subset_Arguments.add_argument('-a',
        '--annotation',
        type=str,
        dest='annotation',
        default=None,
        metavar='ANNOTATION',
        help="Annotation file for subsetting")
    Subset_Arguments.add_argument('-d',
        '--desired-subset',
        type=int,
        dest='desired',
        default=None,
        metavar='DESIRED SUBSET',
        help='Number of contigs to subset out')
    Subset_Arguments.add_argument('-o',
        '--out',
        type=str,
        dest='out',
        default='subsetAnnotations',
        metavar='OUTFILE',
        help="Desired name, WITHOUT the extension, of the subsetted annotation file. The extension will be added automatcially based off of the input annotaiton file. Defaults to 'subsetAnnotations'")
    #   Parse the arguments
    args = Arguments.parse_args()
    return(args)


#   Usage message
def Usage():
    """Prints usage message"""
    print'''Usage: ./pseudoscaffold_annotator.py <subroutine>
where: <subroutine> is one of
        fix
        blast-config
        annotate
        subset

The 'annotate' subroutine creates a GFF annotation file
for an assembled pseudoscaffold fasta file based off a
reference fasta file and GFF annotation file for the
reference fasta file. Support for the BED format
will be included in a later release.

This program requires bedtools, BioPython and NCBI's BLAST+
excecutables to be installed andfound within the system path.
Please do this before running pseudoscaffold_annotator.py

To configure the parameters for the BLAST search,
use the 'blast-config' subroutine to generate a new
configuration file to be used by pseudoscaffold_annotator.py

The 'subset' subroutine creates a random subset of an
annotation file. Currently, this subroutine only supports
GFF annotation files.

***IMPORTANT***
pseudoscaffold_annotator.py requires no new lines
within the sequence of the pseudoscaffold.
The following is not an allowed sequence:
        >pseudoscaffold
        ACTGTCAG
        GCTATCGA

The 'fix' subroutine removes new lines
between sequence data, creating a fasta
file that reads like:
        >pseudoscaffold
        ACTGTCAGGCTATCGA
'''
    return
