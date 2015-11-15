/**
 * @file dbstruct.h
 * @brief Declarations for DbStruct class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBSTRUCT_H_INCLUDE
#define GUARD_DBSTRUCT_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/dbobject.h>
#include <dbstruct/dbtable.h>
#include <dbstruct/dbview.h>

#include <vector>

//! The structure of a database.
class DBSTRUCT_EXPORT DbStruct : public DbObject {

public:

    //! Default constructor.
    DbStruct ();

    //! Destructor.
    virtual ~DbStruct();

    //! The type of this object.
    virtual Type
    type () const {
        return DBO_STRUCT;
    }

protected:

private:
};

#endif // GUARD_DBSTRUCT_H_INCLUDE
