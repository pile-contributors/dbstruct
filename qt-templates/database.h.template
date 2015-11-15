/* ========================================================================= */
/* ------------------------------------------------------------------------- */
/*!
  \file %(database)s.h
  \date %(Month)s %(Year)s
  \author %(Author)s

  \brief Auto-generated data class for %(Database)s table.


*//*

 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Please read COPYING and README files in root folder
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
/* ------------------------------------------------------------------------- */
/* ========================================================================= */
#ifndef __%(NAMESPACE)s_DB_%(DATABASE)s_DATABASE_INC__
#define __%(NAMESPACE)s_DB_%(DATABASE)s_DATABASE_INC__
//
//
//
//
/*  INCLUDES    ------------------------------------------------------------ */

#include "all-meta-tables.h"

#include <QString>
#include <QLatin1String>

/*  INCLUDES    ============================================================ */
//
//
//
//
/*  DEFINITIONS    --------------------------------------------------------- */

/*  DEFINITIONS    ========================================================= */
//
//
//
//
/*  CLASS    --------------------------------------------------------------- */

namespace %(namespace)s {

//! Describes the structure of the %(Database)s database .
///
class %(EXPORT)s %(Database)s : public %(BaseClass)s {
    //
    //
    //
    //
    /*  DEFINITIONS    ----------------------------------------------------- */

public:

    //! Unique numeric identifiers for tables and views
    enum DbCompId {
        DBC_INVALID = -1,

%(DBC_IDS)s
        DBC_MAX /**< number of objects in this database */
    };

    //! Unique numeric identifiers for tables
    enum DbTableId {
        DBT_INVALID = -1,

%(DB_TABLE_IDS)s
        DBT_MAX /**< number of tables in this database */
    };

    //! Unique numeric identifiers for views
    enum DbViewId {
        DBV_INVALID = -1,

%(DB_VIEW_IDS)s
        DBV_MAX /**< number of views in this database */
    };


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

    //! The name of this database.
    static QString databaseName () { return QLatin1String("%(Database)s"); }

    //! Get the name of the table or view based on its identifier.
    static QString componentName (DbCompId index) {
        switch(index) {

%(DB_COMPONENTS_NAME_CASE)s
            default:
                return QString();
        }
    }

    //! Get the id based on a table or view name.
    static DbCompId idFromName (const QString & value) {

%(DB_COMPONENTS_NAME_TO_ID)s
        return DBC_INVALID;
    }



    /*  --  T A B L E S  --  */


    //! Convert between component identifier and table identifier.
    static DbTableId comp2table (DbCompId value) {
        DbTableId result = (DbTableId)(value);
        if (result >= DBT_MAX) result = DBT_INVALID;
        return result;
    }

    //! Convert between table identifier and component identifier.
    static DbCompId table2comp (DbTableId value) {
        return (DbCompId)value;
    }

    //! Get the id based on a table name.
    static DbTableId tableIdFromName (const QString & value) {
        return comp2table (idFromName (value));
    }

%(DB_TABLES_CONSTR)s

    //! Get the name of the table based on its identifier.
    static QString tableName (DbTableId index) {
        switch(index) {

%(DB_TABLES_NAME_CASE)s
        default:
            return QString();
        }
    }


    /*  --  V I E W S  --  */


    //! Convert between component identifier and view identifier.
    static DbViewId comp2view (DbCompId value) {
        DbViewId result = (DbViewId)(value - DBT_MAX);
        if ((result <= DBV_INVALID) || (result >= DBV_MAX))
            result = DBV_INVALID;
        return result;
    }

    //! Convert between view identifier and component identifier.
    static DbCompId view2comp (DbViewId value) {
        return (DbCompId)(value + DBT_MAX);
    }

    //! Get the id based on a view name.
    static DbViewId viewIdFromName (const QString & value) {
        return comp2view (idFromName (value));
    }

%(DB_VIEWS_CONSTR)s

    //! Get the name of the view based on its identifier.
    static QString viewName (DbViewId index) {
        switch(index) {

%(DB_VIEWS_NAME_CASE)s
        default:
            return QString();
        }
    }


    /*  FUNCTIONS    ======================================================= */
    //
    //
    //
    //

}; /* class %(Database)s */

/*  CLASS    =============================================================== */
//
//
//
//

} // namespace %(namespace)s

#endif // __%(NAMESPACE)s_DB_%(DATABASE)s_DATABASE_INC__
/* ------------------------------------------------------------------------- */
/* ========================================================================= */
