#!/usr/bin/env python

#
# Generated  by generateDS.py.
#
# Command line options:
#   ('-p', 'pile_sch_')
#   ('--subclass-suffix', '_sub')
#   ('-m', '')
#   ('-f', '')
#   ('--no-dates', '')
#   ('--no-versions', '')
#   ('--no-questions', '')
#   ('--external-encoding', 'utf-8')
#   ('--member-specs', 'dict')
#   ('--cleanup-name-list', "[(':', '__'), ('-', '___'), ('\\\\.', '____'), ('^int$', 'integer')]")
#   ('--use-getter-setter', 'new')
#   ('--super', 'dbstructpy.pileschema_drc')
#   ('-o', 'dbstructpy\\pileschema_drc.py')
#   ('-s', 'dbstructpy\\pileschema_subclasses.py')
#
# Command line arguments:
#   H:\prog\piles\dbstruct\src\dbstruct\dbstructpy\bin\\..\share\dbstruct.xsd
#
# Command line:
#   K:\pf\Anaconda2\python.exe\..\scripts\generateDS.py -p "pile_sch_" --subclass-suffix="_sub" -m -f --no-dates --no-versions --no-questions --external-encoding="utf-8" --member-specs="dict" --cleanup-name-list="[(':', '__'), ('-', '___'), ('\\.', '____'), ('^int$', 'integer')]" --use-getter-setter="new" --super="dbstructpy.pileschema_drc" -o "dbstructpy\pileschema_drc.py" -s "dbstructpy\pileschema_subclasses.py" H:\prog\piles\dbstruct\src\dbstruct\dbstructpy\bin\\..\share\dbstruct.xsd
#
# Current working directory (os.getcwd()):
#   dbstructpy
#

import sys
from lxml import etree as etree_

import dbstructpy.pileschema_drc as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'utf-8'

#
# Data representation classes
#


class pile_sch_tables_sub(supermod.pile_sch_tables):
    def __init__(self):
        super(pile_sch_tables_sub, self).__init__()
supermod.pile_sch_tables.subclass = pile_sch_tables_sub
# end class pile_sch_tables_sub


class pile_sch_views_sub(supermod.pile_sch_views):
    def __init__(self):
        super(pile_sch_views_sub, self).__init__()
supermod.pile_sch_views.subclass = pile_sch_views_sub
# end class pile_sch_views_sub


class pile_sch_bootstrap_sub(supermod.pile_sch_bootstrap):
    def __init__(self):
        super(pile_sch_bootstrap_sub, self).__init__()
supermod.pile_sch_bootstrap.subclass = pile_sch_bootstrap_sub
# end class pile_sch_bootstrap_sub


class pile_sch_database_sub(supermod.pile_sch_database):
    def __init__(self, tables=None, views=None, bootstrap=None):
        super(pile_sch_database_sub, self).__init__(tables, views, bootstrap, )
supermod.pile_sch_database.subclass = pile_sch_database_sub
# end class pile_sch_database_sub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'tables'
        rootClass = supermod.pile_sch_tables
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:dbsm="http://pile-contributors.github.io/trunk/dbstruct.xsd"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'tables'
        rootClass = supermod.pile_sch_tables
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    from StringIO import StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'tables'
        rootClass = supermod.pile_sch_tables
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:dbsm="http://pile-contributors.github.io/trunk/dbstruct.xsd"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'tables'
        rootClass = supermod.pile_sch_tables
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from dbstructpy.pileschema_drc import *\n\n')
        sys.stdout.write('import dbstructpy.pileschema_drc as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
