#!/usr/bin/env python
'''
Script implementing all top level commands.

Basic usage:

.. code-block:: none

    pileschema.py command

'''

import argparse
from collections import OrderedDict
import datetime
import logging
from lxml import etree
import os
import platform
import sys

import pile_schema_api

if platform.system() == 'Windows':
    import win32api
    def username ():
        return win32api.GetUserNameEx(3)
else:
    import pwd
    def username():
        return pwd.getpwuid(os.getuid())[0]

PARSER = None
SCHEMA_FILE = None
AUTHOR = None
META_TABLE_BASE = 'DbTable' # The base class for Meta Tables
RECORD_BASE = 'DbRecord' # The base class for Tables
META_TABLE_BASE_FILE = '#include <dbstruct/dbtable.h>' # include files for Meta Table file
DEFAULT_SCHEMA_FILE = './PileSchema.xsd'
NSPACESTR = None
logger = logging.getLogger('PileSchema')
FROM_VARIANT = {
    'QString': 'toString ()',
    'bool': 'toBool ()',
    'long': 'toLongLong (&b_one); b_ret = b_ret & b_one',
    'char': 'toInt (&b_one); b_ret = b_ret & b_one',
    'short': 'toInt (&b_one); b_ret = b_ret & b_one',
    'int': 'toInt (&b_one); b_ret = b_ret & b_one',
    'double': 'toDouble (&b_one); b_ret = b_ret & b_one',
    'float': 'toDouble (&b_one); b_ret = b_ret & b_one',
    'QDateTime': 'toDateTime ()',
    'QDate': 'toDate ()',
    'QTime': 'toTime ()'
}

TO_CAST = {
    'QString': '',
    'bool': '(bool)',
    'long': '(long)',
    'char': '(char)',
    'short': '(short)',
    'int': '(int)',
    'double': '(double)',
    'float': '(float)',
    'QDateTime': '',
    'QDate': '',
    'QTime': ''
}



# ----------------------------------------------------------------------------


class Driver(object):
    '''
    Default implementation with regard to the underlying
    Sql variant.
    '''
    def __init__(self):
        super(Driver, self).__init__()

    def databaseStart(self, name, node):
        '''Starting to process database `name`'''
        pass

    def databaseEnd(self, name, node):
        '''Done processing database `name`'''
        pass

    def tableStart(self, name, node):
        '''Starting to process table `name`'''
        pass

    def tableEnd(self, name, node):
        '''Done processing table `name`'''
        pass

    def column(self, name, label, datatype, nulls, node, dtnode):
        '''Processing a column'''
        pass

    def viewStart(self, name, node):
        '''Starting to process view `name`'''
        pass

    def viewEnd(self, name, node):
        '''Done processing view `name`'''
        pass

    def viewSubset(self, node, subset):
        '''Process a subset in a view'''
        pass

    def getForeignKey(self, node):
        '''
        Extracts foreign key data from an xml node

        The result is None if no foreign key exists of a list of three elements:
        the table, the key column and the columns that should replace
        original key in a presentation to the user.
        '''

        # Is this column a foreign key into another table?
        ftable = node.foreignTable
        fcolumn = node.foreignColumn
        finsert = node.foreignInsert
        fbehaviour = node.foreignBehaviour
        if ftable is not None:
            return [ftable, fcolumn, finsert, fbehaviour]
        else:
            return None

    def checkForeignKeys(self):
        '''Make sure that all columns referenced in foreign keys actually exist.'''
        for tbl in self.tables:
            tbldata = self.tables[tbl]
            for col in tbldata['columns']:
                coldata = tbldata['columns'][col]['fkey']
                if coldata:
                    # the column is a foreign key
                    ftable, fcolumn, finsert, fbehaviour = coldata
                    try:
                        f_actual = self.tables[ftable]
                    except KeyError:
                        try:
                            f_actual = self.views[ftable]
                        except KeyError:
                            logger.warning(
                                'Column %s of table %s references table '
                                '%s that does not exist' % (col, tbl, ftable))
                            raise
                    try:
                        f_actual['columns'][fcolumn]
                    except KeyError:
                        logger.warning(
                            'Column %s of table %s references column '
                            '%s in table %s that does not exist' % (
                            col, tbl, fcolumn, ftable))
                        raise
                    if finsert:
                        try:
                            f_actual['columns'][finsert]
                        except KeyError:
                            logger.warning(
                                'Column %s of table %s uses column '
                                '%s in table %s that does not exist' % (
                                col, tbl, finsert, ftable))
                            raise

# ----------------------------------------------------------------------------

