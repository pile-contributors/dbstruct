#!/usr/bin/env python
'''
Script implementing all top level commands for dbschema pile.

Basic usage:

.. code-block:: none

    pileschema.py command

The module is designed to be used mainly from command line. It has three
main parts:
- the driver classes used to process an xml file;
- intermediate level methods (validate(), validate_string());
- utility methods for dealing with user input (arguments) and output (logging).

All driver classes derive from `Driver` class. SqlDriver creates a sql
schema and QtDriver creates C++ source files. `process_with_driver()`
is used to iterate the content of the .xml file and send the parts to
the driver that has been choosen.
'''

import argparse
from collections import OrderedDict
import datetime
import logging
from lxml import etree
import os
import platform

# file generated from PileSchema.xsd
import pile_schema_sclass as pile_schema_api

# The logger used to communicate to outside world (see setup_logging() )
LOGGER = None

# The file holding schema for input xml file
SCHEMA_FILE = None
DEFAULT_SCHEMA_FILE = './PileSchema.xsd'

# The author of the file (written in cpp files header, for example).
AUTHOR = None

# ----------------------------------------------------------------------------
# ------------------[          Driver  Classes         ]----------------------
# ----------------------------------------------------------------------------

class Driver(object):
    '''
    Base class for drivers used to process data in an xml file.

    Processing an xml file usually involves parsing an .xml file using
    a driver given to process_with_driver(). This is the base class for that
    driver that defines the methods used by process_with_driver() while
    iterating the content of the file.

    The class also hosts utility methods of use to all drivers derived
    from this class.
    '''
    def __init__(self):
        self.views = {}
        self.tables = {}
        super(Driver, self).__init__()

    def database_start(self, name, node):
        '''Starting to process database `name`'''
        pass

    def database_end(self, name, node):
        '''Done processing database `name`'''
        pass

    def table_start(self, name, node):
        '''Starting to process table `name`'''
        pass

    def table_end(self, name, node):
        '''Done processing table `name`'''
        pass

    def column(self, name, label, datatype, nulls, node, dtnode):
        '''Processing a column'''
        pass

    def view_start(self, name, node):
        '''Starting to process view `name`'''
        pass

    def view_end(self, name, node):
        '''Done processing view `name`'''
        pass

    def view_subset(self, node, subset):
        '''Process a subset in a view'''
        pass

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

