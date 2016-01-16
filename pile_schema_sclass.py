#!/usr/bin/env python

#
# Generated Sat Jan 16 13:39:50 2016 by generateDS.py version 2.17a.
#
# Command line options:
#   ('-s', 'H:\\prog\\piles\\dbstruct\\src\\dbstruct\\pile_schema_sclass.py')
#   ('--cleanup-name-list', "[(':', '__'), ('-', '___'), ('\\\\.', '____'), ('^int$', 'integer')]")
#   ('--member-specs', 'dict')
#   ('--super', 'pile_schema_api')
#   ('--no-questions', '')
#   ('-f', '')
#   ('-o', 'H:\\prog\\piles\\dbstruct\\src\\dbstruct\\pile_schema_api.py')
#
# Command line arguments:
#   H:\prog\piles\dbstruct\src\dbstruct\PileSchema.xsd
#
# Command line:
#   C:\pf\Python27\Scripts\generateDS.py -s "H:\prog\piles\dbstruct\src\dbstruct\pile_schema_sclass.py" --cleanup-name-list="[(':', '__'), ('-', '___'), ('\\.', '____'), ('^int$', 'integer')]" --member-specs="dict" --super="pile_schema_api" --no-questions -f -o "H:\prog\piles\dbstruct\src\dbstruct\pile_schema_api.py" H:\prog\piles\dbstruct\src\dbstruct\PileSchema.xsd
#
# Current working directory (os.getcwd()):
#   dbstruct
#

import sys
from lxml import etree as etree_

import pile_schema_api as supermod

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

ExternalEncoding = 'ascii'

#
# Data representation classes
#


class parameterlessTypeSub(supermod.parameterlessType):
    def __init__(self):
        super(parameterlessTypeSub, self).__init__()
supermod.parameterlessType.subclass = parameterlessTypeSub
# end class parameterlessTypeSub


class identitySub(supermod.identity):
    def __init__(self, seed=None, increment=None, notForReplication=None):
        super(identitySub, self).__init__(seed, increment, notForReplication, )
supermod.identity.subclass = identitySub
# end class identitySub


class bitSub(supermod.bit):
    def __init__(self, default=None, defaultExpression=None, sqltype='BOOLEAN', qtype='bool'):
        super(bitSub, self).__init__(default, defaultExpression, sqltype, qtype, )
supermod.bit.subclass = bitSub
# end class bitSub


class tristateSub(supermod.tristate):
    def __init__(self, default=None, defaultExpression=None, sqltype='SMALLINT', qtype='char'):
        super(tristateSub, self).__init__(default, defaultExpression, sqltype, qtype, )
supermod.tristate.subclass = tristateSub
# end class tristateSub


class integerSub(supermod.integer):
    def __init__(self, default=None, defaultExpression=None, sqltype='INTEGER', qtype='int', identity=None, valueOf_=None):
        super(integerSub, self).__init__(default, defaultExpression, sqltype, qtype, identity, )
supermod.integer.subclass = integerSub
# end class integerSub


class bigintSub(supermod.bigint):
    def __init__(self, default=None, defaultExpression=None, sqltype='BIGINT', qtype='long', identity=None):
        super(bigintSub, self).__init__(default, defaultExpression, sqltype, qtype, identity, )
supermod.bigint.subclass = bigintSub
# end class bigintSub


class smallintSub(supermod.smallint):
    def __init__(self, default=None, defaultExpression=None, sqltype='SMALLINT', qtype='short', identity=None):
        super(smallintSub, self).__init__(default, defaultExpression, sqltype, qtype, identity, )
supermod.smallint.subclass = smallintSub
# end class smallintSub


class tinyintSub(supermod.tinyint):
    def __init__(self, default=None, defaultExpression=None, sqltype='SMALLINT', qtype='char', identity=None):
        super(tinyintSub, self).__init__(default, defaultExpression, sqltype, qtype, identity, )
supermod.tinyint.subclass = tinyintSub
# end class tinyintSub


class choiceItemSub(supermod.choiceItem):
    def __init__(self, label='', id=None, name=None):
        super(choiceItemSub, self).__init__(label, id, name, )
supermod.choiceItem.subclass = choiceItemSub
# end class choiceItemSub


class choiceSub(supermod.choice):
    def __init__(self, default=None, defaultExpression=None, sqltype='INTEGER', qtype='int', item=None):
        super(choiceSub, self).__init__(default, defaultExpression, sqltype, qtype, item, )
supermod.choice.subclass = choiceSub
# end class choiceSub


class float_Sub(supermod.float_):
    def __init__(self, default=None, qtype='float', sqltype='FLOAT', mantissaBits=None, defaultExpression=None, valueOf_=None):
        super(float_Sub, self).__init__(default, qtype, sqltype, mantissaBits, defaultExpression, )
supermod.float_.subclass = float_Sub
# end class float_Sub


class realSub(supermod.real):
    def __init__(self, default=None, defaultExpression=None, sqltype='REAL', qtype='double'):
        super(realSub, self).__init__(default, defaultExpression, sqltype, qtype, )
supermod.real.subclass = realSub
# end class realSub


class decimalSub(supermod.decimal):
    def __init__(self, defaultExpression=None, scale=None, default=None, precision=None, sqltype='DECIMAL', qtype='double', valueOf_=None):
        super(decimalSub, self).__init__(defaultExpression, scale, default, precision, sqltype, qtype, )
supermod.decimal.subclass = decimalSub
# end class decimalSub


class decimalScale0Sub(supermod.decimalScale0):
    def __init__(self, default=None, defaultExpression=None, sqltype='DECIMAL', qtype='double', precision=None, identity=None):
        super(decimalScale0Sub, self).__init__(default, defaultExpression, sqltype, qtype, precision, identity, )
supermod.decimalScale0.subclass = decimalScale0Sub
# end class decimalScale0Sub


class moneySub(supermod.money):
    def __init__(self, default=None, defaultExpression=None, sqltype='DECIMAL', qtype='double'):
        super(moneySub, self).__init__(default, defaultExpression, sqltype, qtype, )
supermod.money.subclass = moneySub
# end class moneySub


class parameterlessStringTypeSub(supermod.parameterlessStringType):
    def __init__(self, defaultExpression=None, default=None, sqltype='VARCHAR', qtype='QString'):
        super(parameterlessStringTypeSub, self).__init__(defaultExpression, default, sqltype, qtype, )
supermod.parameterlessStringType.subclass = parameterlessStringTypeSub
# end class parameterlessStringTypeSub


class uniqueidentifierSub(supermod.uniqueidentifier):
    def __init__(self, default=None, defaultExpression=None, sqltype='VARCHAR', qtype='QString'):
        super(uniqueidentifierSub, self).__init__(default, defaultExpression, sqltype, qtype, )
supermod.uniqueidentifier.subclass = uniqueidentifierSub
# end class uniqueidentifierSub


class dateTypeSub(supermod.dateType):
    def __init__(self, default=None, defaultExpression=None, sqltype='DATE', qtype='QDate'):
        super(dateTypeSub, self).__init__(default, defaultExpression, sqltype, qtype, )
supermod.dateType.subclass = dateTypeSub
# end class dateTypeSub


class timeTypeSub(supermod.timeType):
    def __init__(self, default=None, defaultExpression=None, sqltype='TIME', qtype='QTime'):
        super(timeTypeSub, self).__init__(default, defaultExpression, sqltype, qtype, )
supermod.timeType.subclass = timeTypeSub
# end class timeTypeSub


class dateTimeTypeSub(supermod.dateTimeType):
    def __init__(self, default=None, defaultExpression=None, sqltype='VARCHAR', qtype='QDateTime'):
        super(dateTimeTypeSub, self).__init__(default, defaultExpression, sqltype, qtype, )
supermod.dateTimeType.subclass = dateTimeTypeSub
# end class dateTimeTypeSub


