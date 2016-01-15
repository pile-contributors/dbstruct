/**
 * @file dbcolumn.h
 * @brief Declarations for DbColumn class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBCOLUMN_H_INCLUDE
#define GUARD_DBCOLUMN_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/dbobject.h>
#include <dbstruct/dbdatatype.h>

#include <QString>
#include <QVariant>
#include <QSharedDataPointer>

QT_BEGIN_NAMESPACE
class QSqlTableModel;
class QSqlRecord;
QT_END_NAMESPACE

class DbTaew;
class DbColumnData;

//! The column of a database.
class DBSTRUCT_EXPORT DbColumn : public DbObject {

public:

    //! Default constructor.
    DbColumn ();

    //! Constructor.
    explicit DbColumn (
            const QString & col_name,
            DbDataType::Dty datatype,
            int col_id,
            const QString & col_label = QString(),
            int real_col_id = dbstruct::DEFAULT,
            int length = dbstruct::UNDEFINED,
            bool allow_nulls = true,
            bool readonly = false);

    //! Copy constructor.
    DbColumn (const DbColumn &other);

    //! Assignment operator.
    DbColumn &operator= (const DbColumn & other);

    //! Destructor.
    virtual ~DbColumn ();

    //! Tell if this is a virtual column or a real one.
    bool
    isVirtual () const;

    //! Name of the column in the database
    const QString &
    columnName () const;

    //! User-visible name for the column
    const QString &
    columnLabel () const;

    //! ID of the column inside the table
    int
    columnId () const;

    //! ID of the column amongst real columns
    int
    columnRealId () const;

    //! Size of the field in the database
    int
    columnLength () const;

    //! The type of data we're representing
    DbDataType::Dty
    columnType () const;

    //! Does this column allows NULL values?
    bool
    allowNulls () const;

    //! Is the user allowed to modify the values in this column?
    bool
    readOnly () const;



    //! Name of the column in the database
    void
    setColumnName (
            const QString & value);

    //! User-visible name for the column
    void
    setColumnLabel (
            const QString & value);

    //! ID of the column inside the table
    void
    setColumnId (
            int value);

    //! ID of the column amongst real columns
    void
    setColumnRealId (
            int value);

    //! Size of the field in the database
    void
    setColumnLength (
            int value);

    //! Column allows NULL values.
    void
    setAllowNulls (
            bool value);

    //! User allowed to change values.
    void
    setReadOnly (
            bool value);



    //! Create a new column instance using provided values.
    static DbColumn
    col (
            const QString & col_name,
            DbDataType::Dty datatype,
            int col_id,
            const QString & col_label = QString(),
            int real_col_id = dbstruct::DEFAULT,
            int length = dbstruct::UNDEFINED,
            bool allow_nulls = true,
            bool readonly = false);


private:

    QSharedDataPointer<DbColumnData> d; /**< actual internal data */
};

#endif // GUARD_DBCOLUMN_H_INCLUDE