class SqlDriver(Driver):
    '''
    Default implementation for generating Sql statements.

    The statements are accumulated in sql_string; the user may use this
    variable to retrieve the output after processing a file.
    '''
    def __init__(self):
        # this is where we accumulate the content of the file
        self.sql_string = ''
        # base class constructor
        super(SqlDriver, self).__init__()

    def database_start(self, name, node):
        '''Starting to process database `name`'''
        if name is None:
            name = '(not labeled)'
        self.append_file_guard()
        self.sql_string += '-- Database schema for: ' + name + '\n'
        self.append_line_marks()

    def database_end(self, name, node):
        '''Done processing database `name`'''
        self.append_file_guard()

    def table_start(self, name, node):
        '''Starting to process table `name`'''
        self.sql_string += 'CREATE TABLE IF NOT EXISTS `' + name + '` (\n'

    def table_end(self, name, node):
        '''Done processing table `name`'''
        # if a primary key was defined then add it to the statement
        try:
            pkey = node.primaryKey.key.column[0]
            self.sql_string += '  PRIMARY KEY (`' + pkey.name + '`),\n'
        except AttributeError:
            pass
        # add collected foreign keys
        for fkey in node.foreign_columns:
            self.append_foreign_key(fkey)
        # that should do it
        self.end_sql_statement()

    def column(self, name, node):
        '''Processing a column'''
        # skip virtual columns
        if node.virtual:
            return

        # first comes the name
        self.sql_string += '  `' + name + '` '
        # then the datatype and its size
        self.sql_string += node.sqltype
        if node.length:
            self.sql_string += '(' + node.length + ') '
        else:
            self.sql_string += ' '
        # any defaults
        defval = node.default
        if defval is not None:
            self.sql_string += 'DEFAULT ' + str(defval) + ' '
        # null constraint
        if not node.allowNulls:
            self.sql_string += 'NOT NULL '
        # auto-incrementing for identity column
        if node.identity:
            self.sql_string += 'AUTO_INCREMENT '
        # strip trailing whitespace
        if self.sql_string[-1] == ' ':
            self.sql_string = self.sql_string[:-1]
        # and that's it folks
        self.sql_string += ',\n'

    def view_start(self, name, node):
        '''Starting to process view `name`'''
        self.sql_string += 'CREATE VIEW IF NOT EXISTS `' + name + '` AS\n'

    def view_end(self, name, node):
        '''Done processing view `name`'''
        self.sql_string += ';\n'

    def view_subset(self, node, subset):
        '''Process a subset in a view'''
        if subset.in_ is None:
            # only a primary table
            self.sql_string += '  SELECT * FROM ' + subset.name1 + \
                ' WHERE ' + \
                subset.col1 + subset.constraint + subset.value + '\n'
        else:
            # a primary and a secondary
            self.sql_string += '  SELECT * FROM ' + subset.name1 + \
                ' WHERE ' + \
                subset.col1 + ' IN (\n' + \
                '    SELECT ' + subset.incol + ' FROM ' + subset.in_ + \
                ' WHERE ' + \
                subset.where + subset.constraint + subset.value + ')\n'

    def end_sql_statement(self):
        '''Terminate an sql statement'''

        # get rid of last comma
        if (self.sql_string[-2] == ',') and (self.sql_string[-1] == '\n'):
            self.sql_string = self.sql_string[:-2] + '\n'

        self.sql_string += ');\n'

    def append_comment_line(self, comment):
        '''Adds the text after comment marker'''
        self.sql_string += '-- ' + comment + '\n'

    def append_comment(self, comment):
        '''Splits the text in lines and adds comment marker.'''
        for cm_line in comment.split('\n'):
            self.sql_string += '-- ' + cm_line + '\n'

    def append_line_marks(self):
        '''Adds the text after comment marker'''
        self.sql_string += '-- ' + 77 * '-' + '\n'

    def append_file_guard(self):
        '''Adds comments useful at beginning and/or end of file'''
        self.append_line_marks()
        self.sql_string += '-- ' + \
            'This file was generated by pileschema.py; ' +\
            'please dont\'t edit it manually.\n'
        self.append_line_marks()

    def append_foreign_key(self, fdata):
        '''Adds the ForeignKey to the file content'''
        self.sql_string += \
            '  FOREIGN KEY(' + \
            fdata.name + \
            ') REFERENCES ' + \
            fdata.foreignTable + \
            '(' + fdata.foreignColumn + '),\n'


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


# The base class for Meta Tables
META_TABLE_BASE = 'DbTable'
# The base class for Tables
RECORD_BASE = 'DbRecord'
# include files for Meta Table file
META_TABLE_BASE_FILE = '#include <dbstruct/dbtable.h>'
# convert a QVariant to actual data inside a table
FROM_VARIANT = {
    'QString': 'toString ())',
    'bool': 'toBool ())',
    'long': 'toLongLong (&b_one)); b_ret = b_ret & b_one',
    'char': 'toInt (&b_one)); b_ret = b_ret & b_one',
    'short': 'toInt (&b_one)); b_ret = b_ret & b_one',
    'int': 'toInt (&b_one)); b_ret = b_ret & b_one',
    'double': 'toDouble (&b_one)); b_ret = b_ret & b_one',
    'float': 'toDouble (&b_one)); b_ret = b_ret & b_one',
    'QDateTime': 'toDateTime ())',
    'QDate': 'toDate ())',
    'QTime': 'toTime ())',
    'QByteArray': 'toByteArray ())',
    'void *': 'value<void *>())'
}


