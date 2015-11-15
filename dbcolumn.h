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

#include <QString>

//! The columnure of a database.
class DBSTRUCT_EXPORT DbColumn : public DbObject {

public:

    QString col_name_;
    int col_id_;
    int length_;
    QString col_label_;
    QString datatype_;
    bool nulls_;
    bool autoincrement_;
    QString default_value_;

    //! Default constructor.
    DbColumn ();

    //! Default constructor.
    DbColumn (
            const QString & col_name,
            int col_id,
            int length,
            const QString & col_label,
            const QString & datatype,
            bool nulls,
            bool autoincrement,
            const QString & default_value) : DbObject(),
        col_name_(col_name),
        col_id_(col_id),
        length_(length),
        col_label_(col_label),
        datatype_(datatype),
        nulls_(nulls),
        autoincrement_(autoincrement),
        default_value_(default_value)
    {
    }


    //! Destructor.
    virtual ~DbColumn();

protected:

private:

};

#endif // GUARD_DBCOLUMN_H_INCLUDE
