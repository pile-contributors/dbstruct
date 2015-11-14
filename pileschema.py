#!/usr/bin/env python
"""
Script implementing all top level commands.

Basic usage:

.. code-block:: none

    pileschema.py command
    
    

"""

import argparse
from collections import OrderedDict
import logging
from lxml import etree
import os
import sys

PARSER = None
SCHEMA = None
DEFAULT_SCHEMA_FILE = './PileSchema.xsd'
NSPACESTR = None
logger = logging.getLogger('PileSchema')
FROM_VARIANT = {
    'QString': 'toString ()',
    'bool': 'toBool ()',
    'long': 'toLongLong (&b_one); b_ret = b_ret & b_one',
    'byte': 'toInt (&b_one); b_ret = b_ret & b_one',
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
    'byte': '(byte)',
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
    """
    Default implementation with regard to the underlying
    Sql variant.
    """
    def __init__(self):
        super(Driver, self).__init__()

    def databaseStart(self, name, node):
        """Starting to process database `name`"""
        pass
    
    def databaseEnd(self, name, node):
        """Done processing database `name`"""
        pass

    def tableStart(self, name, node):
        """Starting to process table `name`"""
        pass
    
    def tableEnd(self, name, node):
        """Done processing table `name`"""
        pass

    def column(self, name, label, datatype, nulls, node, dtnode):
        """Processing a column"""
        pass

    def viewStart(self, name, node):
        """Starting to process view `name`"""
        pass
    
    def viewEnd(self, name, node):
        """Done processing view `name`"""
        pass
    
    def viewSubset(self, node, subset):
        """Process a subset in a view"""
        pass

# ----------------------------------------------------------------------------

class SqlDriver(Driver):
    """
    Default implementation with regard to the underlying
    Sql variant.
    """
    def __init__(self):
        self.sql_string = ''
        super(SqlDriver, self).__init__()

    def tableStart(self, name, node):
        """Starting to process table `name`"""
        self.sql_string += 'CREATE TABLE IF NOT EXISTS `' + name + '` (\n'
    
    def tableEnd(self, name, node):
        """Done processing table `name`"""
        pkey = node.find(NSPACESTR + 'primaryKey')
        if pkey is not None:
            pkey = pkey.getchildren()[0] # key
            if pkey is not None:
                pkey = pkey.getchildren()[0] # column

        if pkey is not None:
            self.sql_string += '  PRIMARY KEY (`' + pkey.get('name') + '`)\n'
        elif (self.sql_string[-2] == ',') and (self.sql_string[-1] == '\n'):
            # get rid of last comma
            self.sql_string = self.sql_string[:-2] + '\n'
        self.sql_string += ');\n'

    def column(self, name, label, datatype, nulls, node, dtnode):
        """Processing a column"""
        # first comes the name
        self.sql_string += '  `' + name + '` '
        # then the datatype
        length = dtnode.get('length')
        if length:
            self.sql_string += datatype + '(' + length + ') '
        else:
            self.sql_string += datatype + ' '
        # any defaults
        defval = dtnode.get('default')
        defexpr = dtnode.get('defaultExpression')
        if defval:
            self.sql_string += 'DEFAULT ' + defval
        elif defexpr:
            self.sql_string += 'DEFAULT ' + defexpr
        # null constraint
        if (not nulls):
            self.sql_string += 'NOT NULL '
        # auto-incrementing
        identity = dtnode.find(NSPACESTR + 'identity')
        if not identity is None:
            self.sql_string += 'AUTO_INCREMENT '
        if self.sql_string[-1] == ' ':
            self.sql_string = self.sql_string[:-1]
        # and that's it folks
        self.sql_string += ',\n'

    def viewStart(self, name, node):
        """Starting to process view `name`"""
        self.sql_string += 'CREATE VIEW IF NOT EXISTS `' + name + '` AS\n'
    
    def viewEnd(self, name, node):
        """Done processing view `name`"""
        self.sql_string += ';\n'
    
    def viewSubset(self, node, subset):
        """Process a subset in a view"""
        name1 = subset.get('name1')
        col1 = subset.get('col1')
        name_in = subset.get('in')
        incol = subset.get('incol')
        where = subset.get('where')
        constraint = subset.get('constraint')
        value = subset.get('value')

        if name_in is None:
            # only a primary table
            self.sql_string += '  SELECT * FROM ' + name1 + ' WHERE ' + col1 + constraint + value + '\n'
        else:
            # a primary and a secondary
            self.sql_string += '  SELECT * FROM ' + name1 + ' WHERE ' + col1 + ' IN (\n' + \
                               '    SELECT ' + incol + ' FROM ' + name_in + ' WHERE ' + where + constraint + value + ')\n'


# ----------------------------------------------------------------------------

class QtDriver(Driver):
    """
    Build C++ classes with Qt support.
    """
    def __init__(self, out_dir, template_dir, namespace='', export_macro='', base_class='Xx'):
        self.out_dir = out_dir
        self.template_dir = template_dir
        self.data = {}
        self.templates = {}
        self.db_name = ''
        self.namespace = namespace
        self.export_macro = export_macro
        self.base_class = base_class
        self.tables = OrderedDict()
        self.views = OrderedDict()
        self.columns = OrderedDict()
        super(QtDriver, self).__init__()

    def databaseStart(self, name, node):
        """Starting to process database `name`"""
        self.db_name = name
    
    def databaseEnd(self, name, node):
        """Done processing database `name`"""

        all_hdr = ''
        all_meta_hdr = ''
        db_comp_id = ''
        db_table_id = ''
        db_tables_constr = ''
        db_comp_name_case = ''
        db_table_name_case = ''
        db_name_to_id = ''
        for tbl in self.tables:
            dbc_name = 'DBC_' + tbl.upper()
            dbt_name = 'DBT_' + tbl.upper()
            all_hdr += '#include "' + tbl.lower() + '.h"\n'
            all_meta_hdr += '#include "' + tbl.lower() + '-meta.h"\n'
            db_comp_id += ' ' * 8 + dbc_name + ',\n'
            db_table_id += ' ' * 8 + dbt_name + ',\n'
            db_tables_constr += '    static meta::' + tbl + ' ' + tbl.lower() + ' () { return meta::' + tbl + '(); }\n'
            db_comp_name_case += ' ' * 8 + 'case ' + dbc_name + ': return QLatin1String("' + tbl + '");\n'
            db_table_name_case += ' ' * 8 + 'case ' + dbt_name + ': return QLatin1String("' + tbl + '");\n'
            db_name_to_id += ' ' * 8 + 'if (!value.compare(QLatin1String("' + tbl + '"), Qt::CaseInsensitive)) return ' + dbc_name + ';\n'

        db_view_id = ''
        db_views_constr = ''
        db_view_name_case = ''
        for view in self.views:
            dbc_name = 'DBC_' + tbl.upper()
            dbv_name = 'DBV_' + tbl.upper()
            db_comp_id += ' ' * 8 + dbc_name + ',\n'
            db_view_id += ' ' * 8 + dbv_name + ',\n'
            db_views_constr += '    static meta::' + view + ' ' + view.lower() + ' () { return meta::' + view + '(); }\n'
            db_comp_name_case += ' ' * 8 + 'case ' + dbc_name + ': return QLatin1String("' + view + '");\n'
            db_view_name_case += ' ' * 8 + 'case ' + dbv_name + ': return QLatin1String("' + view + '");\n'
            db_name_to_id += ' ' * 8 + 'if (!value.compare(QLatin1String("' + view + '"), Qt::CaseInsensitive)) return ' + dbc_name + ';\n'

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

        with open(os.path.join(self.out_dir, self.data['database'] + '.h'), 'w') as f:
            file.write(f, self.getTemplate ('database.h') % self.data)

        with open(os.path.join(self.out_dir, self.data['database'] + '.cc'), 'w') as f:
            file.write(f, self.getTemplate ('database.cc') % self.data)

        with open(os.path.join(self.out_dir, 'all-meta-tables.h'), 'w') as f:
            file.write(f, self.getTemplate ('all-meta-tables.h') % self.data)

        with open(os.path.join(self.out_dir, 'all-tables.h'), 'w') as f:
            file.write(f, self.getTemplate ('all-tables.h') % self.data)

        self.db_name = ''

    def tableStart(self, name, node):
        """Starting to process table `name`"""
        self.tables[name] = {}
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
            'EXPORT': self.export_macro
        }
        self.columns = OrderedDict()
    
    def tableEnd(self, name, node):
        """Done processing table `name`"""
        self.tables[name]['columns'] = self.columns

        id_column = -1
        pipe_columns = ''
        case_columns = ''
        bind_columns = ''
        bind_one_column = ''
        comma_columns = ''
        column_columns = ''
        assign_columns = ''
        comma_columns_no_id = ''
        retreive_columns = ''
        record_columns = ''
        column_getters = ''
        table_data_members = ''
        i = -1

        column_ids = ''
        for i, col in enumerate(self.columns):
            coldata = self.columns[col]
            qtype = coldata['qtype']
            to_cast = TO_CAST[qtype]
            to_converter = FROM_VARIANT[qtype]
            dbc_name = 'COLID_' + col.upper()
            column_ids += ' ' * 8 + dbc_name + ',\n'
            if col == 'id':
                id_column = i
            table_data_members += ' ' * 4 + qtype + ' ' + col.lower() + ';\n'
            pipe_columns += ' ' * 8 + '<< "' + col + '"\n'
            case_columns += ' ' * 4 + 'case ' + str(i) + ': result = "' + col + '"; break;\n'
            bind_one_column += ' ' * 4 + 'case ' + str(i) + ': query.bindValue (":' + col + '", ' + col + '); break;\n'
            comma_columns += ' ' * 12 + '"' + col + ',"\n'
            bind_columns += ' ' * 4 + 'query.bindValue (":' + col + '", ' + col + ');\n'
            column_getters += ' ' * 4 + 'static DbColumn ' + col.lower() + \
                              'Column () { return DbColumn("' + \
                              col + '", ' + \
                              dbc_name + ', '+ \
                              stringChoice(coldata['length'], '-1', coldata['length']) + ', "'  + \
                              coldata['label'] + '", "'  + \
                              coldata['datatype'] + '", ' + \
                              stringChoice('True', 'False', coldata['nulls']) + ', ' + \
                              stringChoice('True', 'False', coldata['autoincrement']) + ', "' + \
                              stringChoice(coldata['defval'], '', not coldata['defval'] is None) + '"); }\n'
            if col != 'id':
                comma_columns_no_id += ' ' * 12 + '"' + col + ',"\n'
                column_columns += ' ' * 12 + '":' + col + ',"\n'
                assign_columns += ' ' * 12 + '"' + col + '=:' + col + ',"\n'
            retreive_columns += ' '*4 + col + ' = ' + to_cast + \
                'query.value (' + str(i) + ').' + to_converter + ';\n'
            record_columns += ' '*4 + col + ' = ' + to_cast + \
                'rec.value ("' + col + '").' + to_converter + ';\n'

        if id_column == -1:
            id_column = 'COLID_INVALID'
            get_id_result = 'COLID_INVALID'
            set_id = '// id unavailable in this model'
        elif self.columns['id']['datatype'] in ['long', 'int', 'bigint', 'smallint', 'tinyint']:
            get_id_result = 'id'
            set_id = 'id = value'
        else:
            get_id_result = 'COLID_INVALID'
            set_id = '// id unavailable in this model'
            

        pipe_columns = pipe_columns[:-1]
        case_columns = case_columns[:-1]
        bind_columns = bind_columns[:-1]
        bind_one_column = bind_one_column[:-1]
        comma_columns = comma_columns[:-3] + '"'
        comma_columns_no_id = comma_columns_no_id[:-3] + '"'
        column_columns = column_columns[:-3] + '"'
        assign_columns = assign_columns[:-3] + '"'

        self.data['COLUMN_COUNT'] = str(len(self.columns))
        self.data['PIPE_COLUMNS'] = pipe_columns
        self.data['CASE_COLUMNS'] = case_columns
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
        self.data['TableDataMembers'] = table_data_members

        with open(os.path.join(self.out_dir, self.data['table'] + '.h'), 'w') as f:
            file.write(f, self.getTemplate ('table.h') % self.data)

        with open(os.path.join(self.out_dir, self.data['table'] + '-meta.h'), 'w') as f:
            file.write(f, self.getTemplate ('table-meta.h') % self.data)

        with open(os.path.join(self.out_dir, self.data['table'] + '.cc'), 'w') as f:
            file.write(f, self.getTemplate ('table.cc') % self.data)

        with open(os.path.join(self.out_dir, self.data['table'] + '-meta.cc'), 'w') as f:
            file.write(f, self.getTemplate ('table-meta.cc') % self.data)

    def column(self, name, label, datatype, nulls, node, dtnode):
        """Processing a column"""

        # then the datatype
        length = dtnode.get('length')
        # any defaults
        defval = dtnode.get('default')
        defexpr = dtnode.get('defaultExpression')
        if not defval:
            defval = defexpr
        # auto-incrementing
        identity = dtnode.find(NSPACESTR + 'identity')
        qtype = dtnode.get('qtype')
        if not qtype:
            qtype = datatype

        self.columns[name] = {
            'qtype': qtype,
            'label': label,
            'length': length,
            'nulls': nulls,
            'defval': defval,
            'autoincrement': not identity is None,
            'datatype': datatype
        }

    def viewStart(self, name, node):
        """Starting to process view `name`"""
        pass
    
    def viewEnd(self, name, node):
        """Done processing view `name`"""
        pass
    
    def viewSubset(self, node, subset):
        """Process a subset in a view"""
        pass
    
    def getTemplate(self, which):
        """Read the content of a template file"""
        if not which in self.templates:
            with open(os.path.join(self.template_dir, which), 'r') as f:
                self.templates[which] = f.read()
        return self.templates[which]

# ----------------------------------------------------------------------------

class SqLiteDriver(SqlDriver):
    """
    SqLite specifics.
    """
    def __init__(self):
        super(SqLiteDriver, self).__init__()

    
# ----------------------------------------------------------------------------

def load_parser(schema_file=None):
    """
    Creates a parser from schema file.
    """
    global PARSER
    global SCHEMA

    if schema_file == None:
        schema_file = DEFAULT_SCHEMA_FILE;
    with open(schema_file, 'r') as f:
        schema_root = etree.XML(f.read())
    SCHEMA = etree.XMLSchema(schema_root)
    PARSER = etree.XMLParser(schema=SCHEMA, attribute_defaults=True)
    
# ----------------------------------------------------------------------------

def validate(xmlfilename):
    """
    Validates a file and returns the xml tree.
    """
    try:
        xml_root = None
        with open(xmlfilename, 'r') as f:
            xml_root = etree.fromstring(f.read(), PARSER) 
        return xml_root
    except etree.XMLSchemaError as exc:
        logger.error('Schema validation failed: ' + str(exc))
        return None

# ----------------------------------------------------------------------------

def validateString(xmlstring):
    """
    Validates a string and returns the xml tree.
    """
    try:
        xml_root = etree.fromstring(xmlstring, PARSER) 
        return xml_root
    except etree.XMLSchemaError as exc:
        logger.error('Schema validation failed: ' + str(exc))
        return None

