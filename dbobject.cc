/**
 * @file dbobject.cc
 * @brief Definitions for DbObject class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbobject.h"
#include "dbstruct-private.h"

#include "dbstruct.h"
#include "dbcolumn.h"
#include "dbrecord.h"
#include "dbtable.h"
#include "dbview.h"

/**
 * @class DbObject
 *
 * Detailed description.
 */

/* ------------------------------------------------------------------------- */
/**
 * Detailed description for conobjector.
 */
DbObject::DbObject()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * Detailed description for deobjector.
 */
DbObject::~DbObject()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbStructMeta * DbObject::asStruct ()
{
    if (type () != DBO_STRUCT)
        return NULL;
    return static_cast<DbStructMeta*>(this);
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbColumn * DbObject::asColumn ()
{
    if (type () != DBO_COLUMN)
        return NULL;
    return static_cast<DbColumn*>(this);
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbRecord * DbObject::asRecord ()
{
    if (type () != DBO_RECORD)
        return NULL;
    // return static_cast<DbRecord*>(this);
    return NULL;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbTable * DbObject::asTable ()
{
    if (type () != DBO_TABLE)
        return NULL;
    return static_cast<DbTable*>(this);
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
DbView * DbObject::asView ()
{
    if ((type () == DBO_SUBSET) || (type () == DBO_CPLX_VIEW))
        return static_cast<DbView*>(this);
    return NULL;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
