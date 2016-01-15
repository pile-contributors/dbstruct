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
import pile_schema_api

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

class ForeignKey(object):
    '''
    A class that stores information about foreign keys.

    Parameters:
    ----------
    name : str
        The name of the column in current table.
    table : str
        The name of the foreign table.
    foreign_col : str
        The name of the column in foreign table.
    behaviour : str
        Allow the user to add new values or not.
    '''
    def __init__(self, name, table, foreign_col, behaviour):
        self.name = name
        self.table = table
        self.foreign_col = foreign_col
        self.prevent_add = behaviour in [None, '', 'choose']
        super(ForeignKey, self).__init__()

    @staticmethod
    def from_node(node):
        '''Retrieves the foreign key data from a node and returns the object'''
        if node.foreignTable:
            return ForeignKey(
                node.foreignColumn, node.foreignTable,
                node.foreignInsert, node.foreignBehavior)
        else:
            return None

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
        # the list of foreign keys as ForeignKey instances for current table
        self.foreign_keys = {}
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
        self.foreign_keys = {}

    def table_end(self, name, node):
        '''Done processing table `name`'''
        # if a primary key was defined then add it to the statement
        try:
            pkey = node.primaryKey.key.column[0]
            self.sql_string += '  PRIMARY KEY (`' + pkey.name + '`),\n'
        except AttributeError:
            pass
        # add collected foreign keys
        for fkey in self.foreign_keys:
            fdata = self.foreign_keys[fkey]
            self.append_foreign_key(fdata)
        # that should do it
        self.end_sql_statement()

    def column(self, name, label, datatype, nulls, node, dtnode):
        '''Processing a column'''
        # skip virtual columns
        if datatype == 'vrtcol':
            return

        # first comes the name
        self.sql_string += '  `' + name + '` '
        # then the datatype
        try:
            length = dtnode.length
        except AttributeError:
            length = None
        if length:
            self.sql_string += dtnode.sqltype + '(' + length + ') '
        else:
            self.sql_string += dtnode.sqltype + ' '
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
        if not nulls:
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
        ftable = ForeignKey.from_node(node)
        if ftable is not None:
            self.foreign_keys[name] = ftable

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
            fdata.table + \
            '(' + fdata.foreign_col + '),\n'


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# Default base class for Meta Tables.
META_TABLE_BASE = 'DbTable'

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
        # base class constructor
        super(QtDriver, self).__init__()


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

    if not tables is None and not tables.table is None:
        for table in tables.table:
            driver.table_start(table.name, table)

            columns = table.columns
            for column in columns.column:

                datatype_name = ''
                datatype = None
                for kkk in dir(column):
                    # This is a hack; it exists because the generated class
                    # does no provide any means to iterate child elements
                    # It relies on the assumption that all elements
                    # are custom types
                    if str(type(getattr(column, kkk))).find('class') > 0:
                        datatype = getattr(column, kkk)
                        datatype_name = kkk
                        break

                driver.column(
                    column.name,
                    string_choice(
                        column.label,
                        column.name,
                        column.label),
                    datatype_name,
                    str2bool(column.allowNulls),
                    column, datatype)

            driver.table_end(table.name, table)

    if not views is None and not views.view is None:
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