class SqlDriver(Driver):
    '''
    Default implementation with regard to the underlying
    Sql variant.
    '''
    def __init__(self):
        self.sql_string = ''
        self.foreignKeys = {}
        super(SqlDriver, self).__init__()

    def tableStart(self, name, node):
        '''Starting to process table `name`'''
        self.sql_string += 'CREATE TABLE IF NOT EXISTS `' + name + '` (\n'
        self.foreignKeys = {}

    def tableEnd(self, name, node):
        '''Done processing table `name`'''
        try:
            pkey = node.primaryKey.key.column[0]
        except AttributeError:
            pkey = None

        if pkey is not None:
            self.sql_string += '  PRIMARY KEY (`' + pkey.name + '`),\n'
        for fkey in self.foreignKeys:
            fdata = self.foreignKeys[fkey]
            self.sql_string += '  FOREIGN KEY(' + fkey + ') REFERENCES ' + \
                fdata[0] + '(' + fdata[1] + '),\n'

        if (self.sql_string[-2] == ',') and (self.sql_string[-1] == '\n'):
            # get rid of last comma
            self.sql_string = self.sql_string[:-2] + '\n'

        self.sql_string += ');\n'

    def column(self, name, label, datatype, nulls, node, dtnode):
        '''Processing a column'''
        # first comes the name
        self.sql_string += '  `' + name + '` '
        # then the datatype
        try:
            length = dtnode.length
        except AttributeError:
            length = None
        if length:
            self.sql_string += datatype + '(' + length + ') '
        else:
            self.sql_string += datatype + ' '
        # any defaults
        try:
            defval = dtnode.default
        except AttributeError:
            defval = None
        try:
            defexpr = dtnode.defaultExpression
        except AttributeError:
            defexpr = defval
        if defval:
            self.sql_string += 'DEFAULT ' + str(defval) + ' '
        elif defexpr:
            self.sql_string += 'DEFAULT ' + defexpr + ' '
        # null constraint
        if (not nulls):
            self.sql_string += 'NOT NULL '
        # auto-incrementing
        try:
            identity = dtnode.identity
        except AttributeError:
            identity = None
        if not identity is None:
            self.sql_string += 'AUTO_INCREMENT '
        if self.sql_string[-1] == ' ':
            self.sql_string = self.sql_string[:-1]
        # and that's it folks
        self.sql_string += ',\n'

        # Is this column a foreign key into another table?
        ftable = self.getForeignKey(node)
        if ftable is not None:
            self.foreignKeys[name] = ftable


    def viewStart(self, name, node):
        '''Starting to process view `name`'''
        self.sql_string += 'CREATE VIEW IF NOT EXISTS `' + name + '` AS\n'

    def viewEnd(self, name, node):
        '''Done processing view `name`'''
        self.sql_string += ';\n'

    def viewSubset(self, node, subset):
        '''Process a subset in a view'''
        name1 = subset.name1
        col1 = subset.col1
        name_in = subset.in_
        incol = subset.incol
        where = subset.where
        constraint = subset.constraint
        value = subset.value

        if name_in is None:
            # only a primary table
            self.sql_string += '  SELECT * FROM ' + name1 + ' WHERE ' + \
                col1 + constraint + value + '\n'
        else:
            # a primary and a secondary
            self.sql_string += '  SELECT * FROM ' + name1 + ' WHERE ' + \
                col1 + ' IN (\n' + \
                '    SELECT ' + incol + ' FROM ' + name_in + ' WHERE ' + \
                where + constraint + value + ')\n'


# ----------------------------------------------------------------------------

