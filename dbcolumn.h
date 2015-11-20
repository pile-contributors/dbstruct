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

#include <QString>

//! The columnure of a database.
class DBSTRUCT_EXPORT DbColumn : public DbObject {

public:

    enum DataType {
        DTY_INVALID = -1, /**< invalid data type */

        DTY_BIGINT,
        DTY_BINARY,
        DTY_BIT,
        DTY_CHAR,
        DTY_DATE,
        DTY_DATETIME,
        DTY_DATETIME2,
        DTY_DATETIMEOFFSET,
        DTY_DECIMAL,
        DTY_DECIMALSCALE,
        DTY_FLOAT,
        DTY_HIERARCHYID,
        DTY_IMAGE,
        DTY_INTEGER,
        DTY_MONEY,
        DTY_NCHAR,
        DTY_NTEXT,
        DTY_NUMERIC,
        DTY_NUMERICSCALE,
        DTY_NVARCHAR,
        DTY_REAL,
        DTY_ROWVERSION,
        DTY_SMALLDATETIME,
        DTY_SMALLINT,
        DTY_SMALLMONEY,
        DTY_SQL,
        DTY_TEXT,
        DTY_TIME,
        DTY_TINYINT,
        DTY_UNIQUEIDENTIFIER,
        DTY_VARBINARY,
        DTY_VARCHAR,
        DTY_XML,

        DTY_MAX /**< first invalid value */
    };


    QString col_name_;
    int col_id_;
    int length_;
    QString col_label_;
    DataType datatype_;
    bool nulls_;
    bool autoincrement_;
    QString default_value_;
    bool read_only_;
    QString foreign_table_; /**< The table that this column references */
    QString foreign_key_; /**< Name of the column in the referenced table */
    QStringList foreign_ref_; /**< The columns that should replace this column */

    //! Default constructor.
    DbColumn ();

    //! Default constructor.
    DbColumn (
            const QString & col_name,
            int col_id,
            int length,
            const QString & col_label,
            DataType datatype,
            bool nulls,
            bool autoincrement,
            const QString & default_value,
            bool read_only,
            const QString & foreign_table,
            const QString & foreign_key,
            const QStringList & foreign_ref) : DbObject(),
        col_name_(col_name),
        col_id_(col_id),
        length_(length),
        col_label_(col_label),
        datatype_(datatype),
        nulls_(nulls),
        autoincrement_(autoincrement),
        default_value_(default_value),
        read_only_(read_only),
        foreign_table_(foreign_table),
        foreign_key_(foreign_key),
        foreign_ref_(foreign_ref)
    {
    }

    //! Destructor.
    virtual ~DbColumn();

    //! The type of this object.
    virtual Type
    type () const {
        return DBO_COLUMN;
    }

    //! Tell if this column has a foreign key.
    inline bool
    isForeignKey () const {
        return !foreign_table_.isEmpty();
    }

protected:

private:

};

#endif // GUARD_DBCOLUMN_H_INCLUDE
