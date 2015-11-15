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

//! The objecture of a database.
class DBSTRUCT_EXPORT DbObject {

public:

    //! Default constructor.
    DbObject ();

    //! Destructor.
    virtual ~DbObject();

protected:

private:

};

#endif // GUARD_DBOBJECT_H_INCLUDE
