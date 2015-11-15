/**
 * @file dbrecord.h
 * @brief Declarations for DbRecord class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBRECORD_H_INCLUDE
#define GUARD_DBRECORD_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/dbobject.h>
#include <dbstruct/dbcolumn.h>
#include <assert.h>

class QSqlDatabase;
class QSqlQuery;
class QSqlRecord;
class DbTable;

//! A record in a database.
class DBSTRUCT_EXPORT DbRecord  {

public:

    //! Default constructor.
    DbRecord ();

    //! Destructor.
    virtual ~DbRecord();

    //! The type of this object.
    virtual DbObject::Type
    type () const {
        return DbObject::DBO_RECORD;
    }

    //! Initialize this instance from a given id.
    bool
    initFromId (
            DbTable * table,
            QSqlDatabase & db,
            long db_id);

    //! Initialize this instance from a given field
    bool
    initFrom (
            DbTable * table,
            QSqlDatabase & db,
            int column);

    //! Saves the instance to the database.
    virtual bool
    save (
            DbTable * table,
            QSqlDatabase & db);

    //! Remove this entry from the database.
    bool
    remFromDb (
            DbTable * table,
            QSqlDatabase &db,
            int column);

    //! Tell if this instance is a new one or it has a database correspondent.
    virtual bool
    isNew () const {
        return getId() < 0;
    }

    //! Bind a single value identified by column index in a query.
    virtual void
    bindOne (
            QSqlQuery & query,
            int i) const = 0;

    //! Bind values to names in a query.
    virtual void
    bind (
        QSqlQuery & query) const = 0;

    //! Get values from a query.
    virtual bool
    retreive (
        const QSqlQuery & query) = 0;

    //! Get values from a record.
    virtual bool
    retreive (
        const QSqlRecord & rec) = 0;

    //! Set the index to given value (if the model has an id column).
    virtual void
    setId (
            long /*value*/) {
        // by default do nothing
    }

    //! Get the index of this instance (if the model has an id column).
    virtual long
    getId () const;


protected:

private:
};

#endif // GUARD_DBRECORD_H_INCLUDE