class QtDriver(Driver):
    '''
    Build C++ classes with Qt support.
    '''
    def __init__(self, out_dir, template_dir,
                 namespace='', export_macro='',
                 import_header='',
                 base_class=META_TABLE_BASE):

        self.out_dir = out_dir
        self.template_dir = template_dir
        self.data = {}
        self.templates = {}
        self.db_name = ''
        self.import_header = import_header
        self.namespace = namespace
        self.export_macro = export_macro
        self.base_class = base_class
        self.tables = OrderedDict()
        self.views = OrderedDict()
        self.columns = OrderedDict()
        self.vrtcols = [] # the names of the columns that are virtual
        super(QtDriver, self).__init__()

    def databaseStart(self, name, node):
        '''Starting to process database `name`'''
        self.db_name = name

    def databaseEnd(self, name, node):
        '''Done processing database `name.`'''

        self.checkForeignKeys()

        all_hdr = ''
        all_meta_hdr = ''
        db_comp_id = ''
        db_table_id = ''
        db_tables_constr = ''
        db_comp_name_case = ''
        db_table_name_case = ''
        db_name_to_id = ''
        db_new_components = ''
        nspace_prefix = self.db_name.lower() + '::meta::'
        for tbl in self.tables:
            with_nspace = nspace_prefix + tbl
            dbc_name = 'DBC_' + tbl.upper()
            dbt_name = 'DBT_' + tbl.upper()
            all_hdr += '#include "' + tbl.lower() + '.h"\n'
            all_meta_hdr += '#include "' + tbl.lower() + '-meta.h"\n'
            db_comp_id += ' ' * 8 + dbc_name + ',\n'
            db_table_id += ' ' * 8 + dbt_name + ',\n'
            db_tables_constr += '    static ' + with_nspace + ' ' + \
                tbl.lower() + ' () { return ' + with_nspace + '(); }\n'
            db_comp_name_case += ' ' * 8 + 'case ' + dbc_name + \
                ': return QLatin1String("' + tbl + '");\n'
            db_table_name_case += ' ' * 8 + 'case ' + dbt_name + \
                ': return QLatin1String("' + tbl + '");\n'
            db_name_to_id += ' ' * 8 + 'if (!value.compare(QLatin1String("' + \
                tbl + '"), Qt::CaseInsensitive)) return ' + dbc_name + ';\n'
            db_new_components += ' ' * 8 + 'case ' + dbc_name + \
                ': return new ' + with_nspace + '();\n'


        db_view_id = ''
        db_views_constr = ''
        db_view_name_case = ''
        for view in self.views:
            with_nspace = nspace_prefix + view
            dbc_name = 'DBC_' + view.upper()
            dbv_name = 'DBV_' + view.upper()
            db_comp_id += ' ' * 8 + dbc_name + ',\n'
            db_view_id += ' ' * 8 + dbv_name + ',\n'
            db_views_constr += '    static ' + with_nspace + ' ' + \
                view.lower() + ' () { return ' + with_nspace + \
                '(); }\n'
            db_comp_name_case += ' ' * 8 + 'case ' + dbc_name + \
                ': return QLatin1String("' + view + '");\n'
            db_view_name_case += ' ' * 8 + 'case ' + dbv_name + \
                ': return QLatin1String("' + view + '");\n'
            db_name_to_id += ' ' * 8 + 'if (!value.compare(QLatin1String("' + \
                view + '"), Qt::CaseInsensitive)) return ' + dbc_name + ';\n'
            all_hdr += '#include "' + view.lower() + '.h"\n'
            all_meta_hdr += '#include "' + view.lower() + '-meta.h"\n'
            db_new_components += ' ' * 8 + 'case ' + dbc_name + \
                ': return new ' + with_nspace + '();\n'

        self.data['BaseClass'] = 'DbStructMeta'
        self.data['baseclass'] = 'dbstructmeta'
        self.data['BASECLASS'] = 'DBSTRUCTMETA'
        self.data['INCLUDE_ALL_HEADERS'] = all_hdr
        self.data['INCLUDE_ALL_META_HEADERS'] = all_meta_hdr
        self.data['DBC_IDS'] = db_comp_id
        self.data['DB_TABLE_IDS'] = db_table_id
        self.data['DB_VIEW_IDS'] = db_view_id
        self.data['DB_TABLES_CONSTR'] = db_tables_constr
        self.data['DB_VIEWS_CONSTR'] = db_views_constr
        self.data['DB_COMPONENTS_NAME_CASE'] = db_comp_name_case
        self.data['DB_TABLES_NAME_CASE'] = db_table_name_case
        self.data['DB_VIEWS_NAME_CASE'] = db_view_name_case
        self.data['DB_COMPONENTS_NAME_TO_ID'] = db_name_to_id
        self.data['DB_NEW_COMPONENTS'] = db_new_components

        with open(os.path.join(self.out_dir, self.data['database'] + '.h'), 'w') as f:
            file.write(f, self.getTemplate ('database.h.template') % self.data)

        with open(os.path.join(self.out_dir, self.data['database'] + '.cc'), 'w') as f:
            file.write(f, self.getTemplate ('database.cc.template') % self.data)

        with open(os.path.join(self.out_dir, 'all-meta-tables.h'), 'w') as f:
            file.write(f, self.getTemplate ('all-meta-tables.h.template') % self.data)

        with open(os.path.join(self.out_dir, 'all-tables.h'), 'w') as f:
            file.write(f, self.getTemplate ('all-tables.h.template') % self.data)

        self.db_name = ''

    def bootstrapData(self, name):
        '''Add common data in the variable map'''
        now = datetime.datetime.now()
        self.data = {
            'Database': self.db_name,
            'database': self.db_name.lower(),
            'DATABASE': self.db_name.upper(),
            'Table': name,
            'table': name.lower(),
            'TABLE': name.upper(),
            'Namespace': self.namespace,
            'namespace': self.namespace.lower(),
            'NAMESPACE': self.namespace.upper(),
            'BaseClass': self.base_class,
            'baseclass': self.base_class.lower(),
            'BASECLASS': self.base_class.upper(),
            'MetaClassInclude': META_TABLE_BASE_FILE,
            'RecordBaseClass': RECORD_BASE,
            'EXPORT': self.export_macro,
            'IMPORTH': '#include <%s>' % self.import_header,
            'Year': str(now.year),
            'Month': now.strftime("%B"),
            'Author': AUTHOR
        }

    def tableStart(self, name, node):
        '''Starting to process table `name`'''
        self.tables[name] = {}
        self.columns = OrderedDict()
        self.bootstrapData(name)
        self.vrtcols = []

    def fillTableData(self, name):
        '''Prepare values for variables in the context of this table'''

        id_column = -1
        pipe_columns = ''
        case_columns = ''
        case_label = ''
        model_label = ''
        bind_columns = ''
        bind_one_column = ''
        comma_columns = ''
        column_columns = ''
        assign_columns = ''
        comma_columns_no_id = ''
        retreive_columns = ''
        record_columns = ''
        rec_to_map = ''
        rec_from_map = ''
        column_getters = ''
        column_index_getters = ''
        table_data_members = ''
        default_constr = ''
        assign_constr = ''
        copy_constr = ''
        real_column_mapping = ''
        virtual_column_mapping = ''
        set_table_defaults = ''
        i = -1
        real_id = 0

        column_ids = ''
        for i, col in enumerate(self.columns):
            coldata = self.columns[col]
            col_var_name = col.lower()
            qtype = coldata['qtype']
            defval = coldata['defval']
            to_cast = TO_CAST[qtype]
            to_converter = FROM_VARIANT[qtype]
            dbc_name = 'COLID_' + col.upper()
            column_ids += ' ' * 8 + dbc_name + ',\n'
            column_label = 'QCoreApplication::translate("' + self.db_name + \
                '::' + name + '", "' + coldata['label'] + '")'

            col_mapping_nicety = '/* ' + dbc_name + ' -> */ '
            col_mapping_nicety += ' ' * (64 - len(col_mapping_nicety))
            real_column_mapping += 4*' ' + col_mapping_nicety
            if not coldata['virtual']:
                real_column_mapping += str(real_id) + ',\n'
                virtual_column_mapping += 4*' ' + col_mapping_nicety + str(i) + ',\n'
                if col == 'id':
                    id_column = i
                    if coldata['autoincrement']:
                        default_constr = default_constr + ' ' * 8 + col_var_name + \
                            '(COLID_INVALID),\n'
                    elif qtype == 'QString':
                        default_constr = default_constr + ' ' * 8 + col_var_name + \
                            '(QLatin1String("-1")),\n'
                    else:
                        default_constr = default_constr + ' ' * 8 + col_var_name + \
                            '(),\n'
                else:
                    default_constr = default_constr + ' ' * 8 + \
                        col_var_name + '(),\n'
                    comma_columns_no_id += ' ' * 12 + '"' + col + ',"\n'
                    column_columns += ' ' * 12 + '":' + col + ',"\n'
                    assign_columns += ' ' * 12 + '"' + col + '=:' + col + ',"\n'
                pipe_columns += ' ' * 8 + '<< QLatin1String("' + col + '")\n'
                bind_one_column += ' ' * 4 + 'case ' + dbc_name + \
                    ': query.bindValue (QLatin1String(":' + col + '"), ' + \
                    col_var_name + '); break;\n'
                bind_columns += ' ' * 4 + 'query.bindValue (QLatin1String(":' + \
                    col + '"), ' + col_var_name + ');\n'
                comma_columns += ' ' * 12 + '"' + col + ',"\n'
            else:
                real_column_mapping += '-1,\n'
                default_constr = default_constr + ' ' * 8 + \
                    col_var_name + '(),\n'

            assign_constr = assign_constr + ' ' * 8 + col_var_name + \
                ' = other.' + col_var_name + ';\n'
            copy_constr = copy_constr + ' ' * 8 + col_var_name + \
                ' (other.' + col_var_name + '),\n'

            table_data_members += ' ' * 4 + qtype + ' ' + col.lower() + ';\n'
            case_label += ' ' * 4 + 'case ' + dbc_name + ': result = ' + \
                column_label + '; break;\n'
            case_columns += ' ' * 4 + 'case ' + dbc_name + \
                ': result = QLatin1String("' + col + '"); break;\n'
            model_label += ' ' * 4 + 'model->setHeaderData (' + dbc_name + \
                ', Qt::Horizontal, ' + column_label + ');\n'


            # definition related to foreign keys
            fkey_data = coldata['fkey']
            if fkey_data:

                fkey_col = '%40s, %30s, %30s, %15s' % (
                    'QLatin1String("%s")' % fkey_data[0],
                    'QLatin1String("%s")' % fkey_data[1],
                    'QLatin1String("%s")' % fkey_data[2] if fkey_data[2] else 'QString()',
                    'DbColumn::FB_CHOOSE' if fkey_data[3] == '' or fkey_data[3] == 'choose' else 'DbColumn::FB_CHOOSE_ADD')

#                fkey_col = 'QLatin1String("' + fkey_data[0] + \
#                    '"), QLatin1String("' + fkey_data[1] + '"), '
#                if fkey_data[2]:
#                    fkey_col += 'QLatin1String("' + fkey_data[2] + '")'
#                else:
#                    fkey_col += 'QString()'
#                if fkey_data[3] == '' or fkey_data[3] == 'choose':
#                    fkey_col += ', DbColumn::FB_CHOOSE'
#                else:
#                    fkey_col += ', DbColumn::FB_CHOOSE_ADD'
            else:
                fkey_col = '%40s, %30s, %30s, %15s' % (
                    'QString()', 'QString()',
                    'QString()', 'DbColumn::FB_CHOOSE')

            # the other column for virtual columns
            try:
                virt_ref_col = 'COLID_' + coldata['reference'].upper()
            except KeyError:
                virt_ref_col = None

            # constructor for column
            column_create = 'DbColumn (%40s,%25s,%6d,%6d,%80s,%30s,%7s,%7s,%25s,%40s,%7s,%16s,%s)' % (
                'QLatin1String("%s")' % col,
                dbc_name,
                real_id,
                int(coldata['length']) if coldata['length'] else -1,
                column_label,
                'DbColumn::DTY_%s' % coldata['datatype'].upper(),
                'true' if coldata['nulls'] else 'false',
                'true' if coldata['autoincrement'] else 'false',
                'QLatin1String("%s")' % coldata['defexpr'] if coldata['defexpr'] else 'QString()',
                'QLatin1String("%s")' % coldata['format'] if coldata['format'] else 'QString()',
                'true' if coldata['ronly'] else 'false',
                virt_ref_col if coldata['virtual'] else '-1',
                fkey_col
            )
