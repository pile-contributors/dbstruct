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
 * Represents a table (CREATE TABLE) inside the backend.
 * This is mostly syntactic sugar as the bulk of the interface is provided
 * by DbTaew class.
 */

/* ------------------------------------------------------------------------- */
/**
 * The constructor does nothing in this implementation.
 */
DbTable::DbTable()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * The destructor does nothing in this implementation.
 */
DbTable::~DbTable()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */
