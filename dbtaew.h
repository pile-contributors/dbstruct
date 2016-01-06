/**
 * @file dbtaew.h
 * @brief Declarations for DbTaew class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBTAEW_H_INCLUDE
#define GUARD_DBTAEW_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/dbobject.h>
#include <dbstruct/dbobject.h>

QT_BEGIN_NAMESPACE
class QObject;
class QSqlTableModel;
class QSqlDatabase;
QT_END_NAMESPACE

//! A table or view in a database.
class DBSTRUCT_EXPORT DbTaew : public DbObject {

public:

    //! Special codes
    enum Codes {
        ID_NEW_INSTANCE = -1,
        ID_UNAVAILABLE = -2
    };

    //! Default constructor.
    DbTaew ();

    //! Destructor.
    virtual ~DbTaew();

    //! Tell if a column is part of this table.
    bool
    hasColumn(
            const QString & s_name) const;

    //! Tell the index of a column in this table.
    int
    columnIndex (
            const QString & s_name) const;

    //! Tell the index of a column in the underlying table.
    int
    realColumnIndex (
            const QString & s_name) const;

    //! Create a Sql model for this table.
    virtual QSqlTableModel *
    sqlModel (
            QSqlDatabase & database,
            QObject * parent = NULL) const;


    /*  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  */
    /** @name Interface
    *  These methods MUST be implemented by subclasses.
    */
    ///@{


    //! The name of this table as a string.
    virtual QString
    tableName() const = 0;

    //! Where updates should go.
    virtual QString
    modifyTableName() const {
        return tableName();
    }

    //! The name of a column given an index.
    virtual QString
    columnName(
        int i) const = 0;

    //! The (translated) label for a column given an index.
    virtual QString
    columnLabel (
        int i) const = 0;

    //! Number of columns in this table.
    virtual int
    columnCount() const = 0;

    //! The name of the columns as a list of strings.
    virtual QStringList
    columns() const = 0;

    //! The index of the id column or ID_UNAVAILABLE if no id column.
    virtual int
    idColumn () const = 0;

    //! All columns as a comma-separated list.
    virtual QString
    commaColumns () const = 0;

    //! All columns as a comma-separated list except the id.
    virtual QString
    commaColumnsNoId () const = 0;

    //! All columns as a comma-separated list and :columns.
    virtual QString
    columnColumns () const = 0;

    //! All columns as a comma-separated list of column=:column.
    virtual QString
    assignColumns () const = 0;

    //! Create a column class instance given its index.
    virtual DbColumn
    columnCtor (
            int i) const = 0;

    //! Creates a record of this type.
    virtual DbRecord *
    createDefaultRecord () const = 0;

    //! Convert from virtual indexes to real indexes (-1 => virtual).
    virtual int
    toRealIndex (int) const = 0;

    //! Convert from real indexes to virtual indexes.
    virtual int
    fromRealIndex (int) const = 0;

    ///@}
    /*  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  */

protected:

private:
};

#endif // GUARD_DBTAEW_H_INCLUDE
