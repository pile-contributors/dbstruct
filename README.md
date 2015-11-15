DbStruct
========

This pile contains classes that can be used to
describe the structure of a database.

The idea derives from a [CodeProject article](http://www.codeproject.com/Articles/76814/Generate-SQL-Database-Schema-from-XML-Part-File)
that features a way to *Generate SQL Database Schema from XML*.

The code that is capable to generate an in-memory
representation using structures defined by this pile
from various sources is grouped in another pile: []().

The code that exports the structure to various other formats
is grouped in yet another pile: []().


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


Default Templates
-----------------

A set of default templates are provided in `qt-templates`
directory. Please note that `lupdate.exe` will crash
if it encounters a .h or .cc file that has variables in it.
This is why the template files all have the `.template` 
extension. The name of the template files are hard-coded into 
`pileschema.py` but that may change in the future.

