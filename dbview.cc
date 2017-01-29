/**
 * @file dbview.cc
 * @brief Definitions for DbView class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbview.h"
#include "dbstruct-private.h"

/**
 * @class DbView
 *
 * Represents a view (CREATE VIEW) inside the backend.
 * This is mostly syntactic sugar as the bulk of the interface is provided
 * by DbTaew class.
 */

/* ------------------------------------------------------------------------- */
/**
 * The constructor does nothing in this implementation.
 */
DbView::DbView()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * The destructor does nothing in this implementation.
 */
DbView::~DbView()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */
