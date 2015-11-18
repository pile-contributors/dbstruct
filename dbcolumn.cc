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

/**
 * @class DbColumn
 *
 * Detailed description.
 */

/* ------------------------------------------------------------------------- */
/**
 * Detailed description for concolumnor.
 */
DbColumn::DbColumn() : DbObject(),
    col_name_(),
    col_id_(-1),
    length_(-1),
    col_label_(),
    datatype_(),
    nulls_(false),
    autoincrement_(false),
    default_value_(),
    read_only_(),
    foreign_table_(),
    foreign_key_(),
    foreign_ref_()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * Detailed description for decolumnor.
 */
DbColumn::~DbColumn()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */
