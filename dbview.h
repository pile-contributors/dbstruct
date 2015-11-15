/**
 * @file dbview.h
 * @brief Declarations for DbView class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBVIEW_H_INCLUDE
#define GUARD_DBVIEW_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/dbtaew.h>

//! A view in a database.
class DBSTRUCT_EXPORT DbView : public DbTaew {

public:

    //! Default constructor.
    DbView ();

    //! Destructor.
    virtual ~DbView();

    //! The type of this object.
    virtual Type
    type () const {
        return DBO_SUBSET;
    }

protected:

private:
};

#endif // GUARD_DBVIEW_H_INCLUDE
