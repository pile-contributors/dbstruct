/* ========================================================================= */
/* ------------------------------------------------------------------------- */
/*!
  \file %(table)s.h
  \date %(Month)s %(Year)s
  \author %(Author)s

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

%(IMPORTH)s
#include "%(table)s-meta.h"
#include <dbstruct/dbrecord.h>

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

//! Mirrors %(Table)s database table.
///
class %(EXPORT)s %(Table)s : public meta::%(Table)s, public %(RecordBaseClass)s {
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

    //! constructor
    explicit %(Table)s() : meta::%(Table)s(), %(RecordBaseClass)s(),
%(DefaultConstructor)s
    {}

    //! destructor
    virtual ~%(Table)s () {}

    //! copy constructor
    %(Table)s (const %(Table)s & other) :
%(CopyConstructor)s
    {}

    //! assignment operator
    %(Table)s& operator= (const %(Table)s& other) {
%(AssignConstructor)s
        return *this;
    }

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

    //! Set the index to given value (if the model has an id column).
    virtual void
    setId (
            long value) {
        %(SET_ID_RESULT)s;
    }

    //! Get the index of this instance (if the model has an id column).
    virtual long
    getId () const {
        return %(GET_ID_RESULT)s;
    }

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
