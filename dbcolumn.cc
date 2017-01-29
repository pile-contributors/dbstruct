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
 *
 * To construct a simple column all one needs to provide to the constructor
 * is the name of the column, the type of data it carries and
 * the index in the table. The label is assumed to be the same as the name,
 * the real id is assumed to match the virtual id, values are not read-only
 * and NULLs are allowed.
 *
 * @code
 * DbColumn testee ("id", DbDataType::DTY_INTEGER, 0);
 * @endcode
 */


/* ------------------------------------------------------------------------- */
/**
 * Default constructor creates an invalid instance
 * (columnType() evaluates to DbDataType::DTY_INVALID)
 * with no name.
 */
DbColumn::DbColumn () :
    DbObject(),
    d (new DbColumnData ())
{
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * To construct a simple column all one needs to provide to the constructor
 * is the name of the column, the type of data it carries and
 * the index in the table. In this case the label is assumed
 * to be the same as the name, the real id is assumed
 * to match the virtual id, values are not read-only
 * NULLs are allowed and the length is undefined (dbstruct::UNDEFINED).
 *
 * @param col_name Name of the column in underlying table.
 * @param datatype Kind of data in this column.
 * @param col_id Index of the column in table.
 * @param col_label User-visible name for the column; by default this is the
 *        same as the name of the column.
 * @param real_col_id Index of the column among "real" columns (dbstruct::UNDEFINED or -1 for
 *        virtual); by default the real column id is assumed to be the same as
 *        general column id.
 * @param length Size of the field in the database (-1, the default, means undefined).
 * @param allow_nulls Tells if underlying table accepts NULLs for this column
 *        (by default this is true).
 * @param readonly Is the user allowed to change the values in this column
 *        (default) or not.
 */
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
           real_col_id == dbstruct::DEFAULT ? col_id : real_col_id,
           length, datatype, allow_nulls, readonly))
{
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbColumn::DbColumn(const DbColumn &other) :
    DbObject (other),
    d (other.d)
{}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbColumn &DbColumn::operator=(const DbColumn &other)
{
    d = other.d;
    return *this;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbColumn::~DbColumn()
{
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
bool DbColumn::isVirtual() const
{
    return d->isVirtual ();
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
const QString &DbColumn::columnName() const
{
    return d->col_name_;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
const QString &DbColumn::columnLabel() const
{
    return d->col_label_;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
int DbColumn::columnId() const
{
    return d->col_id_;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
int DbColumn::columnRealId() const
{
    return d->real_col_id_;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
int DbColumn::columnLength() const
{
    return d->length_;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbDataType::Dty DbColumn::columnType() const
{
    return d->datatype_;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
bool DbColumn::allowNulls() const
{
    return d->allow_nulls_;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
bool DbColumn::readOnly() const
{
    return d->readonly_;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * The name of a column is the name used to identify that column
 * in an actual database table, for example, but its use is not
 * limited to that. It provides a textual name for the column
 * that transcedes language changes in user interface, for example.
 * The label, on the other hand, is expected to change based on
 * the language choosen by the user.
 *
 * The label is set by this method to the same value if it is empty.
 *
 * @param value New name for the column
 * @see setColumnLabel(), columnLabel(), columnName()
 */
void DbColumn::setColumnName(const QString &value)
{
    d->col_name_ = value;
    if (d->col_label_.isEmpty()) {
        d->col_label_= value;
    }
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * Setting a label does not change the name of the column in any case.
 *
 * @param value New label for the column
 * @see setColumnName(), columnLabel(), columnName()
 */
void DbColumn::setColumnLabel (const QString &value)
{
    d->col_label_= value;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * We distinguish between indexes in the "general", "complete" table
 * and indexes in "real" table inside the database because our tables may
 * contain virtual columns that draw their values in some other way than
 * requesting them from the database.
 *
 * This method seths the index of this column inside "complete"
 * table while setColumnRealId() sets the index inside the database table.
 * Setting one does not change the other in any case.
 *
 * @param value New value for column id in general table
 * @see setColumnRealId(), columnId(), columnRealId()
 */
void DbColumn::setColumnId (int value)
{
    d->col_id_= value;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * We distinguish between indexes in the "general", "complete" table
 * and indexes in "real" table inside the database because our tables may
 * contain virtual columns that draw their values in some other way than
 * requesting them from the database.
 *
 * This method seths the index of this column inside the database table
 * table while setColumnId() sets the index inside "complete" table.
 * Setting one does not change the other in any case.
 *
 * @param value New value for column id in "real" table
 * @see setColumnId(), columnId(), columnRealId()
 */
void DbColumn::setColumnRealId(int value)
{
    d->real_col_id_= value;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * This tells if the underlying column in a real table allows
 * NULL (or ommiting the value for this column).
 * @param value true or false
 * @see allowNulls()
 */
void DbColumn::setAllowNulls (bool value)
{
    d->allow_nulls_ = value;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * One example use case is an id column that is auto-incremented by
 * the database.
 *
 * @param value true (column is read-only) or false (column is read-write)
 * @see readOnly()
 */
void DbColumn::setReadOnly (bool value)
{
    d->readonly_ = value;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
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
/* ========================================================================= */


