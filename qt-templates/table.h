/* ========================================================================= */
/* ------------------------------------------------------------------------- */
/*!
  \file %(table)s.h
  \date Oct 2015
  \author TNick

  \brief Auto-generated data class for %(Table)s table.


*//*

 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Please read COPYING and README files in root folder
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
/* ------------------------------------------------------------------------- */
/* ========================================================================= */
#ifndef __%(NAMESPACE)s_DB_%(DATABASE)s_TABLE_%(TABLE)s_INC__
#define __%(NAMESPACE)s_DB_%(DATABASE)s_TABLE_%(TABLE)s_INC__
//
//
//
//
/*  INCLUDES    ------------------------------------------------------------ */

#include "all-meta-tables.h"

/*  INCLUDES    ============================================================ */
//
//
//
//
/*  DEFINITIONS    --------------------------------------------------------- */

class QSqlQuery;
class QSqlRecord;

/*  DEFINITIONS    ========================================================= */
//
//
//
//
/*  CLASS    --------------------------------------------------------------- */

namespace %(namespace)s {
namespace %(database)s {

//! Mirrors $TABLE_NAME_U$ database table.
///
class %(EXPORT)s %(Table)s : public meta::%(Table)s {
    //
    //
    //
    //
    /*  DEFINITIONS    ----------------------------------------------------- */

public:

%(TableDataMembers)s

    /*  DEFINITIONS    ===================================================== */
    //
    //
    //
    //
    /*  DATA    ------------------------------------------------------------ */

public:


    /*  DATA    ============================================================ */
    //
    //
    //
    //
    /*  FUNCTIONS    ------------------------------------------------------- */

public:

    //! Bind a single value identified by column index in a query.
    virtual void
    bindOne (
            QSqlQuery & query,
            int i) const;

    //! Bind values to names in a query.
    virtual void
    bind (
        QSqlQuery & query) const;

    //! Get values from a query.
    virtual bool
    retreive (
        const QSqlQuery & query);

    //! Get values from a record.
    virtual bool
    retreive (
        const QSqlRecord & rec);

    /*  FUNCTIONS    ======================================================= */
    //
    //
    //
    //

}; /* class %(Table)s */

/*  CLASS    =============================================================== */
//
//
//
//

} // namespace %(database)s
} // namespace %(namespace)s

#endif // __%(NAMESPACE)s_DB_%(DATABASE)s_TABLE_%(TABLE)s_INC__
/* ------------------------------------------------------------------------- */
/* ========================================================================= */