# ----------------------------------------------------------------------------

def str2bool(v):
    if v is None:
        return False
    return v.lower() in ("yes", "true", "t", "1")
    
# ----------------------------------------------------------------------------

def stringChoice(s1, s2, choice):
    return str(s1) if choice else str(s2)

# ----------------------------------------------------------------------------

def processWithDriver(driver, database):
    """
    """
    driver.databaseStart (database.get('name'), database)

    tables = database.find(NSPACESTR + 'tables')
    views = database.find(NSPACESTR + 'views')

    for table in tables.iterchildren():
        driver.tableStart (table.get('name'), table)
        
        columns = table.find(NSPACESTR + 'columns')
        for column in columns.iterchildren():
            datatype = column.getchildren()[0]
            datatype_name = datatype.tag.replace(NSPACESTR, '')            
            driver.column (column.get('name'),
                           stringChoice(column.get('label'), column.get('name'), column.get('label')),
                           datatype_name, 
                           str2bool(column.get('allowNulls')),
                           column, datatype)
        driver.tableEnd (table.get('name'), table)

    for view in views.iterchildren():
        driver.viewStart (view.get('name'), view)
        subset = view.find(NSPACESTR + 'subset')
        if subset is not None:
            driver.viewSubset(view, subset)
        else:
            logger.error('Unknown view type')
            return -1
        driver.viewEnd (view.get('name'), view)

    driver.databaseEnd (database.get('name'), database)

# ----------------------------------------------------------------------------

def cmd_validate (args):
    """
    Example:
    validate file.xml
    """
    if not PARSER:
        load_parser(args.schema)
    if validate(args.xml):
        logger.info("%s validates" % args.xml)
        return 1
    else:
        logger.warning("%s doesn't validate" % args.xml)
        return 0

# ----------------------------------------------------------------------------

def cmd_sql (args):
    """
    Example:
    sql file.xml
    """
    global NSPACESTR

    if (args.driver == 'none') or (args.driver == ''):
        driver = SqlDriver()
    elif args.driver == 'sqlite':
        driver = SqLiteDriver()
    else:
        logger.error('Unknown driver: ' + args.driver)
        return -1

    if PARSER is None:
        load_parser(args.schema)

    database = validate(args.xml)
    if database is None:
        return -1

    if NSPACESTR is None:
        namespace = database.nsmap[None]
        NSPACESTR = '{' + namespace + '}'

    processWithDriver (driver, database)

    out_file = args.output
    if out_file is None:
        out_file = os.path.splitext(args.xml)[0] + '.sql'
    with open(out_file, 'w') as f:
        f.write (driver.sql_string)
    return 0

# ----------------------------------------------------------------------------

def cmd_qt (args):
    """
    Example:
    qt file.xml
    """
    global NSPACESTR

    if args.driver == 'qt':
        driver = QtDriver(args.output, args.templates, args.namespace)
    else:
        logger.error('Unknown driver: ' + args.driver)
        return -1

    if PARSER is None:
        load_parser(args.schema)

    database = validate(args.xml)
    if database is None:
        return -1

    if NSPACESTR is None:
        namespace = database.nsmap[None]
        NSPACESTR = '{' + namespace + '}'

    processWithDriver(driver, database)

    return 0

