/**
 * @file dbcolumn.cc
 * @brief Definitions for DbColumn class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbcolumndata.h"
#include "../dbstruct-private.h"


/**
 * @class DbColumnData
 *
 * The class is implicitly shared and represents the
 * base class for other - more specialized - column types.
 * It is the default object type that is created along with default
 * DbColumn instances.
 *
 */

DbColumnData::DbColumnData () :
    QSharedData (),
    col_name_(),
    col_label_(),
    col_id_(),
    real_col_id_(),
    length_(),
    datatype_(),
    allow_nulls_(true)
{
}

DbColumnData::DbColumnData (
        const QString &col_name, const QString &col_label,
        int col_id, int real_col_id, int length,
        DataType datatype, bool allow_nulls) :
    QSharedData (),
    col_name_(col_name),
    col_label_(col_label),
    col_id_(col_id),
    real_col_id_(real_col_id),
    length_(length),
    datatype_(datatype),
    allow_nulls_(allow_nulls)
{
}

DbColumnData::DbColumnData(const DbColumnData &other) :
    QSharedData(other),
    col_name_(other.col_name_),
    col_label_(other.col_label_),
    col_id_(other.col_id_),
    real_col_id_(other.real_col_id_),
    length_(other.length_),
    datatype_(other.datatype_),
    allow_nulls_(other.allow_nulls_)
{
}



