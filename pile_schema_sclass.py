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
#   C:\pf\Python27\Scripts\generateDS.py -s ^
#       "H:\prog\piles\dbstruct\src\dbstruct\pile_schema_sclass.py" ^
#       --cleanup-name-list="[(':', '__'), ('-', '___'), ('\\.', '____'), ('^int$', 'integer')]" ^
#       --member-specs="dict" --super="pile_schema_api" ^
#       --no-questions -f ^
#       -o "H:\prog\piles\dbstruct\src\dbstruct\pile_schema_api.py" ^
#       H:\prog\piles\dbstruct\src\dbstruct\PileSchema.xsd
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

CPP_KEYWORDS = [
    'alignas', 'alignof', 'and', 'and_eq', 'asm', 
    'auto', 'bitand', 'bitor', 'bool', 'break',
    'case', 'catch', 'char', 'char16_t', 'char32_t', 
    'class', 'compl', 'concept', 'const',
    'const_cast', 'constexpr', 'continue', 
    'decltype', 'default', 'delete', 'do',
    'double', 'dynamic_cast', 'else', 'enum', 
    'explicit', 'export', 'extern', 'false',
    'float', 'for', 'friend', 'goto', 'if', 
    'inline', 'int', 'long', 'mutable', 'namespace',
    'new', 'noexcept', 'not', 'not_eq', 
    'nullptr', 'operator', 'or', 'or_eq', 'private',
    'protected', 'public', 'register', 
    'reinterpret_cast', 'requires', 'return',
    'short', 'signed', 'sizeof', 'static', 
    'static_assert', 'static_cast', 'struct',
    'switch', 'template', 'this', 
    'thread_local', 'throw', 'true', 'try', 'typedef',
    'typeid', 'typename', 'union', 
    'unsigned', 'using', 'virtual', 'void', 'volatile',
    'wchar_t', 'while', 'xor', 'xor_eq']

# ----------------------------------------------------------------------------
# ------------------[          Custom classes          ]----------------------
# ----------------------------------------------------------------------------

class TaewMixin(object):
    '''
    Groups methods that are common to views and tables.
    '''
    def __init__(self):
        super(TaewMixin, self).__init__()
        

    @property
    def colid(self):
        '''The COLID_ for id column, if any.'''
        return self.id_column.colid \
            if hasattr(self, 'id_column') and self.id_column \
            else 'dbstruct::UNDEFINED'

    @property
    def dbcid(self):
        '''The DBC_ for this table or view.'''
        return 'DBC_%s' % self.name

    @property
    def header(self):
        '''Name of the header for this table or view.'''
        return '%s.h' % self.name.lower()

    @property
    def metaheader(self):
        '''Name of the meta header for this table or view.'''
        return '%s-meta.h' % self.name.lower()

    @property
    def var_name(self):
        '''Name of the variable holding an instance of this table or view.'''
        result = self.name.lower()
        if result in CPP_KEYWORDS:
            result = '%s_v' % result
        return result

    @property
    def class_name(self):
        '''Name of the class for this table or view.'''
        return self.name

    @property
    def nspaced_class(self):
        '''Name of the class with namespace for this table or view.'''
        return self.database.nspaced(self.class_name)

    @property
    def meta_nspaced_class(self):
        '''Name of the class with namespace for this table or view.'''
        return self.database.meta_nspaced(self.class_name)
        
# ----------------------------------------------------------------------------
# ------------------[    Data representation classes   ]----------------------
# ----------------------------------------------------------------------------

class parameterlessTypeSub(supermod.parameterlessType):

    def __init__(self):
        super(parameterlessTypeSub, self).__init__()
supermod.parameterlessType.subclass = parameterlessTypeSub
# end class parameterlessTypeSub

# ----------------------------------------------------------------------------

class identitySub(supermod.identity):

    def __init__(self, seed=None, increment=None, notForReplication=None):
        super(identitySub, self).__init__(seed, increment, notForReplication, )
supermod.identity.subclass = identitySub
# end class identitySub

# ----------------------------------------------------------------------------

class bitSub(supermod.bit):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='BOOLEAN',
            qtype='bool'):
        super(
            bitSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.bit.subclass = bitSub
# end class bitSub

# ----------------------------------------------------------------------------

class tristateSub(supermod.tristate):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='SMALLINT',
            qtype='char'):
        super(
            tristateSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.tristate.subclass = tristateSub
# end class tristateSub

# ----------------------------------------------------------------------------

class integerSub(supermod.integer):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='INTEGER',
            qtype='int',
            identity=None,
            valueOf_=None):
        super(
            integerSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
            identity,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.integer.subclass = integerSub
# end class integerSub

# ----------------------------------------------------------------------------

class bigintSub(supermod.bigint):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='BIGINT',
            qtype='long',
            identity=None):
        super(
            bigintSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
            identity,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.bigint.subclass = bigintSub
# end class bigintSub

# ----------------------------------------------------------------------------

class smallintSub(supermod.smallint):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='SMALLINT',
            qtype='short',
            identity=None):
        super(
            smallintSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
            identity,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.smallint.subclass = smallintSub
# end class smallintSub

# ----------------------------------------------------------------------------

class tinyintSub(supermod.tinyint):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='SMALLINT',
            qtype='char',
            identity=None):
        super(
            tinyintSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
            identity,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.tinyint.subclass = tinyintSub
# end class tinyintSub

# ----------------------------------------------------------------------------

class choiceItemSub(supermod.choiceItem):

    def __init__(self, label='', id=None, name=None):
        super(choiceItemSub, self).__init__(label, id, name, )
supermod.choiceItem.subclass = choiceItemSub
# end class choiceItemSub

# ----------------------------------------------------------------------------

class choiceSub(supermod.choice):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='INTEGER',
            qtype='int',
            item=None):
        super(
            choiceSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
            item,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.choice.subclass = choiceSub
# end class choiceSub

# ----------------------------------------------------------------------------

class float_Sub(supermod.float_):

    def __init__(
            self,
            default=None,
            qtype='float',
            sqltype='FLOAT',
            mantissaBits=None,
            defaultExpression=None,
            valueOf_=None):
        super(
            float_Sub,
            self).__init__(
            default,
            qtype,
            sqltype,
            mantissaBits,
            defaultExpression,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.float_.subclass = float_Sub
# end class float_Sub

# ----------------------------------------------------------------------------

class realSub(supermod.real):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='REAL',
            qtype='double'):
        super(
            realSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.real.subclass = realSub
# end class realSub

# ----------------------------------------------------------------------------

class decimalSub(supermod.decimal):

    def __init__(
            self,
            defaultExpression=None,
            scale=None,
            default=None,
            precision=None,
            sqltype='DECIMAL',
            qtype='double',
            valueOf_=None):
        super(
            decimalSub,
            self).__init__(
            defaultExpression,
            scale,
            default,
            precision,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.decimal.subclass = decimalSub
# end class decimalSub

# ----------------------------------------------------------------------------

class decimalScale0Sub(supermod.decimalScale0):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='DECIMAL',
            qtype='double',
            precision=None,
            identity=None):
        super(
            decimalScale0Sub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
            precision,
            identity,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.decimalScale0.subclass = decimalScale0Sub
# end class decimalScale0Sub

# ----------------------------------------------------------------------------

class moneySub(supermod.money):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='DECIMAL',
            qtype='double'):
        super(
            moneySub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.money.subclass = moneySub
# end class moneySub

# ----------------------------------------------------------------------------

class parameterlessStringTypeSub(supermod.parameterlessStringType):

    def __init__(
            self,
            defaultExpression=None,
            default=None,
            sqltype='VARCHAR',
            qtype='QString'):
        super(
            parameterlessStringTypeSub,
            self).__init__(
            defaultExpression,
            default,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.parameterlessStringType.subclass = parameterlessStringTypeSub
# end class parameterlessStringTypeSub

# ----------------------------------------------------------------------------

class uniqueidentifierSub(supermod.uniqueidentifier):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='VARCHAR',
            qtype='QString'):
        super(
            uniqueidentifierSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.uniqueidentifier.subclass = uniqueidentifierSub
# end class uniqueidentifierSub

# ----------------------------------------------------------------------------

class dateTypeSub(supermod.dateType):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='DATE',
            qtype='QDate'):
        super(
            dateTypeSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.dateType.subclass = dateTypeSub
# end class dateTypeSub

# ----------------------------------------------------------------------------

class timeTypeSub(supermod.timeType):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='TIME',
            qtype='QTime'):
        super(
            timeTypeSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.timeType.subclass = timeTypeSub
# end class timeTypeSub

# ----------------------------------------------------------------------------

class dateTimeTypeSub(supermod.dateTimeType):

    def __init__(
            self,
            default=None,
            defaultExpression=None,
            sqltype='VARCHAR',
            qtype='QDateTime'):
        super(
            dateTimeTypeSub,
            self).__init__(
            default,
            defaultExpression,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.dateTimeType.subclass = dateTimeTypeSub
# end class dateTimeTypeSub

# ----------------------------------------------------------------------------

class charSub(supermod.char):

    def __init__(
            self,
            defaultExpression=None,
            default=None,
            length=None,
            sqltype='CHARACTER',
            qtype='QString'):
        super(
            charSub,
            self).__init__(
            defaultExpression,
            default,
            length,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.char.subclass = charSub
# end class charSub

# ----------------------------------------------------------------------------

class binarySub(supermod.binary):

    def __init__(self, length=None, sqltype='VARBINARY', qtype='QByteArray'):
        super(binarySub, self).__init__(length, sqltype, qtype, )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.binary.subclass = binarySub
# end class binarySub

# ----------------------------------------------------------------------------

class ncharSub(supermod.nchar):

    def __init__(
            self,
            defaultExpression=None,
            default=None,
            length=None,
            sqltype='VARCHAR',
            qtype='QByteArray'):
        super(
            ncharSub,
            self).__init__(
            defaultExpression,
            default,
            length,
            sqltype,
            qtype,
        )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.nchar.subclass = ncharSub
# end class ncharSub

# ----------------------------------------------------------------------------

class vrtcolSub(supermod.vrtcol):

    def __init__(self, dynamic=False, references=None):
        super(vrtcolSub, self).__init__(dynamic, references, )
        
    def constructor(self):
        '''C++ constructor for this type'''
        return ''
        
supermod.vrtcol.subclass = vrtcolSub
# end class vrtcolSub

# ----------------------------------------------------------------------------

class columnSub(supermod.column):

    def __init__(
            self,
            foreignInsert='id',
            name=None,
            foreignTable=None,
            label=None,
            allowNulls=True,
            readOnly=False,
            foreignBehavior='choose',
            foreignColumn='id',
            userformat='',
            bit=None,
            tristate=None,
            integer=None,
            bigint=None,
            smallint=None,
            tinyint=None,
            choice=None,
            numeric=None,
            decimal=None,
            numericScale0=None,
            decimalScale0=None,
            money=None,
            float_=None,
            real=None,
            date=None,
            datetime=None,
            time=None,
            char=None,
            varchar=None,
            text=None,
            nchar=None,
            nvarchar=None,
            ntext=None,
            binary=None,
            varbinary=None,
            image=None,
            xml=None,
            vrtcol=None):
        # the kind of data this column holds
        self.datatype = None
        # the index of this column inside its table (includes virtual columns)
        self.myid = None
        # the index of this column inside database table
        self.my_real = None
        # the table this column is part of
        self.table = None
        
        super(columnSub, self).__init__(
            foreignInsert,
            name,
            foreignTable,
            label,
            allowNulls,
            readOnly,
            foreignBehavior,
            foreignColumn,
            userformat,
            bit,
            tristate,
            integer,
            bigint,
            smallint,
            tinyint,
            choice,
            numeric,
            decimal,
            numericScale0,
            decimalScale0,
            money,
            float_,
            real,
            date,
            datetime,
            time,
            char,
            varchar,
            text,
            nchar,
            nvarchar,
            ntext,
            binary,
            varbinary,
            image,
            xml,
            vrtcol,
        )

    def build(self, node):
        super(columnSub, self).build(node)
        assert(self.datatype is not None)
        #import some attributes from datatype into this level
        self.sqltype = self.dataprop.sqltype
        self.qtype = self.dataprop.qtype
        try:
            self.length = self.dataprop.length
        except AttributeError:
            self.length = None

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        super(columnSub, self).buildChildren(child_, node,
                                             nodeName_, fromsubclass_)
        # we want to have an easy way of knowing the datatype
        if nodeName_ == 'int':
            self.datatype = 'integer'
        elif nodeName_ == 'float':
            self.datatype  = 'float_'
        else:
            self.datatype = nodeName_
        # allow checking for identity in a simple manner (if self.identity: )
        try:
            self.identity = self.dataprop.identity
        except AttributeError:
            self.identity = None
        
    @property
    def default(self):
        if hasattr(self.dataprop, 'default'):
            if self.dataprop.default is not None:
                return self.dataprop.default
        if hasattr(self.dataprop, 'defaultExpression'):
            return self.dataprop.defaultExpression
        return None

    @property
    def is_foreign(self):
        return self.foreignTable is not None

    @property
    def var_name(self):
        result = self.name.lower()
        if result in CPP_KEYWORDS:
            result = '%s_v' % result
        return result

    @property
    def colid(self):
        return 'COLID_' + self.name.upper()

    @property
    def datatypeid(self):
        upp = self.datatype.upper()
        if upp == 'FLOAT_':
            upp = 'FLOAT'
        return 'DTY_%s' % upp

    @property
    def dataprop(self):
        return getattr(self, self.datatype)

    @dataprop.setter
    def dataprop(self, dataprop):
        setattr(self, self.datatype, dataprop)

    @property
    def title(self):
        return self.name if self.label is None else self.label

    @title.setter
    def title(self, title):
        self.label = title

    @property
    def qt_title(self):
        '''The title in a form allowing qt application to translate it.'''
        return 'QCoreApplication::translate("%s::%s", "%s")' % (
            self.database.name, self.table.name, self.title)

    @property
    def virtual(self):
        return self.datatype == 'vrtcol'

    @property
    def dynamic(self):
        if hasattr(self.dataprop, 'dynamic'):
            return self.dataprop.dynamic
        else:
            return False

    @property
    def database(self):
        return self.table.database

    @property
    def inttype(self):
        '''Tell if this column is some form of integer'''
        return self.qtype in int_types

    @property
    def realtype(self):
        '''Tell if this column is some form of real number'''
        return self.qtype in real_types

    @property
    def qtconstructor(self):
        return 'DbColumn::col (%-50s, %-40s, ' \
               '%4d, %-90s, %4d, %-20s, %-5s, %-5s%s)' % (
            'QLatin1String("%s")' % self.name, 
            'DbDataType::%s' % self.datatypeid, 
            self.myid, 
            self.qt_title, 
            self.my_real,
            'dbstruct::UNDEFINED' if self.length is None else str(self.length),
            'true' if self.allowNulls else 'false',
            'true' if self.readOnly else 'false',
            self.dataprop.constructor())


int_types = [
    'char', 'char', 'long', 'integer', 'int', 'short',
    'bigint', 'smallint', 'tinyint']
real_types = ['double', 'float']
supermod.column.subclass = columnSub
# end class columnSub

# ----------------------------------------------------------------------------

class columnListSub(supermod.columnList):

    def __init__(self, column=None):
        super(columnListSub, self).__init__(column, )
    
    def virtuals(self):
        '''Enumerates all virtual columns'''
        for col in self.column:
            if col.virtual:
                yield col
    
    def non_virtuals(self):
        '''Enumerates all non-virtual columns'''
        for col in self.column:
            if not col.virtual:
                yield col
        
    def filtered(self, with_id=True, only_real=True, exclude_fk=False):
        '''
        The list of column names (useful for sql statements).
        
        Parameters:
        ----------
        with_id : bool
            Is the id column to be included or not.
        only_real : bool
            Is the id column to be included or not.
        exclude_fk : bool
            Should foreign keys be excluded or not.
        '''
        def included(col):
            if only_real and col.virtual:
                return False
            if exclude_fk and col.is_foreign:
                return False
            if not with_id and col.name == 'id':
                return False
            return True
        for col in self.column:
            if included(col):
                yield col
        

    def comma_columns(self, with_id=True, only_real=True, exclude_fk=False,
                      padding='', lines=True, prefix=''):
        '''
        The list of column names (useful for sql statements).
        
        Parameters:
        ----------
        with_id : bool
            Is the id column to be included or not.
        only_real : bool
            Is the id column to be included or not.
        exclude_fk : bool
            Should foreign keys be excluded or not.
        padding : str
            String to be added before each column (spaces, for example).
        lines : bool
            Should each column be placed on its oown line or not?
        '''
        join = '\n' if lines else ''
        result = join.join(['%s"%s%s,"' % (padding, prefix, col.name)
            for col in self.filtered(with_id, only_real, exclude_fk)])
        if result.endswith(',"'):
            result = result[:-2] + '"'
        else:
            result = '""'
        return result

    def assign_columns(self, with_id=True, only_real=True, exclude_fk=False,
                      padding='', lines=True):
        '''
        The list of `col=:col` pairs (useful for sql statements).
        
        Parameters:
        ----------
        with_id : bool
            Is the id column to be included or not.
        only_real : bool
            Is the id column to be included or not.
        exclude_fk : bool
            Should foreign keys be excluded or not.
        padding : str
            String to be added before each column (spaces, for example).
        lines : bool
            Should each column be placed on its oown line or not?
        '''
        join = '\n' if lines else ''
        result = join.join(['%s"%s=:%s,"' % (padding, col.name, col.name)
            for col in self.filtered(with_id, only_real, exclude_fk)])
        if result.endswith(',"'):
            result = result[:-2] + '"'
        else:
            result = '""'
        return result
        
    def column_ids(self, with_id=True, only_real=True, exclude_fk=False,
                      padding='', lines=True):
        '''
        The list of COLID_ values.
        
        Parameters:
        ----------
        with_id : bool
            Is the id column to be included or not.
        only_real : bool
            Is the id column to be included or not.
        exclude_fk : bool
            Should foreign keys be excluded or not.
        padding : str
            String to be added before each column (spaces, for example).
        lines : bool
            Should each column be placed on its oown line or not?
        '''
        join = ',\n' if lines else ','
        result = ''.join(['%s%s%s' % (padding, col.colid, join)
            for col in self.filtered(with_id, only_real, exclude_fk)])
        return result
        
supermod.columnList.subclass = columnListSub
# end class columnListSub

# ----------------------------------------------------------------------------

class constraintColumnSub(supermod.constraintColumn):

    def __init__(self, name=None, sortOrder=None):
        super(constraintColumnSub, self).__init__(name, sortOrder, )
supermod.constraintColumn.subclass = constraintColumnSub
# end class constraintColumnSub

# ----------------------------------------------------------------------------

class constraintSub(supermod.constraint):

    def __init__(
            self,
            clustered=None,
            padIndex=None,
            fillFactor=None,
            name=None,
            column=None,
            extensiontype_=None):
        super(
            constraintSub,
            self).__init__(
            clustered,
            padIndex,
            fillFactor,
            name,
            column,
            extensiontype_,
        )
supermod.constraint.subclass = constraintSub
# end class constraintSub

# ----------------------------------------------------------------------------

class primaryKeySub(supermod.primaryKey):

    def __init__(self, key=None):
        super(primaryKeySub, self).__init__(key, )
supermod.primaryKey.subclass = primaryKeySub
# end class primaryKeySub

# ----------------------------------------------------------------------------

class uniqueConstraintsSub(supermod.uniqueConstraints):

    def __init__(self, constraint=None):
        super(uniqueConstraintsSub, self).__init__(constraint, )
supermod.uniqueConstraints.subclass = uniqueConstraintsSub
# end class uniqueConstraintsSub

# ----------------------------------------------------------------------------

class indexSub(supermod.index):

    def __init__(
            self,
            clustered=None,
            padIndex=None,
            fillFactor=None,
            name=None,
            column=None,
            unique=None):
        super(
            indexSub,
            self).__init__(
            clustered,
            padIndex,
            fillFactor,
            name,
            column,
            unique,
        )
supermod.index.subclass = indexSub
# end class indexSub

# ----------------------------------------------------------------------------

class indexesSub(supermod.indexes):

    def __init__(self, index=None):
        super(indexesSub, self).__init__(index, )
supermod.indexes.subclass = indexesSub
# end class indexesSub

# ----------------------------------------------------------------------------

class relationshipColumnSub(supermod.relationshipColumn):

    def __init__(self, name=None):
        super(relationshipColumnSub, self).__init__(name, )
supermod.relationshipColumn.subclass = relationshipColumnSub
# end class relationshipColumnSub

# ----------------------------------------------------------------------------

class foreignKeyColumnsSub(supermod.foreignKeyColumns):

    def __init__(self, column=None):
        super(foreignKeyColumnsSub, self).__init__(column, )
supermod.foreignKeyColumns.subclass = foreignKeyColumnsSub
# end class foreignKeyColumnsSub

# ----------------------------------------------------------------------------

class primaryKeyTableSub(supermod.primaryKeyTable):

    def __init__(self, name=None, column=None):
        super(primaryKeyTableSub, self).__init__(name, column, )
supermod.primaryKeyTable.subclass = primaryKeyTableSub
# end class primaryKeyTableSub

# ----------------------------------------------------------------------------

class relationshipSub(supermod.relationship):

    def __init__(
            self,
            name=None,
            foreignKeyColumns=None,
            primaryKeyTable=None):
        super(
            relationshipSub,
            self).__init__(
            name,
            foreignKeyColumns,
            primaryKeyTable,
        )
supermod.relationship.subclass = relationshipSub
# end class relationshipSub

# ----------------------------------------------------------------------------

class relationshipsSub(supermod.relationships):

    def __init__(self, relationship=None):
        super(relationshipsSub, self).__init__(relationship, )
supermod.relationships.subclass = relationshipsSub
# end class relationshipsSub

# ----------------------------------------------------------------------------

class tableSub(supermod.table, TaewMixin):

    def __init__(
            self,
            name=None,
            columns=None,
            primaryKey=None,
            uniqueConstraints=None,
            indexes=None,
            relationships=None):
        self.foreign_columns = []
        self.database = None
        self.id_column = None
        super(tableSub, self).__init__(
            name,
            columns,
            primaryKey,
            uniqueConstraints,
            indexes,
            relationships,
        )

    def build(self, node):
        super(tableSub, self).build(node)

        # make sure there is a columns element
        if self.columns is None:
            self.columns = supermod.columnList.factory()
        assert(self.columns.column is not None)
        
        # update columns
        id_counter = 0
        real_counter = 0
        for col in self.columns.column:
            # inform each column who their daddy is
            col.table = self
            # allocate indices for each column
            col.myid = id_counter
            id_counter = id_counter + 1
            # also allocate real indices for columns actually stored in db
            if col.virtual:
                col.my_real = -1
            else:
                col.my_real = real_counter
                real_counter = real_counter + 1
            # create a list with all foreign columns
            if col.is_foreign:
                self.foreign_columns.append(col)
            # find id column, if any
            if col.name == 'id' and self.id_column is None:
                self.id_column = col

    @property
    def dbtid(self):
        '''The DBT_ for this table.'''
        return 'DBT_%s' % self.name

supermod.table.subclass = tableSub
# end class tableSub

# ----------------------------------------------------------------------------

class tablesSub(supermod.tables):

    def __init__(self, table=None):
        super(tablesSub, self).__init__(table, )
supermod.tables.subclass = tablesSub
# end class tablesSub

# ----------------------------------------------------------------------------

class viewSubsetSub(supermod.viewSubset):

    def __init__(
            self,
            constraint=None,
            name1=None,
            value=None,
            col1=None,
            in_=None,
            incol=None,
            where=None):
        super(
            viewSubsetSub,
            self).__init__(
            constraint,
            name1,
            value,
            col1,
            in_,
            incol,
            where,
        )
supermod.viewSubset.subclass = viewSubsetSub
# end class viewSubsetSub

# ----------------------------------------------------------------------------

class viewWriteBackColSub(supermod.viewWriteBackCol):

    def __init__(self, default=None, name=None, value=None):
        super(viewWriteBackColSub, self).__init__(default, name, value, )
supermod.viewWriteBackCol.subclass = viewWriteBackColSub
# end class viewWriteBackColSub

# ----------------------------------------------------------------------------

class viewWriteBackSub(supermod.viewWriteBack):

    def __init__(self, table=None, column=None):
        super(viewWriteBackSub, self).__init__(table, column, )
supermod.viewWriteBack.subclass = viewWriteBackSub
# end class viewWriteBackSub

# ----------------------------------------------------------------------------

class viewSub(supermod.view, TaewMixin):
    def __init__(self, name=None, subset=None, writeback=None):
        super(viewSub, self).__init__(name, subset, writeback, )

    @property
    def dbvid(self):
        '''The DBV_ for this view.'''
        return 'DBV_%s' % self.name
        
supermod.view.subclass = viewSub
# end class viewSub

# ----------------------------------------------------------------------------

class viewsSub(supermod.views):

    def __init__(self, view=None):
        super(viewsSub, self).__init__(view, )
supermod.views.subclass = viewsSub
# end class viewsSub

# ----------------------------------------------------------------------------

class databaseSub(supermod.database):

    def __init__(
            self,
            username=None,
            name=None,
            driver=None,
            host=None,
            path=None,
            password=None,
            port=None,
            tables=None,
            views=None):
        super(databaseSub, self).__init__(
            username,
            name,
            driver,
            host,
            path,
            password,
            port,
            tables,
            views,
        )

    def build(self, node):
        super(databaseSub, self).build(node)
        # make sure we have tables objects
        if self.tables is None:
            self.tables = supermod.tables.factory()
        assert(self.tables.table is not None)
        for tbl in self.tables.table:
            # who's your daddy?!
            tbl.database = self
        # make sure we have views objects
        if self.views is None:
            self.views = supermod.views.factory()
        assert(self.views.view is not None)
        for view in self.views.view:
            # who's your daddy?!
            view.database = self
        # make sure there is a name
        if self.name is None:
            self.name = 'database'

    @property
    def namespace(self):
        '''The namespace for this database.'''
        return self.name.lower()

    def nspaced(self, inp):
        '''Prepend the namespace to given name.'''
        return '%s::%s' % (self.namespace, inp)

    def meta_nspaced(self, inp):
        '''Prepend the meta namespace to given name.'''
        return '%s::meta::%s' % (self.namespace, inp)
        
        
        
supermod.database.subclass = databaseSub
# end class databaseSub


# ----------------------------------------------------------------------------
# ------------------[              Methods             ]----------------------
# ----------------------------------------------------------------------------

def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass

# ----------------------------------------------------------------------------

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
            sys.stdout,
            0,
            name_=rootTag,
            namespacedef_='xmlns:dbsm="http://pile-contributors.github.io/database/PileSchema.xsd"',
            pretty_print=True)
    return rootObj

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

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
            sys.stdout,
            0,
            name_=rootTag,
            namespacedef_='xmlns:dbsm="http://pile-contributors.github.io/database/PileSchema.xsd"')
    return rootObj

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

# ----------------------------------------------------------------------------

def usage():
    print(USAGE_TEXT)
    sys.exit(1)

# ----------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

# ----------------------------------------------------------------------------
