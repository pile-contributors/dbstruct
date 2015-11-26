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
 * Detailed description.
 */

/* ------------------------------------------------------------------------- */
/**
 * Detailed description for contaewor.
 */
DbTaew::DbTaew()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * Detailed description for detaewor.
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
    if (partial == -1)
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
