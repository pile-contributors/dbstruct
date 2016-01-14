DbStruct
========

Classes that can be used to describe the structure of a database.

Introduction
------------

The idea derives from a [CodeProject article](http://www.codeproject.com/Articles/76814/Generate-SQL-Database-Schema-from-XML-Part-File)
that features a way to *Generate SQL Database Schema from XML*.

Some basic classes are provided: DbColumn, DbTable, DbView,
DbRecord. They are all based on DbObject and DbStruct represents
a database.

Auto-generate
-------------

A Python script (`pileschema.py`) is provided that can generate
content based on an input .xml file. The structure of the .xml,
default options and explanations are part of `PileSchema.xsd`
schema file.

The script will accept a command and various options:
 - *validate*: check a .xml file against the constraints
 in `PileSchema.xsd`;
 - *sql*: generate a .sql file used to create the database
 structure;
 - *cpp*: generate C++ source files based on templates and
 input .xml file.

The script depends on `lxml`  that can be installed using `pip`.
An additional python module (`pile_schema_loader.py`) is generated
from `PileSchema.xsd` by
[generateDS](http://www.davekuhlman.org/generateDS.html)
and contains a Python parser for the file:

    python generateDS.py --no-questions -f -o pile_schema_loader.py PileSchema.xsd

This module is then used by `pileschema.py` to do its chores.

Default Templates
-----------------

A set of default templates are provided in `qt-templates`
directory. Please note that `lupdate.exe` will crash
if it encounters a .h or .cc file that has variables in it.
This is why the template files all have the `.template`
extension. The name of the template files are hard-coded into
`pileschema.py` but that may change in the future.


Column Types
------------

Columns may be actual database columns hosted by a table
(called "real" columns) or they may have a different way
of retreiving the data (called "virtual" columns).
