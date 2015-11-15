/**
 * @file dbtable.cc
 * @brief Definitions for DbTable class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbtable.h"
#include "dbstruct-private.h"

/**
 * @class DbTable
 *
 * Detailed description.
 */

/* ------------------------------------------------------------------------- */
/**
 * Detailed description for contableor.
 */
DbTable::DbTable()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * Detailed description for detableor.
 */
DbTable::~DbTable()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
bool DbTable::hasColumn (const QString &s_name) const
{
    return columns().contains (s_name, Qt::CaseInsensitive);
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
int DbTable::columnIndex (const QString &s_name) const
{
    return columns().indexOf (s_name, Qt::CaseInsensitive);
}
/* ========================================================================= */
