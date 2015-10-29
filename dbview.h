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
#include <dbstruct/dbobject.h>
#include <dbstruct/dbobject.h>

//! A view in a database.
class DBSTRUCT_EXPORT DbView : public DbObject {

public:

    //! Default constructor.
    DbView ();

    //! Destructor.
    virtual ~DbView();

protected:

private:
};

#endif // GUARD_DBVIEW_H_INCLUDE
