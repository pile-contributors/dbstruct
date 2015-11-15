/* ========================================================================= */
/* ------------------------------------------------------------------------- */
/*!
  \file %(table)s-meta.h
  \date %(Month)s %(Year)s
  \author %(Author)s

  \brief Auto-generated meta-data class for %(Table)s view.


*//*

 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Please read COPYING and README files in root folder
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
/* ------------------------------------------------------------------------- */
/* ========================================================================= */
#ifndef __%(NAMESPACE)s_DB_%(DATABASE)s_VIEW_%(TABLE)s_META_INC__
#define __%(NAMESPACE)s_DB_%(DATABASE)s_VIEW_%(TABLE)s_META_INC__
//
//
//
//
/*  INCLUDES    ------------------------------------------------------------ */

#include <dbstruct/dbcolumn.h>
%(MetaClassInclude)s

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
namespace %(database)s {
namespace meta {

//! Mirrors $TABLE_NAME_U$ database table.
///
class %(EXPORT)s %(Table)s : public %(BaseClass)s {
    //
    //
    //
    //
    /*  DEFINITIONS    ----------------------------------------------------- */

public:


    enum ColId {
        COLID_INVALID = -1, /**< invalid column indicator */

%(COLUMN_IDS)s
        COLID_MAX /**< number of columns in this table */
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

    //! The name of this table as a string.
    virtual QString
    tableName() const {
        return tableString();
    }

    //! The name of a column given an index.
    virtual QString
    columnName(
        int i) const {

        return columnString (i);
    }

    //! Number of columns in this table.
    virtual int
    columnCount() const {
        return COLID_MAX;
    }

    //! The name of the columns as a list of strings.
    virtual QStringList
    columns() const {
        return columnsString ();
    }

    //! The index of the id column or ID_UNAVAILABLE if no id column.
    virtual int
    idColumn () const {
        return idColumnIndex ();
    }

    //! All columns as a comma-separated list.
    virtual QString
    commaColumns () const {
        return commaColumnsString ();
    }

    //! All columns as a comma-separated list except the id.
    virtual QString
    commaColumnsNoId () const {
        return commaColumnsNoIdString ();
    }

    //! All columns as a comma-separated list and :columns.
    virtual QString
    columnColumns () const {
        return columnColumnsString ();
    }

    //! All columns as a comma-separated list of column=:column.
    virtual QString
    assignColumns () const {
        return assignColumnsString ();
    }


%(TableColumnConstr)s



    //! The name of this table as a string.
    static inline QString
    tableString() {
        return QLatin1String("%(Table)s");
    }

    //! The name of a column given an index.
    static QString
    columnString (
        int i);

    //! Number of columns in this table.
    static inline int
    columnSize() {
        return COLID_MAX;
    }

    //! The name of the columns.
    static QStringList
    columnsString () ;

    //! The index of the id column or ID_UNAVAILABLE if no id column.
    static inline int
    idColumnIndex () {
        return %(ID_COLUMN)s;
    }

    //! All columns as a comma-separated list.
    static QString
    commaColumnsString () {
        return QLatin1String(
%(COMMA_COLUMNS)s);
    }

    //! Number of rows in this table.
    static long
    rowsInTable (
            QSqlDatabase & db);

    //! All columns as a comma-separated list except the id.
    static QString
    commaColumnsNoIdString () {
        return QLatin1String(
%(COMMA_COLUMNS_NO_ID)s);
    }

    //! All columns as a comma-separated list and :columns.
    static QString
    columnColumnsString () {
        return QLatin1String(
%(COLUMN_COLUMNS)s);
    }

    //! All columns as a comma-separated list of column=:column.
    static QString
    assignColumnsString () {
        return QLatin1String(
%(ASSIGN_COLUMNS)s);
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

} // namespace meta
} // namespace %(database)s
} // namespace %(namespace)s

#endif // __%(NAMESPACE)s_DB_%(DATABASE)s_VIEW_%(TABLE)s_META_INC__
/* ------------------------------------------------------------------------- */
/* ========================================================================= */
