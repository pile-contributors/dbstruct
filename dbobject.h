/**
 * @file dbobject.h
 * @brief Declarations for DbObject class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBOBJECT_H_INCLUDE
#define GUARD_DBOBJECT_H_INCLUDE

#include <dbstruct/dbstruct-config.h>

#include <QString>
#include <QStringList>
#include <QDate>
#include <QTime>
#include <QDateTime>

class DbStructMeta;
class DbColumn;
class DbRecord;
class DbTable;
class DbView;

//! The objecture of a database.
class DBSTRUCT_EXPORT DbObject {

public:

    //! The types of objects that use this class as a base.
    enum Type {
        DBO_INVALID = -1,

        DBO_STRUCT, /**< a DbStruct instance */
        DBO_COLUMN, /**< a DbColumn instance */
        DBO_RECORD, /**< a DbRecord instance */
        DBO_TABLE, /**< a DbTable instance */
        DBO_SUBSET, /**< a DbView instance that exposes all columns of a table */
        DBO_CPLX_VIEW, /**< a DbView that draws information from multiple tables */
        DBO_CUSTOM, /**< User-defined (none of the above) */

        DBO_MAX /**< number of valid types*/
    };

    //! Default constructor.
    DbObject ();

    //! Destructor.
    virtual ~DbObject();

    //! The type of this object.
    virtual Type
    type () const {
        return DBO_CUSTOM;
    }

    //! Get this instance as a DbStruct.
    DbStructMeta * asStruct ();

    //! Get this instance as a DbColumn.
    DbColumn * asColumn ();

    //! Get this instance as a DbRecord.
    DbRecord * asRecord ();

    //! Get this instance as a DbTable.
    DbTable * asTable ();

    //! Get this instance as a DbView.
    DbView * asView ();

    //! Tell if this instance is a DbStruct.
    inline bool isStruct () {
        return type() == DBO_STRUCT;
    }

    //! Tell if this instance is a DbColumn.
    inline bool isColumn () {
        return type() == DBO_COLUMN;
    }

    //! Tell if this instance is a DbRecord.
    inline bool isRecord () {
        return type() == DBO_RECORD;
    }

    //! Tell if this instance is a DbTable.
    inline bool isTable () {
        return type() == DBO_TABLE;
    }

    //! Tell if this instance is a DbView.
    inline bool isView () {
        return (type() == DBO_SUBSET) || (type() == DBO_CPLX_VIEW);
    }

    //! Tell if this instance is a custom one.
    inline bool isCustom () {
        return type() == DBO_CUSTOM;
    }

public:

    //! Create an MD5 hash for input string.
    static QString
    md5Hash (
            const QString &input);

};

#endif // GUARD_DBOBJECT_H_INCLUDE