class charSub(supermod.char):
    def __init__(self, defaultExpression=None, default=None, length=None, sqltype='CHARACTER', qtype='QString'):
        super(charSub, self).__init__(defaultExpression, default, length, sqltype, qtype, )
supermod.char.subclass = charSub
# end class charSub


class binarySub(supermod.binary):
    def __init__(self, length=None, sqltype='VARBINARY', qtype='QByteArray'):
        super(binarySub, self).__init__(length, sqltype, qtype, )
supermod.binary.subclass = binarySub
# end class binarySub


class ncharSub(supermod.nchar):
    def __init__(self, defaultExpression=None, default=None, length=None, sqltype='VARCHAR', qtype='QByteArray'):
        super(ncharSub, self).__init__(defaultExpression, default, length, sqltype, qtype, )
supermod.nchar.subclass = ncharSub
# end class ncharSub


class vrtcolSub(supermod.vrtcol):
    def __init__(self, dynamic=False, references=None):
        super(vrtcolSub, self).__init__(dynamic, references, )
supermod.vrtcol.subclass = vrtcolSub
# end class vrtcolSub


class columnSub(supermod.column):
    def __init__(self, foreignInsert='id', name=None, foreignTable=None, label=None, allowNulls=True, readOnly=False, foreignBehavior='choose', foreignColumn='id', userformat='', bit=None, tristate=None, integer=None, bigint=None, smallint=None, tinyint=None, choice=None, numeric=None, decimal=None, numericScale0=None, decimalScale0=None, money=None, float_=None, real=None, date=None, datetime=None, time=None, char=None, varchar=None, text=None, nchar=None, nvarchar=None, ntext=None, binary=None, varbinary=None, image=None, xml=None, vrtcol=None):
        super(columnSub, self).__init__(foreignInsert, name, foreignTable, label, allowNulls, readOnly, foreignBehavior, foreignColumn, userformat, bit, tristate, integer, bigint, smallint, tinyint, choice, numeric, decimal, numericScale0, decimalScale0, money, float_, real, date, datetime, time, char, varchar, text, nchar, nvarchar, ntext, binary, varbinary, image, xml, vrtcol, )
supermod.column.subclass = columnSub
# end class columnSub


class columnListSub(supermod.columnList):
    def __init__(self, column=None):
        super(columnListSub, self).__init__(column, )
supermod.columnList.subclass = columnListSub
# end class columnListSub


class constraintColumnSub(supermod.constraintColumn):
    def __init__(self, name=None, sortOrder=None):
        super(constraintColumnSub, self).__init__(name, sortOrder, )
supermod.constraintColumn.subclass = constraintColumnSub
# end class constraintColumnSub


class constraintSub(supermod.constraint):
    def __init__(self, clustered=None, padIndex=None, fillFactor=None, name=None, column=None, extensiontype_=None):
        super(constraintSub, self).__init__(clustered, padIndex, fillFactor, name, column, extensiontype_, )
supermod.constraint.subclass = constraintSub
# end class constraintSub


class primaryKeySub(supermod.primaryKey):
    def __init__(self, key=None):
        super(primaryKeySub, self).__init__(key, )
supermod.primaryKey.subclass = primaryKeySub
# end class primaryKeySub


class uniqueConstraintsSub(supermod.uniqueConstraints):
    def __init__(self, constraint=None):
        super(uniqueConstraintsSub, self).__init__(constraint, )
supermod.uniqueConstraints.subclass = uniqueConstraintsSub
# end class uniqueConstraintsSub


class indexSub(supermod.index):
    def __init__(self, clustered=None, padIndex=None, fillFactor=None, name=None, column=None, unique=None):
        super(indexSub, self).__init__(clustered, padIndex, fillFactor, name, column, unique, )
supermod.index.subclass = indexSub
# end class indexSub


class indexesSub(supermod.indexes):
    def __init__(self, index=None):
        super(indexesSub, self).__init__(index, )
supermod.indexes.subclass = indexesSub
# end class indexesSub


