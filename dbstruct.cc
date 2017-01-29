/**
 * @file dbstruct.cc
 * @brief Definitions for DbStruct class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbstruct.h"
#include "dbstruct-private.h"

/**
 * @class DbStructMeta
 *
 * This class groups information about the structure of a database.
 *
 * The class defines an interface that describes the sub-structures of the
 * database like tables and views (reffered to as taew).
 *
 * To identify internal components two addressing methods are used: a numeric
 * one and a text-based one (table/view name).
 *
 * Each table has a zero-based table index. Each view has a
 * zero-based view index. A common component index is also provided
 * and comp2table(), table2comp (), comp2view() and view2comp()
 * can be used to convert between them.
 *
 * Converting between text-based method and index based method is done using
 * tableIdFromName(), tableName(), viewIdFromName(), viewName().
 */

/* ------------------------------------------------------------------------- */
/**
 * The constructor does nothing in this implementation.
 */
DbStructMeta::DbStructMeta()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * The destructor does nothing in this implementation.
 */
DbStructMeta::~DbStructMeta()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/**
 * @class DbStruct
 *
 * This is the structure that holds an actual connection to a database
 * described by a DbStructMeta. It hosts a Qt-based connection and requires
 * the implementation to be able to export a DbStructMeta using its
 * metaDatabase() method.
 *
 * The database metadata is isolated outside this class so that its use is
 * lightweight. A simple implementation that provides both metadata and
 * the connection looks like this:
 *
 * @code
 * class MyDb : public MyDbMeta, public DbStruct {
 * public:
 *     DbStructMeta * metaDatabase () {
 *         return static_cast<DbStructMeta*>(this);
 *     }
 * };
 * @endcode
 *
 * And this is basically what META_DATA_BASE macro does.
 */