class QtDriver(Driver):
    '''
    Default implementation for generating Qt5 based C++ source files.
    '''
    def __init__(self, out_dir, template_dir,
                 namespace='', export_macro='',
                 import_header='',
                 base_class=META_TABLE_BASE):
        # save arguments
        self.out_dir = out_dir
        self.template_dir = template_dir
        self.namespace = namespace
        self.export_macro = export_macro
        self.import_header = import_header
        self.base_class = base_class
        # will be collected in later stages
        self.db_name = None
        self.db_node = None
        # the dict holds data to be replaced in template files
        self.data = {}
        # content of template files indexed by file name
        self.templates = {}
        # base class constructor
        super(QtDriver, self).__init__()

    def database_start(self, name, node):
        '''Starting to process database `name`'''
        now = datetime.datetime.now()

        self.db_name = name
        self.db_node = node
        self.set_data_mix('Database', name)
        self.set_data_mix('Namespace', self.namespace)
        self.set_data_mix('BaseClass', self.base_class)
        self.set_data_mix('MetaClassInclude', META_TABLE_BASE_FILE)
        self.set_data_mix('RecordBaseClass', RECORD_BASE)
        self.set_data('EXPORT', self.export_macro)
        if self.import_header is not None and len(self.import_header) > 0:
            self.set_data('IMPORTH', '#include <%s>' % self.import_header)
        else:
            self.set_data('IMPORTH', '')
        self.set_data('Year', str(now.year))
        self.set_data('Month', now.strftime("%B"))
        self.set_data('Author', AUTHOR)
        #for k in self.data:
        #    print k, self.data[k]

    def database_end(self, name, node):
        '''Done processing database `name`'''
        self.set_data_mix('BaseClass', 'DbStructMeta')
        self.collect_db_ids_(node)
        self.collect_db_headers_(node)
        self.collect_db_ctors_(node)
        self.collect_db_new_ctors_(node)
        self.collect_db_namecase_(node)
        self.collect_db_name2id_(node)
        
        dbn = self.data['database']
        self.from_tpl(dbn, '.h', 'database.h.template')
        self.from_tpl(dbn, '.cc', 'database.cc.template')
        self.from_tpl('all-meta-tables.h', '', 'all-meta-tables.h.template')
        self.from_tpl('all-tables.h', '', 'all-tables.h.template')

    def table_start(self, name, node):
        '''Starting to process table `name`'''
        self.set_data_mix('Table', name)

    def table_end(self, name, node):
        '''Done processing table `name`'''
        name = name.lower()
        self.set_data('TableDataMembers', self.table_data_members_(node))
        self.set_data('COLUMN_COUNT', len(node.columns.column))
        self.set_data('PIPE_COLUMNS', self.pipe_columns_(node))
        self.set_data('CASE_COLUMNS', self.case_column_(node, get_name=True))
        self.set_data('CASE_LABELS', self.case_column_(node, get_name=False))
        self.set_data('MODEL_LABELS', self.header_data_(node))
        self.set_data('BIND_COLUMNS', self.bind_columns_(node, only_one=False))
        self.set_data('BIND_ONE_COLUMN', self.bind_columns_(node, only_one=True))
        self.set_data('RETREIVE_COLUMNS', self.retrieve_columns_(node, False))
        self.set_data('RECORD_COLUMNS', self.retrieve_columns_(node, True))
        self.set_data('ID_COLUMN', node.colid)
        if node.id_column and node.id_column.inttype:
            self.set_data('GET_ID_RESULT', node.colid)
            self.set_data('SET_ID_RESULT', '%s = value' % node.id_column.name)
        else:
            self.set_data('GET_ID_RESULT', 'COLID_INVALID')
            self.set_data('SET_ID_RESULT', '// id unavailable in this model')
        self.set_data('COMMA_COLUMNS', node.columns.comma_columns(
            with_id=True, only_real=True, exclude_fk=False,
            padding=' ' * 12, lines=True, prefix=''))
        self.set_data('COMMA_COLUMNS_NO_ID', node.columns.comma_columns(
            with_id=False, only_real=True, exclude_fk=False,
            padding=' ' * 12, lines=True, prefix=''))
        self.set_data('COLUMN_COLUMNS', node.columns.comma_columns(
            with_id=True, only_real=True, exclude_fk=False,
            padding=' ' * 12, lines=True, prefix=''))
        self.set_data('ASSIGN_COLUMNS', node.columns.assign_columns(
            with_id=False, only_real=True, exclude_fk=True,
            padding=' ' * 12, lines=True))
        self.set_data('COLUMN_IDS', node.columns.column_ids(
            with_id=True, only_real=True, exclude_fk=True,
            padding=' ' * 8, lines=True))
        self.set_data('TableColumnConstr', self.column_getters_(node))
        self.set_data('TableColumnsIndexCtor', self.column_idx_getters_(node))
        self.set_data('TableDataMembers', self.table_data_members_(node))
        self.set_data('CopyConstructor', self.copy_constr_(node, False))
        self.set_data('AssignConstructor', self.copy_constr_(node, True))
        self.set_data('DefaultConstructor', self.default_constr_(node))
        self.set_data('RecToMap', self.rec_to_map_(node))
        self.set_data('RecFromMap', self.rec_from_map_(node))
        self.set_data('SetTableDefaults', self.set_table_defaults_(node))
        self.set_data('SetTableOverrides', '    Q_UNUSED(result);')
        self.set_data('RealColumnMapping', self.real_column_mapping_(node))
        self.set_data('VirtualColumnMapping', self.virtual_column_mapping_(node))

        self.from_tpl(name, '.h', 'table.h.template')
        self.from_tpl(name, '-meta.h', 'table-meta.h.template')
        self.from_tpl(name, '.cc', 'table.cc.template')
        self.from_tpl(name, '-meta.cc', 'table-meta.cc.template')


    def column(self, name, node):
        '''Processing a column'''
        pass

    def view_start(self, name, node):
        '''Starting to process view `name`'''
        self.set_data_mix('Table', name)

    def view_end(self, name, node):
        '''Done processing view `name`'''
        name = name.lower()
        self.from_tpl(name, '.h', 'view.h.template')
        self.from_tpl(name, '-meta.h', 'view-meta.h.template')
        self.from_tpl(name, '.cc', 'view.cc.template')
        self.from_tpl(name, '-meta.cc', 'view-meta.cc.template')

    def view_subset(self, node, subset):
        '''Process a subset in a view'''
        pass

    # ------------------------------------

    def table_data_members_(self, node):
        '''
        Data members inside table classes to hold actual data.
        '''
        result = ''
        for col in node.columns.column:
            result += table_data_members_templ % (col.qtype, col.var_name)
        return result[:-1] if len(result) > 0 else ''

    def pipe_columns_(self, node):
        '''
        Add each column name to a string list.
        '''
        result = ''
        for col in node.columns.column:
            result += pipe_columns_templ % col.name
        return result[:-1] if len(result) > 0 else ''

    def case_column_(self, node, get_name=True):
        '''
        Get the name or label of a column based on its index.

        The frunction must declare `result` as a QString and the text
        must be inside a select statement.
        '''
        result = ''

        for col in node.columns.column:
            result += case_column_templ % (
                col.colid, col.name if get_name else col.title)
        return result[:-1] if len(result) > 0 else ''

    def bind_columns_(self, node, only_one=False):
        '''
        Binds the value for a column with the name in a QSqlQuery.

        To be used inside a table class when values in a record are about to
        be set.
        '''
        result = ''
        for col in node.columns.non_virtuals():
            if only_one:
                result += bind_column_templ % (
                    col.colid, col.name, col.var_name)
            else:
                result += bind_columns_templ % (col.name, col.var_name)
        return result[:-1] if len(result) > 0 else ''

    def header_data_(self, node):
        '''
        Sets the horizontal headers of a Qt model to labels from columns.
        '''
        result = ''
        for col in node.columns.column:
            result += header_data_templ % (col.colid, col.qt_title)
        return result[:-1] if len(result) > 0 else ''

    def retrieve_columns_(self, node, record=False):
        '''
        Binds the value for a column with the name in a QSqlQuery.

        To be used inside a table class when values in a record are about to
        be set.
        '''
        result = ''
        for col in node.columns.non_virtuals():
            if record:
                result += record_columns_templ % (
                    col.var_name, col.qtype, 'QLatin1String("%s")' % col.name,
                    FROM_VARIANT[col.qtype])
            else:
                result += retrieve_columns_templ % (
                    col.var_name, col.qtype, col.colid, col.my_real,
                    FROM_VARIANT[col.qtype])
        return result[:-1] if len(result) > 0 else ''

    def column_getters_(self, node):
        '''
        Constructors for each column in the table.
        '''
        result = ''
        for col in node.columns.column:
            result += column_getters_templ % (col.name, col.qtconstructor)
        return result[:-1] if len(result) > 0 else ''

    def column_idx_getters_(self, node):
        '''
        Constructors for each column in the table based on the index.
        '''
        result = ''
        for col in node.columns.column:
            result += column_idx_getters_templ % (col.colid, col.qtconstructor)
        return result[:-1] if len(result) > 0 else ''

    def copy_constr_(self, node, assign=False):
        '''
        Copy each data item to its counterpart.
        '''
        result = ''
        if assign:
            templ = asgn_constr_templ
            cut_back = 1
        else:
            templ = copy_constr_templ
            cut_back = 1
        for col in node.columns.column:
            result += templ % (col.var_name, col.var_name)
        return result[:-cut_back] if len(result) > 0 else ''

    def default_constr_(self, node):
        '''
        Default values for data in tables.
        '''
        result = ''
        for col in node.columns.column:
            if col.identity is None:
                if col.inttype:
                    valx = 'COLID_INVALID'
                elif col.qtype is 'QString':
                    valx = 'QLatin1String("-1")'
                else:
                    valx = ''
            else:
                valx = ''
            result += default_constr_templ % (col.var_name, valx)
        return result[:-1] if len(result) > 0 else ''

    def rec_to_map_(self, node):
        '''
        Insert the value.
        '''
        result = ''
        for col in node.columns.column:
            result += rec_to_map_templ % (
                    'QLatin1String ("%s")' % col.name,
                    ('qVariantFromValue (%s)' % col.var_name)
                        if col.dynamic else 'QVariant (%s)' % col.var_name)
        return result[:-1] if len(result) > 0 else ''

    def rec_from_map_(self, node):
        '''
        Get the value.
        '''
        result = ''
        for col in node.columns.column:
            result += rec_from_map_templ % (
                'QLatin1String ("%s")' % col.name,
                col.var_name, col.qtype, FROM_VARIANT[col.qtype])
        return result[:-1] if len(result) > 0 else ''

    def set_table_defaults_(self, node):
        '''.'''
        result = ''
        for col in node.columns.column:
            val_def = col.default
            if val_def == 'NULL':
                val_def = None
            if val_def is None:
                if col.inttype:
                    val_def = '0'
                elif col.realtype:
                    val_def = '0.0'
                elif col.qtype == 'bool':
                    val_def = 'false'
                else:
                    val_def = '%s ()' % col.qtype
            # val_def is defined
            elif col.qtype == 'QString':
                val_def = 'QLatin1String ("%s");\n' % val_def
            elif col.inttype or col.realtype:
                pass
            elif col.qtype == 'bool':
                val_def = str(val_def).lower()
            else:
                val_def = '%s (%s)' % (col.qtype, val_def)
            result += '    result->%s = %s;\n' % (col.var_name, val_def)                
        return result[:-1] if len(result) > 0 else ''

    def real_column_mapping_(self, node):
        '''.'''
        result = ''
        for col in node.columns.column:
            col_mapping_nicety = '/* ' + col.colid + ' -> */ '
            col_mapping_nicety += ' ' * (64 - len(col_mapping_nicety))
            result += 4 * ' ' + col_mapping_nicety
            if not col.virtual:
                result += '%d,\n' % col.myid
            else:
                result += '-1,\n'
        return result[:-2] if len(result) > 0 else '-1'

    def virtual_column_mapping_(self, node):
        '''.'''
        result = ''
        for i, col in enumerate(node.columns.column):
            col_mapping_nicety = '/* ' + col.colid + ' -> */ '
            col_mapping_nicety += ' ' * (64 - len(col_mapping_nicety))
            if not col.virtual:
                result += 4*' ' + col_mapping_nicety + str(i) + ',\n'
        return result[:-2] if len(result) > 0 else '-1'
    
    # ------------------------------------

    def set_data_mix(self, label, value):
        '''
        Adds data to the self.data in mixed case, lower case and upper case.
        '''
        self.data[label] = value
        self.data[label.lower()] = value.lower()
        self.data[label.upper()] = value.upper()

    def set_data(self, label, value):
        '''
        Adds data to the self.data in the case that was provided.
        '''
        self.data[label] = value

    def from_tpl(self, file_name, suffix, template_name):
        '''
        Reads specified template, replaces variables and writes teh file.
        '''
        fname = os.path.join(self.out_dir, file_name + suffix)
        with open(fname, 'w') as foutp:
            file.write(
                foutp, self.get_template(template_name) % self.data)
        return fname

    def get_template(self, which):
        '''Read the content of a template file'''
        if not which in self.templates:
            with open(os.path.join(self.template_dir, which), 'r') as finp:
                self.templates[which] = finp.read()
        return self.templates[which]

    def collect_db_ids_(self, dbnode):
        '''Create unique IDs for components of the database'''
        db_comp_id = ''
        db_table_id = ''
        db_view_id = ''
        for tbl in dbnode.tables.table:
            db_comp_id += '        %s,\n' % tbl.dbcid
            db_table_id += '        %s,\n' % tbl.dbtid
        for view in dbnode.views.view:
            db_comp_id += '        %s,\n' % view.dbcid
            db_view_id += '        %s,\n' % view.dbvid

        self.set_data('DBC_IDS', db_comp_id)
        self.set_data('DB_TABLE_IDS', db_table_id)
        self.set_data('DB_VIEW_IDS', db_view_id)
        return db_comp_id, db_table_id, db_view_id

    def collect_db_headers_(self, dbnode):
        '''Create a #include list of all the headers for the database.'''
        all_hdr = ''
        all_meta_hdr = ''
        for tbl in dbnode.tables.table:
            all_hdr += '#include "%s"\n' % tbl.header
            all_meta_hdr += '#include "%s"\n' % tbl.metaheader
        for view in dbnode.views.view:
            all_hdr += '#include "%s"\n' % view.header
            all_meta_hdr += '#include "%s"\n' % view.metaheader

        self.set_data('INCLUDE_ALL_HEADERS', all_hdr)
        self.set_data('INCLUDE_ALL_META_HEADERS', all_meta_hdr)

    def collect_db_ctors_(self, dbnode):
        '''Constructors for tables and views as static methods.'''
        db_tables_constr = ''
        for tbl in dbnode.tables.table:
            nspace = tbl.meta_nspaced_class
            db_tables_constr += '    static %s %s () { return %s (); }\n' % (
                nspace, tbl.var_name, nspace)
        db_views_constr = ''
        for view in dbnode.views.view:
            nspace = view.meta_nspaced_class
            db_tables_constr += '    static %s %s () { return %s (); }\n' % (
                nspace, view.var_name, nspace)

        self.set_data('DB_TABLES_CONSTR', db_tables_constr)
        self.set_data('DB_VIEWS_CONSTR', db_views_constr)

    def collect_db_new_ctors_(self, dbnode):
        '''Constructors for tables and views as static methods.'''
        db_new_components = ''
        for tbl in dbnode.tables.table:
            db_new_components += collect_db_new_ctors_templ % (
                tbl.dbcid, tbl.meta_nspaced_class)
        for view in dbnode.views.view:
            db_new_components += collect_db_new_ctors_templ % (
                view.dbcid, view.meta_nspaced_class)
        self.set_data('DB_NEW_COMPONENTS', db_new_components)

    def collect_db_namecase_(self, dbnode):
        '''Get the name of a table or view based on their id.'''
        db_comp_name_case = ''
        db_table_name_case = ''
        for tbl in dbnode.tables.table:
            ncase = '        case %s: return QLatin1String("%s");\n' % (
                tbl.dbcid, tbl.name)
            db_comp_name_case += ncase
            db_table_name_case += ncase
        db_view_name_case = ''
        for view in dbnode.views.view:
            ncase = '        case %s: return QLatin1String("%s");\n' % (
                view.dbcid, view.name)
            db_comp_name_case += ncase
            db_table_name_case += ncase

        self.set_data('DB_TABLES_NAME_CASE', db_table_name_case)
        self.set_data('DB_VIEWS_NAME_CASE', db_view_name_case)
        self.set_data('DB_COMPONENTS_NAME_CASE', db_comp_name_case)

    def collect_db_name2id_(self, dbnode):
        '''Get the name of a table or view based on their id.'''
        db_name_to_id = ''
        for tbl in dbnode.tables.table:
            db_name_to_id += collect_db_name2id_templ % (
                tbl.name, tbl.dbcid)
        for view in dbnode.views.view:
            db_name_to_id += collect_db_name2id_templ % (
                view.name, view.dbcid)
        self.set_data('DB_COMPONENTS_NAME_TO_ID', db_name_to_id)

table_data_members_templ = '    %s %s;\n'
pipe_columns_templ = '        << QLatin1String("%s")\n'
case_column_templ = '    case %s: result = QLatin1String("%s"); break;\n'
bind_columns_templ = '    query.bindValue (QLatin1String (":%s"), %s);\n'
bind_column_templ = '    case %s: query.bindValue (QLatin1String (":%s"), %s); break;\n'
header_data_templ = '    model->setHeaderData (%s, Qt::Horizontal, %s);\n'
retrieve_columns_templ = '    %-26s = static_cast<%10s>(query.value (' \
                         '/* %33s */ %4d).%s;\n'
record_columns_templ = '    %-26s = static_cast<%10s>(rec.value (' \
                       '%40s).%s;\n'
column_getters_templ = '    static DbColumn %30sColCtor () { return %s; }\n'
column_idx_getters_templ = '    case %20s: return %s;\n'
copy_constr_templ = '        , %s (other.%s)\n'
asgn_constr_templ = '        %s = other.%s;\n'
default_constr_templ = '        , %s (%s)\n'
rec_from_map_templ = '        if (!i.key ().compare (%40s)) { ' \
                     '%-20s = static_cast<%10s> (i.value ().%s; }\n'
rec_to_map_templ = '    result.insert(%-40s, %-30s);\n'
collect_db_name2id_templ = '        if (!value.compare(' \
    'QLatin1String("%s"), Qt::CaseInsensitive)) return %s;\n'
collect_db_new_ctors_templ = '        case %s: return new %s ();\n'

# ----------------------------------------------------------------------------
# ------------------[   Intermediate level Functions   ]----------------------
# ----------------------------------------------------------------------------

def validate(xmlfilename):
    '''
    Validates a file and returns the xml tree.
    '''
    with open(xmlfilename, 'r') as finp:
        return validate_string(finp.read())

# ----------------------------------------------------------------------------

def validate_string(xmlstring):
    '''
    Validates a string and returns the xml tree.
    '''
    try:
        xml_root = pile_schema_api.parseString(xmlstring, silence=True)

        return xml_root
    except (etree.XMLSchemaError, etree.XMLSyntaxError) as exc:
        LOGGER.error('Schema validation failed: ' + str(exc))
        return None

# ----------------------------------------------------------------------------

def process_with_driver(driver, database):
    '''
    Use a driver to process the database.
    '''
    driver.database_start(database.name, database)

    tables = database.tables
    views = database.views

    for table in tables.table:
        driver.table_start(table.name, table)
        columns = table.columns
        for column in columns.column:
            driver.column(column.name, column)
        driver.table_end(table.name, table)

    for view in views.view:
        driver.view_start(view.name, view)
        subset = view.subset
        if subset is not None:
            driver.view_subset(view, subset)
        else:
            LOGGER.error('Unknown view type')
            return -1
        driver.view_end(view.name, view)

    driver.database_end(database.name, database)

# ----------------------------------------------------------------------------

def str2bool(value):
    '''Get a proper boolean value based on a string value.'''
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return value.lower() in ("yes", "true", "t", "1")

# ----------------------------------------------------------------------------

def string_choice(str1, str2, choice):
    '''Returns either first or second string based on choice.'''
    return str(str1) if choice else str(str2)

# ----------------------------------------------------------------------------
# ----------------------[         User  input         ]-----------------------
# ----------------------------------------------------------------------------

def extract_common(args):
    '''
    Extract common information from arguments and save it at module level.
    '''
    global AUTHOR, SCHEMA_FILE

    if hasattr(args, 'author') and args.author is not None:
        AUTHOR = args.author

    if not hasattr(args, 'schema') or args.schema == None:
        args.schema = DEFAULT_SCHEMA_FILE

    if SCHEMA_FILE != args.schema:
        SCHEMA_FILE = args.schema
        with open(args.schema, 'r') as finp:
            schema_root = etree.XML(finp.read())
        schema = etree.XMLSchema(schema_root)
        etree.XMLParser(schema=schema, attribute_defaults=True)

# ----------------------------------------------------------------------------

def cmd_validate(args):
    '''The input xml file is read and checked against the schema.'''
    extract_common(args)
    if validate(args.xml):
        LOGGER.info("%s validates", args.xml)
        return 1
    else:
        LOGGER.warning("%s doesn't validate", args.xml)
        return 0

# ----------------------------------------------------------------------------

def cmd_sql(args):
    '''Creates an sql file from input xml file.'''

    extract_common(args)

    if (args.driver == 'none') or (args.driver == ''):
        driver = SqlDriver()
    else:
        LOGGER.error('Unknown driver: ' + args.driver)
        return -1

    database = validate(args.xml)
    if database is None:
        return -1

    process_with_driver(driver, database)

    out_file = args.output
    if out_file is None:
        out_file = os.path.splitext(args.xml)[0] + '.sql'
    with open(out_file, 'w') as foutp:
        foutp.write(driver.sql_string)
    return 0

# ----------------------------------------------------------------------------

def cmd_qt(args):
    '''Generate C++ source files from input .xml file.'''

    extract_common(args)

    if args.driver == 'qt':
        driver = QtDriver(
            out_dir=args.output,
            template_dir=args.templates,
            namespace=args.namespace,
            export_macro=args.exportm,
            import_header=args.importh)
    else:
        LOGGER.error('Unknown driver: ' + args.driver)
        return -1

    database = validate(args.xml)
    if database is None:
        return -1

    process_with_driver(driver, database)

    return 0

# ----------------------------------------------------------------------------

def make_argument_parser():
    '''
    Creates an ArgumentParser to read the options for this script from
    sys.argv
    '''
    parser = argparse.ArgumentParser(
        description="Main entry point for pileschema module.",
        epilog='\n'.join(__doc__.strip().split('\n')[1:]).strip(),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--logfile',
                        action='store',
                        help='Save the output to file.')
    parser.add_argument('--debug', '-D',
                        action='store_true',
                        help='Display any DEBUG-level log messages, '
                             'suppressed by default.')

    subparsers = parser.add_subparsers(help='Available sub-commands')

    parser_a = subparsers.add_parser(
        'validate',
        help='Validate an xml against PileSchema.xsd')
    parser_a.add_argument(
        'xml', metavar="XML", type=str,
        help='input .xml file')
    parser_a.add_argument(
        '--schema', type=str,
        help='schema used for validation',
        default=DEFAULT_SCHEMA_FILE)
    parser_a.set_defaults(func=cmd_validate)

    parser_a = subparsers.add_parser(
        'sql',
        help='Generate an .sql file from input .xml')
    parser_a.add_argument(
        'xml', metavar="XML", type=str,
        help='input .xml file')
    parser_a.add_argument(
        'output', metavar="OUT", type=str, nargs='?',
        help='output .sql file')
    parser_a.add_argument(
        '--schema', type=str,
        help='schema used for validation',
        default=DEFAULT_SCHEMA_FILE)
    parser_a.add_argument(
        '--driver', type=str,
        help='driver used for output',
        choices=['none', 'sqlite'], default='none')
    parser_a.add_argument(
        '--author', type=str,
        help='The author of the files',
        default=username())
    parser_a.set_defaults(func=cmd_sql)

    parser_a = subparsers.add_parser(
        'cpp',
        help='Generate C++ sources from input .xml')
    parser_a.add_argument(
        'xml', metavar="XML", type=str,
        help='input .xml file')
    parser_a.add_argument(
        'output', metavar="OUT", type=str, nargs='?',
        help='output directory',
        default='.')
    parser_a.add_argument(
        '--driver', type=str,
        help='driver used for output',
        choices=['qt'], default='qt')
    parser_a.add_argument(
        '--namespace', type=str,
        help='top level namespace for generated output',
        default='')
    parser_a.add_argument(
        '--templates', type=str,
        help='directory containing file templates',
        default='qt-templates')
    parser_a.add_argument(
        '--schema', type=str,
        help='schema used for validation',
        default=DEFAULT_SCHEMA_FILE)
    parser_a.add_argument(
        '--author', type=str,
        help='The author of the files',
        default=username())
    parser_a.add_argument(
        '--exportm', type=str,
        help='The macro used to export functions and classes',
        default='')
    parser_a.add_argument(
        '--importh', type=str,
        help='Header file to be imported in every generated header',
        default='')
    parser_a.set_defaults(func=cmd_qt)

    return parser

# ----------------------------------------------------------------------------

def username():
    '''The name of the user for running machine.'''
    if platform.system() == 'Windows':
        import win32api
        return win32api.GetUserNameEx(3)
    else:
        import pwd
        return pwd.getpwuid(os.getuid())[0]

# ----------------------------------------------------------------------------

def setup_logging(args):
    '''
    Prepare module logger based on user options.
    '''
    global LOGGER

    # Set the root logger level.
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    if args.logfile and len(args.logfile) > 0:
        logfile = args.logfile
    else:
        logfile = None

    LOGGER = logging.getLogger('PilesSchema')


    if logfile:
        log_formatter = logging.Formatter('%(asctime)s ' \
                                         '[%(threadName)-12.12s] ' \
                                         '[%(levelname)-5.5s]  ' \
                                         '%(message)s')

        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)
        LOGGER.addHandler(file_handler)

    log_formatter = logging.Formatter('[%(levelname)-5.5s]  ' \
                                     '%(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    LOGGER.addHandler(console_handler)
    console_handler.setLevel(loglevel)

    LOGGER.setLevel(logging.DEBUG)

# ----------------------------------------------------------------------------

def main():
    '''Main function for the module.'''
    parser = make_argument_parser()
    args = parser.parse_args()
    setup_logging(args)
    args.func(args)

if __name__ == "__main__":
    main()
