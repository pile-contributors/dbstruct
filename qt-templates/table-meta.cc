/* ========================================================================= */
/* ------------------------------------------------------------------------- */
/*!
  \file %(table)s-meta.cc
  \date %(Month)s %(Year)s
  \author %(Author)s

  \brief Auto-generated model for %(Table)s table.


*//*

 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Please read COPYING and README files in root folder
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
/* ------------------------------------------------------------------------- */
/* ========================================================================= */
//
//
//
//
/*  INCLUDES    ------------------------------------------------------------ */

#include "%(table)s-meta.h"

#include <QSql>
#include <QSqlQuery>
#include <QSqlRecord>
#include <QSqlError>
#include <QSqlDatabase>
#include <QVariant>

/*  INCLUDES    ============================================================ */
//
//
//
//
/*  DEFINITIONS    --------------------------------------------------------- */

using namespace %(namespace)s::%(database)s;
using namespace %(namespace)s::%(database)s::meta;

/*  DEFINITIONS    ========================================================= */
//
//
//
//
/*  CLASS    --------------------------------------------------------------- */

/* ------------------------------------------------------------------------- */
QStringList %(Table)s::columnsString()
{
    QStringList result;
    result
%(PIPE_COLUMNS)s
    ;
    return result;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
QString %(Table)s::columnString (int i)
{
    QString result;
    switch (i) {
%(CASE_COLUMNS)s
    default: result = QLatin1String("out_of_bounds"); break;
    }
    return result;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
long %(Table)s::rowsInTable (QSqlDatabase & db)
{
    int rows = -1;
    QSqlQuery query(QLatin1String("SELECT COUNT(*) FROM %(Table)s;\n"), db);
    if (query.exec() && query.next()) {
        bool b_ok = false;
        rows = query.value(0).toLongLong (&b_ok);
        if (!b_ok) {
            rows = -1;
        }
    } else {
        // DB_%(TABLE)s_DBG("Failed to retrieve number of rows");
        // DB_%(TABLE)s_DBG(TMP_A(query.lastError().text()));
    }
    return rows;
}
/* ========================================================================= */

/*  CLASS    =============================================================== */
//
//
//
//

/* ------------------------------------------------------------------------- */
/* ========================================================================= */