#            column_create = 'DbColumn("' + \
#                col + '", ' + \
#                dbc_name + ', '+ \
#                str(real_id) + ', '+ \
#                stringChoice(coldata['length'], '-1', coldata['length']) + \
#                ', ' + column_label + ', '  + \
#                'DbColumn::DTY_' + coldata['datatype'].upper() + ', ' + \
#                stringChoice('true', 'false', coldata['nulls']) + ', ' + \
#                stringChoice('true', 'false', coldata['autoincrement']) + \
#                ', QLatin1String("' + stringChoice('', coldata['defexpr'],
#                    coldata['defexpr'] is None) + '")' + \
#                ', QLatin1String("' + stringChoice('', coldata['format'],
#                    coldata['format'] is None) + '"), ' + \
#                stringChoice('true', 'false', coldata['ronly']) + ', ' + \
#                stringChoice(virt_ref_col, '-1', coldata['virtual']) + \
#                ', ' + fkey_col + ')'


            column_getters += \
                '    static DbColumn %10sColCtor () { return %s; }\n' % (
                    col.lower(), column_create)
            column_index_getters += \
                '    case %20s: return %s;\n' % (
                    dbc_name, column_create)
            retreive_columns += \
                '    %16s = %10squery.value (%20s).%s;\n' % (
                    col_var_name, to_cast, dbc_name, to_converter)
            record_columns += \
                '    %20s = %10srec.value (%40s).%s;\n' % (
                col_var_name, to_cast,
                'QLatin1String("%s")' % col,
                to_converter)
            rec_to_map += \
                '    result.insert(%40s, %30s);\n' % (
                'QLatin1String ("%s")' % col,
                'QVariant (%s)' % col_var_name)
            rec_from_map += \
                '        if (!i.key ().compare (%40s)) { %20s = i.value ().%s; }\n' % (
                'QLatin1String ("%s")' % col,
                col_var_name,
                to_converter)

