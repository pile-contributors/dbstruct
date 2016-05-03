'''
Commands used in the script.

These are high level functions that take their arguments from a single object.
'''
import logging
import os
import re
from dbstructpy.pileschema_subclasses import parse
from dbstructpy import constants


LOGGER = logging.getLogger('dbstruct.command')


def list_content(args):
    '''
    Create a new pile project.
    
    TODO: implement
    '''
    tree = parse(args.file, silence=True)
    for k in dir(tree):
        print k

    LOGGER.error('Not implemented')
    pass

def create_subparsers(subparsers):
    '''
    
    '''

    parser = subparsers.add_parser(
        'list', help='print the content of an xml file')
    parser.add_argument(
        'file', action='store',
        help='The path and name of the file to examine.')
    parser.set_defaults(func=list_content)