class relationshipColumnSub(supermod.relationshipColumn):
    def __init__(self, name=None):
        super(relationshipColumnSub, self).__init__(name, )
supermod.relationshipColumn.subclass = relationshipColumnSub
# end class relationshipColumnSub


class foreignKeyColumnsSub(supermod.foreignKeyColumns):
    def __init__(self, column=None):
        super(foreignKeyColumnsSub, self).__init__(column, )
supermod.foreignKeyColumns.subclass = foreignKeyColumnsSub
# end class foreignKeyColumnsSub


class primaryKeyTableSub(supermod.primaryKeyTable):
    def __init__(self, name=None, column=None):
        super(primaryKeyTableSub, self).__init__(name, column, )
supermod.primaryKeyTable.subclass = primaryKeyTableSub
# end class primaryKeyTableSub


class relationshipSub(supermod.relationship):
    def __init__(self, name=None, foreignKeyColumns=None, primaryKeyTable=None):
        super(relationshipSub, self).__init__(name, foreignKeyColumns, primaryKeyTable, )
supermod.relationship.subclass = relationshipSub
# end class relationshipSub


class relationshipsSub(supermod.relationships):
    def __init__(self, relationship=None):
        super(relationshipsSub, self).__init__(relationship, )
supermod.relationships.subclass = relationshipsSub
# end class relationshipsSub


class tableSub(supermod.table):
    def __init__(self, name=None, columns=None, primaryKey=None, uniqueConstraints=None, indexes=None, relationships=None):
        super(tableSub, self).__init__(name, columns, primaryKey, uniqueConstraints, indexes, relationships, )
supermod.table.subclass = tableSub
# end class tableSub


class tablesSub(supermod.tables):
    def __init__(self, table=None):
        super(tablesSub, self).__init__(table, )
supermod.tables.subclass = tablesSub
# end class tablesSub


class viewSubsetSub(supermod.viewSubset):
    def __init__(self, constraint=None, name1=None, value=None, col1=None, in_=None, incol=None, where=None):
        super(viewSubsetSub, self).__init__(constraint, name1, value, col1, in_, incol, where, )
supermod.viewSubset.subclass = viewSubsetSub
# end class viewSubsetSub


class viewWriteBackColSub(supermod.viewWriteBackCol):
    def __init__(self, default=None, name=None, value=None):
        super(viewWriteBackColSub, self).__init__(default, name, value, )
supermod.viewWriteBackCol.subclass = viewWriteBackColSub
# end class viewWriteBackColSub


class viewWriteBackSub(supermod.viewWriteBack):
    def __init__(self, table=None, column=None):
        super(viewWriteBackSub, self).__init__(table, column, )
supermod.viewWriteBack.subclass = viewWriteBackSub
# end class viewWriteBackSub


class viewSub(supermod.view):
    def __init__(self, name=None, subset=None, writeback=None):
        super(viewSub, self).__init__(name, subset, writeback, )
supermod.view.subclass = viewSub
# end class viewSub


class viewsSub(supermod.views):
    def __init__(self, view=None):
        super(viewsSub, self).__init__(view, )
supermod.views.subclass = viewsSub
# end class viewsSub


class databaseSub(supermod.database):
    def __init__(self, username=None, name=None, driver=None, host=None, path=None, password=None, port=None, tables=None, views=None):
        super(databaseSub, self).__init__(username, name, driver, host, path, password, port, tables, views, )
supermod.database.subclass = databaseSub
# end class databaseSub


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
        rootTag = 'parameterlessType'
        rootClass = supermod.parameterlessType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:dbsm="http://pile-contributors.github.io/database/PileSchema.xsd"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'parameterlessType'
        rootClass = supermod.parameterlessType
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
        rootTag = 'parameterlessType'
        rootClass = supermod.parameterlessType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:dbsm="http://pile-contributors.github.io/database/PileSchema.xsd"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'parameterlessType'
        rootClass = supermod.parameterlessType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from pile_schema_api import *\n\n')
        sys.stdout.write('import pile_schema_api as model_\n\n')
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