#            column_getters += ' ' * 4 + 'static DbColumn ' + col.lower() + \
#                'ColCtor () { return ' + column_create + '; }\n'
#            column_index_getters += ' ' * 4 + 'case ' + dbc_name + \
#                ': return ' + column_create + ';\n'
#            retreive_columns += ' '*4 + col_var_name + ' = ' + to_cast + \
#                'query.value (' + dbc_name + ').' + to_converter + ';\n'
#            record_columns += ' '*4 + col_var_name + ' = ' + to_cast + \
#                'rec.value (QLatin1String("' + col + '")).' + \
#                to_converter + ';\n'
#            rec_to_map += ' '*4 + 'result.insert(QLatin1String ("' + col + \
#                '"), QVariant (' + col_var_name + '));\n'
#            rec_from_map += ' '*8 + 'if (!i.key ().compare (QLatin1String ("' + \
#                col + '"))) { ' + col_var_name + ' = i.value ().' + to_converter + '; }\n'
            if defval:
                set_table_defaults += make_value_setter (col_var_name, defval, qtype)

            real_id = real_id + (not coldata['virtual'])

        int_types = ['long', 'integer', 'bigint', 'smallint', 'tinyint']
        if id_column == -1:
            id_column = 'COLID_INVALID'
            get_id_result = 'COLID_INVALID'
            set_id = '// id unavailable in this model'
        elif self.columns['id']['datatype'] in int_types:
            get_id_result = 'id'
            set_id = 'id = value'
        else:
            get_id_result = 'COLID_INVALID'
            set_id = '// id unavailable in this model'

        default_constr = default_constr[:-2]
        copy_constr = copy_constr[:-2]
        assign_constr = assign_constr[:-1]
        pipe_columns = pipe_columns[:-1]
        case_columns = case_columns[:-1]
        bind_columns = bind_columns[:-1]
        bind_one_column = bind_one_column[:-1]
        comma_columns = comma_columns[:-3] + '"'
        comma_columns_no_id = comma_columns_no_id[:-3] + '"'
        column_columns = column_columns[:-3] + '"'
        assign_columns = assign_columns[:-3] + '"'
        real_column_mapping = real_column_mapping[:-2]
        virtual_column_mapping = virtual_column_mapping[:-2]

        self.data['COLUMN_COUNT'] = str(len(self.columns))
        self.data['PIPE_COLUMNS'] = pipe_columns
        self.data['CASE_COLUMNS'] = case_columns
        self.data['CASE_LABELS'] = case_label
        self.data['MODEL_LABELS'] = model_label
        self.data['BIND_COLUMNS'] = bind_columns
        self.data['RETREIVE_COLUMNS'] = retreive_columns
        self.data['RECORD_COLUMNS'] = record_columns
        self.data['BIND_ONE_COLUMN'] = bind_one_column
        self.data['ID_COLUMN'] = str(id_column)
        self.data['GET_ID_RESULT'] = str(get_id_result)
        self.data['SET_ID_RESULT'] = str(set_id)
        self.data['COMMA_COLUMNS'] = comma_columns
        self.data['COMMA_COLUMNS_NO_ID'] = comma_columns_no_id
        self.data['COLUMN_COLUMNS'] = column_columns
        self.data['ASSIGN_COLUMNS'] = assign_columns
        self.data['COLUMN_IDS'] = column_ids
        self.data['TableColumnConstr'] = column_getters
        self.data['TableColumnsIndexCtor'] = column_index_getters
        self.data['TableDataMembers'] = table_data_members
        self.data['CopyConstructor'] = copy_constr
        self.data['AssignConstructor'] = assign_constr
        self.data['DefaultConstructor'] = default_constr
        self.data['RecToMap'] = rec_to_map
        self.data['RecFromMap'] = rec_from_map
        self.data['SetTableDefaults'] = set_table_defaults
        self.data['SetTableOverrides'] = ''
        self.data['RealColumnMapping'] = real_column_mapping
        self.data['VirtualColumnMapping'] = virtual_column_mapping

    def tableEnd(self, name, node):
        '''Done processing table `name`'''
        self.tables[name]['columns'] = self.columns

        for vrtcol in  self.vrtcols:
            vrtdata = self.columns[vrtcol]
            coldata = self.columns[vrtdata['reference']]
            for okey in coldata:
                if not okey in vrtdata:
                    vrtdata[okey] = coldata[okey]
            print vrtdata

        self.fillTableData(name)

        with open(os.path.join(self.out_dir, self.data['table'] + '.h'), 'w') as f:
            file.write(f, self.getTemplate ('table.h.template') % self.data)

        with open(os.path.join(self.out_dir, self.data['table'] + '-meta.h'), 'w') as f:
            file.write(f, self.getTemplate ('table-meta.h.template') % self.data)

        with open(os.path.join(self.out_dir, self.data['table'] + '.cc'), 'w') as f:
            file.write(f, self.getTemplate ('table.cc.template') % self.data)

        with open(os.path.join(self.out_dir, self.data['table'] + '-meta.cc'), 'w') as f:
            file.write(f, self.getTemplate ('table-meta.cc.template') % self.data)

    def column(self, name, label, datatype, nulls, node, dtnode):
        '''Processing a column'''

        # see if this is one of those virtual columns
        if datatype == 'vrtcol':
            # we should not expect the reference column
            # to be already defined so we defer the processing
            # for the end of the table

            self.columns[name] = {
                'virtual': True,
                'label': label,
                'ronly': True,
                'reference': dtnode.references,
                'foreignInsert': node.foreignInsert
            }
            self.vrtcols.append(name)

        else:
            # the datatype
            try:
                length = dtnode.length
            except AttributeError:
                length = None
            # any defaults?
            try:
                defval = dtnode.default
            except AttributeError:
                defval = None
            try:
                defexpr = dtnode.defaultExpression
            except AttributeError:
                defexpr = None
            if defval:
                defexpr = defval
            # auto-incrementing
            try:
                identity = dtnode.identity
            except AttributeError:
                identity = None
            try:
                read_only = node.readOnly
            except AttributeError:
                read_only = False
            try:
                format_str = node.userformat
            except AttributeError:
                format_str = None

            qtype = dtnode.qtype
            if not qtype:
                qtype = datatype

            self.columns[name] = {
                'virtual': False,
                'qtype': qtype,
                'label': label,
                'length': length,
                'nulls': nulls,
                'defexpr': defexpr,
                'defval': defval,
                'autoincrement': not identity is None,
                'datatype': datatype,
                'fkey': self.getForeignKey(node),
                'format': format_str,
                'ronly': read_only
            }

    def viewStart(self, name, node):
        '''Starting to process view `name`'''
        self.views[name] = {}
        self.bootstrapData(name)
        self.columns = OrderedDict()

    def viewEnd(self, name, node):
        '''Done processing view `name`'''

        self.views[name]['columns'] = self.columns

        name = name.lower()

        with open(os.path.join(self.out_dir, name + '.h'), 'w') as f:
            file.write(f, self.getTemplate ('view.h.template') % self.data)

        with open(os.path.join(self.out_dir, name + '-meta.h'), 'w') as f:
            file.write(f, self.getTemplate ('view-meta.h.template') % self.data)

        with open(os.path.join(self.out_dir, name + '.cc'), 'w') as f:
            file.write(f, self.getTemplate ('view.cc.template') % self.data)

        with open(os.path.join(self.out_dir, name + '-meta.cc'), 'w') as f:
            file.write(f, self.getTemplate ('view-meta.cc.template') % self.data)

    def viewSubset(self, node, subset):
        '''Process a subset in a view'''
        name1 = subset.name1
        col1 = subset.col1
        name_in = subset.in_
        incol = subset.incol
        where = subset.where
        constraint = subset.constraint
        value = subset.value

        self.columns = self.tables[name1]['columns']
        self.fillTableData(name1)

        defaults = {}
        for col in self.columns:
            coldata = self.columns[col]
            defaults[col] = coldata['defval']

        self.data['TableModify'] = name1
        self.data['BaseClass'] = 'DbView'
        self.data['baseclass'] = 'dbview'
        self.data['BASECLASS'] = 'DBVIEW'

        force_values = {}
        if hasattr(node, 'writeback'):
            self.data['TableModify'] = node.writeback.table
            if hasattr(node.writeback, 'column'):
                for column in node.writeback.column:
                    if hasattr(column, 'value'):
                        force_values[column.name] = column.value
                    if hasattr(column, 'default'):
                        defaults[column.name] = column.default

        set_table_overrides = ''
        for col in force_values:
            col_var_name = col.lower()
            colval = force_values[col]
            if colval is not None:
                set_table_overrides += make_value_setter (col_var_name, colval, \
                    self.columns[col]['qtype'])
        set_table_defaults = ''
        for col in defaults:
            col_var_name = col.lower()
            colval = defaults[col]
            if colval is not None:
                set_table_defaults += make_value_setter (col_var_name, colval, \
                    self.columns[col]['qtype'])

        self.data['SetTableDefaults'] = set_table_defaults
        self.data['SetTableOverrides'] = set_table_overrides


        if name_in is None:
            # only a primary table
            pass
        else:
            # a primary and a secondary
            pass

    def getTemplate(self, which):
        '''Read the content of a template file'''
        if not which in self.templates:
            with open(os.path.join(self.template_dir, which), 'r') as f:
                self.templates[which] = f.read()
        return self.templates[which]

