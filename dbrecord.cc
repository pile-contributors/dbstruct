/**
 * @file dbrecord.cc
 * @brief Definitions for DbRecord class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbrecord.h"
#include "dbstruct-private.h"
#include "dbtable.h"

#include <QSqlQuery>
#include <QSqlError>
#include <QSqlDriver>
#include <QString>
#include <QVariant>
#include <QDebug>

#if 1
#   define DBREC_DEBUGM DBSTRUCT_DEBUGM
#else
#   define DBREC_DEBUGM black_hole
#endif

#if 0
#define DBREC_TRACE_ENTRY DBSTRUCT_TRACE_ENTRY
#else
#define DBREC_TRACE_ENTRY
#endif

#if 0
#define DBREC_TRACE_EXIT DBSTRUCT_TRACE_EXIT
#else
#define DBREC_TRACE_EXIT
#endif


/**
 * @class DbRecord
 *
 */

/* ------------------------------------------------------------------------- */
/**
 */
DbRecord::DbRecord()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 */
DbRecord::~DbRecord()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
bool DbRecord::initFromId (DbTaew * table, QSqlDatabase & db, long db_id)
{
    DBREC_TRACE_ENTRY;
    int id_column_index = table->idColumn ();
    if (id_column_index == -1) {
        qWarning () << "The model "<< table->tableName()
                    << "does not have an id column ";
        return false;
    }
    // set the id inside the instance
    long preserve_id = getId();
    DBG_ASSERT(preserve_id != DbTaew::ID_UNAVAILABLE);
    setId (db_id);
    // then ask specialized function to retrieve the values
    bool bret = initFrom (table, db, id_column_index);
    // in case of failure restore the state
    if (!bret) {
        setId (preserve_id);
    }
    DBREC_TRACE_EXIT;
    return bret;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * The value that corresponds to the column inside this instance should have
 * been initialized by the caller with the value to search for.
 *
 * @param column index of the column to use for initialization
 * @return true if the instance was initialized
 */
bool DbRecord::initFrom (DbTaew * table, QSqlDatabase & db, int column)
{
    DBREC_TRACE_ENTRY;
    bool b_ret = false;
    for (;;) {

        QSqlQuery query (db);
        QString s_col_name = table->columnName (column);
        QString statement =
                QString("SELECT %1 FROM %2 WHERE %3=:%4;\n")
                .arg(table->commaColumns ())
                .arg(table->tableName())
                .arg(s_col_name)
                .arg(s_col_name);
        DBREC_DEBUGM("%s\n", TMP_A(statement));
        if (!query.prepare(statement)) {
            qWarning () << "prepare failed: " << statement;
            qWarning () << query.lastError ().text ();
            DBG_ASSERT(false);
            break;
        }
        bindOne (query, column);
        if (!query.exec()) {
            qWarning () << "query failed: " << statement;
            qWarning () << query.lastError ().text ();
            break;
        }
        if (!query.next()) {
            DBREC_DEBUGM("Query succeed but no entry was found "
                         "in the database (%s)\n",
                         TMP_A(query.lastError().text()));
            return false;
        }

        // get the values to their variables
        /*b_ret = */retrieve (query, db);
        b_ret = true;

        int additional_result = 0;
        while (query.next()) {
            ++additional_result;
        }
        if (additional_result > 0) {
            DBREC_DEBUGM("WARNING! %d additional results in set\n", additional_result);
        }

        break;
    }
    DBREC_TRACE_EXIT;
    return b_ret;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
bool DbRecord::save (DbTaew * table, QSqlDatabase & db)
{
    bool b_ret = false;
    for (;;) {

        QString statement;

        if (isNew ()) {
            // a new record is being added
            statement =
                    QString("INSERT INTO %1 (%2) VALUES (%3);")
                    .arg(table->modifyTableName())
                    .arg(table->commaColumnsNoId ())
                    .arg(table->columnColumns ());
        } else {
            // existing record is being updated
            statement =
                    QString("UPDATE %1 SET %2 WHERE %3 = :%4;\n")
                    .arg(table->modifyTableName())
                    .arg(table->assignColumns ())
                    .arg(table->columnName (table->idColumn ()))
                    .arg(table->columnName (table->idColumn ()));
        }
        DBREC_DEBUGM("%s\n", TMP_A(statement));

        DBG_ASSERT(db.isOpen());
        QSqlQuery query (db);

        DBG_ASSERT(query.driver() != NULL);
        DBG_ASSERT(query.driver()->isOpen());
        DBG_ASSERT(!query.driver()->isOpenError());

        if (!query.prepare(statement)) {
            qWarning () << "prepare failed: " << query.lastQuery();
            qWarning () << "query error" << query.lastError ().text ();
            qWarning () << "database error" << db.lastError ().text ();
            qWarning () << "driver error" << query.driver()->lastError ().text ();
            DBG_ASSERT(false);
            break;
        }
        bind (query);

        if (!query.exec()) {
            qWarning () << "query failed: " << statement;
            qWarning () << query.lastError ().text ();
            break;
        }
        if (isNew ()) {
            setId (static_cast<long>(query.lastInsertId().toLongLong ()));
        }

        b_ret = true;
        break;
    }
    return b_ret;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
bool DbRecord::remFromDb (
        DbTaew * table, QSqlDatabase & db, int column,
        const QString & s_col_value)
{
    bool b_ret = false;
    for (;;) {

        if (isNew ()) {
            qWarning () << "record is new/already deleted";
            b_ret = true;
            break;
        }

        QSqlQuery query (db);
        QString s_col_name = table->columnName (column);
        QString statement =
                QString("DELETE FROM %1 WHERE %2=:%3;\n")
                .arg(table->modifyTableName())
                .arg(s_col_name)
                .arg(s_col_value);
        DBREC_DEBUGM("%s\n", TMP_A(statement));
        if (!query.prepare (statement)) {
            qWarning () << "prepare failed: " << statement;
            qWarning () << query.lastError ().text ();
            DBG_ASSERT(false);
            break;
        }
        bindOne (query, column);
        if (!query.exec()) {
            qWarning () << "query failed: " << statement;
            qWarning () << query.lastError ().text ();
            break;
        }
        setId (DbTable::ID_NEW_INSTANCE);

        b_ret = true;
        break;
    }
    return b_ret;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
long DbRecord::getId () const
{
    // assert(idColumn () == DbTable::ID_NEW_INSTANCE);
    return DbTable::ID_UNAVAILABLE;
}
/* ========================================================================= */