# ----------------------------------------------------------------------------

def make_argument_parser():
    """
    Creates an ArgumentParser to read the options for this script from
    sys.argv
    """
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
    
    parser_a = subparsers.add_parser('validate', help='Validate an xml against PileSchema.xsd')
    parser_a.add_argument ('xml', metavar="XML", type=str, help='input .xml file')
    parser_a.add_argument ('--schema', type=str, help='schema used for validation', default=DEFAULT_SCHEMA_FILE)
    parser_a.set_defaults (func=cmd_validate)

    parser_a = subparsers.add_parser ('sql', help='Generate an .sql file from input .xml')
    parser_a.add_argument ('xml', metavar="XML", type=str, help='input .xml file')
    parser_a.add_argument ('output', metavar="OUT",  type=str, nargs='?', help='output .sql file')
    parser_a.add_argument ('--schema', type=str, help='schema used for validation', default=DEFAULT_SCHEMA_FILE)
    parser_a.add_argument ('--driver', type=str, help='driver used for output', choices=['none', 'sqlite'], default='none')
    parser_a.set_defaults (func=cmd_sql)
  
    parser_a = subparsers.add_parser ('cpp', help='Generate C++ sources from input .xml')
    parser_a.add_argument ('xml', metavar="XML", type=str, help='input .xml file')
    parser_a.add_argument ('output', metavar="OUT",  type=str, nargs='?', help='output directory', default='.')
    parser_a.add_argument ('--driver', type=str, help='driver used for output', choices=['qt'], default='qt')
    parser_a.add_argument ('--namespace', type=str, help='top level namespace for generated output', default='')
    parser_a.add_argument ('--templates', type=str, help='directory containing file templates', default='qt-templates')
    parser_a.add_argument ('--schema', type=str, help='schema used for validation', default=DEFAULT_SCHEMA_FILE)
    parser_a.set_defaults (func=cmd_qt)

    return parser
    
# ----------------------------------------------------------------------------
    
def setupLogger(args):
    """
    Prepares the logger.
    """
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
    """
    See module-level docstring for a description of the script.
    """
    parser = make_argument_parser ()
    args = parser.parse_args ()
    setupLogger (args)
    args.func (args)