# ----------------------------------------------------------------------------

class SqLiteDriver(SqlDriver):
    '''
    SqLite specifics.
    '''
    def __init__(self):
        super(SqLiteDriver, self).__init__()


# ----------------------------------------------------------------------------

def validate(xmlfilename):
    '''
    Validates a file and returns the xml tree.
    '''
    with open(xmlfilename, 'r') as f:
        return validateString(f.read())

# ----------------------------------------------------------------------------

def validateString(xmlstring):
    '''
    Validates a string and returns the xml tree.
    '''
    global NSPACESTR

    try:
        xml_root = pile_schema_api.parseString(xmlstring, silence=True)
        # xml_root = etree.fromstring(xmlstring, PARSER)

        #if NSPACESTR is None:
        #    namespace = xml_root.nsmap[None]
        #    NSPACESTR = '{' + namespace + '}'

        return xml_root
    except (etree.XMLSchemaError, etree.XMLSyntaxError) as exc:
        logger.error('Schema validation failed: ' + str(exc))
        return None

# ----------------------------------------------------------------------------

def str2bool(v):
    if v is None:
        return False
    if type(v) is bool:
        return v
    return v.lower() in ("yes", "true", "t", "1")

# ----------------------------------------------------------------------------

def stringChoice(s1, s2, choice):
    return str(s1) if choice else str(s2)

# ----------------------------------------------------------------------------

def processWithDriver(driver, database):
    '''
    '''
    driver.databaseStart (database.name, database)

    tables = database.tables
    views = database.views

    for table in tables.table:
        driver.tableStart (table.name, table)

        columns = table.columns
        for column in columns.column:

            datatype_name = ''
            datatype = None
            for kkk in dir(column):
                # This is a hack; it exists because the generated class does no
                # provide any means to iterate child elements
                # It relies on the assumption that all elements are custom types
                if str(type(getattr(column, kkk))).find('class') > 0:
                    datatype = getattr(column, kkk)
                    datatype_name = kkk
                    break

            driver.column (column.name,
                           stringChoice(column.label,
                                        column.name,
                                        column.label),
                           datatype_name,
                           str2bool(column.allowNulls),
                           column, datatype)



        driver.tableEnd (table.name, table)

    for view in views.view:
        driver.viewStart (view.name, view)
        subset = view.subset
        if subset is not None:
            driver.viewSubset(view, subset)
        else:
            logger.error('Unknown view type')
            return -1
        driver.viewEnd (view.name, view)

    driver.databaseEnd (database.name, database)


# ----------------------------------------------------------------------------

def extract_common (args):
    '''
    Extract common information from arguments and save it at module level.
    '''
    global AUTHOR, PARSER, SCHEMA_FILE

    if hasattr(args, 'author') and args.author is not None:
        AUTHOR = args.author

    if not hasattr(args, 'schema') or args.schema == None:
        args.schema = DEFAULT_SCHEMA_FILE;

    if SCHEMA_FILE != args.schema:
        SCHEMA_FILE = args.schema
        with open(args.schema, 'r') as f:
            schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)
        PARSER = etree.XMLParser(schema=schema, attribute_defaults=True)

# ----------------------------------------------------------------------------

def make_value_setter(var_name, var_value, qtype):
    result = ''
    result += ' '*4 + 'result->' + var_name + \
        ' = '
    if qtype == 'QString':
        result += 'QLatin1String ("' + var_value + '");\n'
    elif qtype == 'bool':
        result += str(var_value).lower() + ';\n'
    else:
        result += str(var_value) + ';\n'
    return result

# ----------------------------------------------------------------------------

def cmd_validate (args):
    '''
    Example:
    validate file.xml
    '''
    extract_common(args)
    if validate(args.xml):
        logger.info("%s validates" % args.xml)
        return 1
    else:
        logger.warning("%s doesn't validate" % args.xml)
        return 0

# ----------------------------------------------------------------------------

