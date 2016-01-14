/**
 * @file dbcolumndata.h
 * @brief Declarations for DbColumnData class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBCOLUMN_DATA_H_INCLUDE
#define GUARD_DBCOLUMN_DATA_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/dbobject.h>
#include <dbstruct/dbdatatype.h>

#include <QSharedData>

//! The column of a database.
class DBSTRUCT_EXPORT DbColumnData : public QSharedData {

public:

    DbColumnData ();

    DbColumnData (
            const QString & col_name,
            const QString & col_label,
            int col_id,
            int real_col_id,
            int length,
            DataType datatype,
            bool allow_nulls = true);

    DbColumnData (
            const DbColumnData &other);

    virtual ~DbColumnData () {}

    QString col_name_; /**< name of the column in the database */
    QString col_label_; /**< User-visible name for the column */
    int col_id_; /**< ID of the column inside the table */
    int real_col_id_; /**< ID of the column amongst real columns */
    int length_; /**< size of the field in the database */
    DataType datatype_; /**< the type of data we're representing */
    bool allow_nulls_; /**< Does this column allows NULL values? */
};

#endif // GUARD_DBCOLUMN_DATA_H_INCLUDE
