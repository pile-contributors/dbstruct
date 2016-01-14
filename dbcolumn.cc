/**
 * @file dbcolumn.cc
 * @brief Definitions for DbColumn class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbcolumn.h"
#include "dbstruct-private.h"

#include <QVariant>
#include <QCoreApplication>

#include "columns/dbcolumndata.h"
/**
 * @class DbColumn
 *
 * The class is implemented using
 * <a href="http://doc.qt.io/qt-5/qshareddatapointer.html">QSharedDataPointer</a>
 * and <a href="http://doc.qt.io/qt-5/qshareddata.html">QSharedData</a> which
 * combines the speed and memory efficiency of pointers with the ease of use
 * of classes.
 *
 * Internal DbColumnData is implicitly shared and may take one of
 * a number of forms depending on the data-type.
 * Any DbColumn instance will always have a valid DbColumnData
 * attached to it.
 *
 * The library supports virtual columns (see isVirtual())
 * that have no corespondent in the
 * database table and, for this reason, the columns have two indexes:
 * the common one - columnId() - that takes into consideration all columns
 * (real and virtual) and the "real" index - columnRealId()- that only takes
 * into consideration actual columns in the underlying database table.
 */

DbColumn::DbColumn () :
    DbObject(),
    d (new DbColumnData ())
{
}

DbColumn::DbColumn (
        const QString &col_name, DbDataType::Dty datatype,
        int col_id, const QString &col_label,
        int real_col_id, int length, bool allow_nulls,
        bool readonly):
    DbObject(),
    d (new DbColumnData (
           col_name,
           col_label.isEmpty() ? col_name : col_label,
           col_id,
           real_col_id == -1 ? col_id : real_col_id,
           length, datatype, allow_nulls, readonly))
{
}

bool DbColumn::isVirtual() const
{
    return d->isVirtual ();
}

const QString &DbColumn::columnName() const
{
    return d->col_name_;
}

const QString &DbColumn::columnLabel() const
{
    return d->col_label_;
}

int DbColumn::columnId() const
{
    return d->col_id_;
}

int DbColumn::columnRealId() const
{
    return d->real_col_id_;
}

int DbColumn::columnLength() const
{
    return d->length_;
}

DbDataType::Dty DbColumn::columnType() const
{
    return d->datatype_;
}

bool DbColumn::allowNulls() const
{
    return d->allow_nulls_;
}

bool DbColumn::readOnly() const
{
    return d->readonly_;
}

void DbColumn::setAllowNulls (bool value)
{
    d->allow_nulls_ = value;
}

void DbColumn::setReadOnly (bool value)
{
    d->readonly_ = value;
}

DbColumn DbColumn::col (
        const QString &col_name, DbDataType::Dty datatype,
        int col_id, const QString &col_label,
        int real_col_id, int length, bool allow_nulls,
        bool readonly)
{
    return DbColumn (
                col_name, datatype,
                col_id, col_label,
                real_col_id, length, allow_nulls, readonly);
}