def cmd_sql (args):
    '''
    Example:
    sql file.xml
    '''
    global NSPACESTR

    extract_common(args)

    if (args.driver == 'none') or (args.driver == ''):
        driver = SqlDriver()
    elif args.driver == 'sqlite':
        driver = SqLiteDriver()
    else:
        logger.error('Unknown driver: ' + args.driver)
        return -1

    database = validate(args.xml)
    if database is None:
        return -1

    processWithDriver (driver, database)

    out_file = args.output
    if out_file is None:
        out_file = os.path.splitext(args.xml)[0] + '.sql'
    with open(out_file, 'w') as f:
        f.write (driver.sql_string)
    return 0

# ----------------------------------------------------------------------------

def cmd_qt (args):
    '''
    Example:
    qt file.xml
    '''
    global NSPACESTR

    extract_common(args)

    if args.driver == 'qt':
        driver = QtDriver(
            out_dir=args.output,
            template_dir=args.templates,
            namespace=args.namespace,
            export_macro=args.exportm,
            import_header=args.importh)
    else:
        logger.error('Unknown driver: ' + args.driver)
        return -1

    database = validate(args.xml)
    if database is None:
        return -1

    processWithDriver(driver, database)

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
    parser.add_argument('--level-name', '-L',
                        action='store_true',
                        help='Display the log level (e.g. DEBUG, INFO) '
                             'for each logged message')
    parser.add_argument('--timestamp', '-T',
                        action='store_true',
                        help='Display human-readable timestamps for '
                             'each logged message')
    parser.add_argument('--verbose-logging', '-V',
                        action='store_true',
                        help='Display timestamp, log level and source '
                             'logger for every logged message '
                             '(implies -T).')
    parser.add_argument('--debug', '-D',
                        action='store_true',
                        help='Display any DEBUG-level log messages, '
                             'suppressed by default.')

    subparsers = parser.add_subparsers (help='Available sub-commands')

    parser_a = subparsers.add_parser('validate',
        help='Validate an xml against PileSchema.xsd')
    parser_a.add_argument ('xml', metavar="XML", type=str,
        help='input .xml file')
    parser_a.add_argument ('--schema', type=str,
        help='schema used for validation',
        default=DEFAULT_SCHEMA_FILE)
    parser_a.set_defaults (func=cmd_validate)

    parser_a = subparsers.add_parser ('sql',
        help='Generate an .sql file from input .xml')
    parser_a.add_argument ('xml', metavar="XML", type=str,
        help='input .xml file')
    parser_a.add_argument ('output', metavar="OUT",  type=str, nargs='?',
        help='output .sql file')
    parser_a.add_argument ('--schema', type=str,
        help='schema used for validation',
        default=DEFAULT_SCHEMA_FILE)
    parser_a.add_argument ('--driver', type=str,
        help='driver used for output',
        choices=['none', 'sqlite'], default='none')
    parser_a.add_argument ('--author', type=str,
        help='The author of the files',
        default=username())
    parser_a.set_defaults (func=cmd_sql)

    parser_a = subparsers.add_parser ('cpp',
        help='Generate C++ sources from input .xml')
    parser_a.add_argument ('xml', metavar="XML", type=str,
        help='input .xml file')
    parser_a.add_argument ('output', metavar="OUT",  type=str, nargs='?',
        help='output directory',
        default='.')
    parser_a.add_argument ('--driver', type=str,
        help='driver used for output',
        choices=['qt'], default='qt')
    parser_a.add_argument ('--namespace', type=str,
        help='top level namespace for generated output',
        default='')
    parser_a.add_argument ('--templates', type=str,
        help='directory containing file templates',
        default='qt-templates')
    parser_a.add_argument ('--schema', type=str,
        help='schema used for validation',
        default=DEFAULT_SCHEMA_FILE)
    parser_a.add_argument ('--author', type=str,
        help='The author of the files',
        default=username())
    parser_a.add_argument ('--exportm', type=str,
        help='The macro used to export functions and classes',
        default='')
    parser_a.add_argument ('--importh', type=str,
        help='Header file to be imported in every generated header',
        default='')
    parser_a.set_defaults (func=cmd_qt)

    return parser

# ----------------------------------------------------------------------------

def setupLogger(args):
    '''
    Prepares the logger.
    '''
    logging.basicConfig()
    return
    # Set up the root logger with a custom handler that logs stdout for INFO
    # and DEBUG and stderr for WARNING, ERROR, CRITICAL.
    root_logger = logging.getLogger()
    if args.verbose_logging:
        pass
        #formatter = logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s "
        #                                  "%(message)s")
        #handler = CustomStreamHandler(formatter=formatter)
    else:
        if args.timestamp:
            prefix = '%(asctime)s '
        else:
            prefix = ''
        #formatter = CustomFormatter(prefix=prefix) #, only_from='pylearn2')
        #handler = CustomStreamHandler(formatter=formatter)
    #root_logger.addHandler(handler)

    # Set the root logger level.
    if args.debug:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    return root_logger

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    '''
    See module-level docstring for a description of the script.
    '''
    parser = make_argument_parser ()
    args = parser.parse_args ()
    setupLogger (args)
    args.func (args)

