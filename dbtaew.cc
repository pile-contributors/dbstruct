/**
 * @file dbtaew.cc
 * @brief Definitions for DbTaew class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbtaew.h"
#include "dbstruct-private.h"

#include <QObject>
#include <QSqlTableModel>

/**
 * @class DbTaew
 *
 * Tables and views share a lot of their characteristics which are grouped in
 * this class.
 *
 * Internal columns are represented using a dual system (unique integers
 * and text strings). Giveen that a table might have virtual
 * columns we distinguish between regular columnIndex() and
 * realColumnIndex(), with the real index being always smaller or equal
 * with the regular column index. Use toRealIndex() and
 * fromRealIndex() to convert between the two.
 *
 * The implementation is expected to provide the name of this table
 * and the name of the table where changes should be written to (for
 * example in case of a view that extracts its content from a table).
 *
 * The implementation should also provide the name of the column
 * (for database backend) and the label (for the user). It will
 * create a DbColumn using columnCtor().
 */

/* ------------------------------------------------------------------------- */
/**
 * The constructor does nothing in this implementation.
 */
DbTaew::DbTaew()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * The destructor does nothing in this implementation.
 */
DbTaew::~DbTaew()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
bool DbTaew::hasColumn (const QString &s_name) const
{
    return columns().contains (s_name, Qt::CaseInsensitive);
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
int DbTaew::columnIndex (const QString &s_name) const
{
    return columns().indexOf (s_name, Qt::CaseInsensitive);
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
int DbTaew::realColumnIndex (const QString &s_name) const
{
    int partial = columnIndex (s_name);
    if (partial == dbstruct::UNDEFINED)
        return partial;
    return toRealIndex (partial);
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
QSqlTableModel * DbTaew::sqlModel (
        QSqlDatabase & database, QObject * parent) const
{
    DBSTRUCT_TRACE_ENTRY;
    QSqlTableModel * model = new QSqlTableModel (
                parent, database);
    model->setTable (tableName ());

    /** @todo other constraints ? */

    model->select ();

    return model;
}
/* ========================================================================= */
