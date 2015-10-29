/**
 * @file dbcolumn.h
 * @brief Declarations for DbColumn class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBCOLUMN_H_INCLUDE
#define GUARD_DBCOLUMN_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/dbobject.h>

//! The columnure of a database.
class DBSTRUCT_EXPORT DbColumn : public DbObject {

public:

    //! Default constructor.
    DbColumn ();

    //! Destructor.
    virtual ~DbColumn();

protected:

private:

};

#endif // GUARD_DBCOLUMN_H_INCLUDE
