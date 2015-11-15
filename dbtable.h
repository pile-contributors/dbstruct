/**
 * @file dbtable.h
 * @brief Declarations for DbTable class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBTABLE_H_INCLUDE
#define GUARD_DBTABLE_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/DbTaew.h>
#include <dbstruct/dbcolumn.h>

class QSqlDatabase;
class QSqlQuery;
class QSqlRecord;

//! A table in a database.
class DBSTRUCT_EXPORT DbTable : public DbTaew {

public:

    //! Default constructor.
    DbTable ();

    //! Destructor.
    virtual ~DbTable();

    //! The type of this object.
    virtual Type
    type () const {
        return DBO_TABLE;
    }

protected:

private:
};

#endif // GUARD_DBTABLE_H_INCLUDE
