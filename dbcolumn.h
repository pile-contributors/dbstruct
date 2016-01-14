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
#include <QVariant>

QT_BEGIN_NAMESPACE
class QSqlTableModel;
class QSqlRecord;
QT_END_NAMESPACE

class DbTaew;

//! The colum of a database.
class DBSTRUCT_EXPORT DbColumn : public DbObject {

public:

    enum ForeignBehavior {
        FB_CHOOSE, /**< the user can choose values from the other table */
        FB_CHOOSE_ADD /**< the user can choose values from or add values to the other table */
    };

    enum DataType {
        DTY_INVALID = -1, /**< invalid data type */

        DTY_BIGINT,
        DTY_BINARY,
        DTY_BIT,
        DTY_TRISTATE,
        DTY_CHAR,
        DTY_CHOICE,
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

        DTY_CALLBACK, /**< dynamically computed value or retrieved from database */

        DTY_MAX /**< first invalid value */
    };

    enum BoolFormat {
        BF_Y_UPPER,
        BF_T_UPPER,

        BF_YES_CAMEL,
        BF_YES_LOWER,
        BF_YES_UPPER,

        BF_ON_CAMEL,
        BF_ON_LOWER,
        BF_ON_UPPER,

        BF_TRUE_CAMEL,
        BF_TRUE_LOWER,
        BF_TRUE_UPPER,

        BF_STRING_ON
    };

    //! Callback used to retrieve the value for a DTY_CALLBACK column.
    typedef QVariant (*Callback) (
            const DbTaew & table,
            const DbColumn & colorig,
            const QSqlRecord & rec,
            int role,
            void * user_data);

    union ColFormat {
        // cppcheck-suppress unusedStructMember
        BoolFormat bit_; /**< for `DTY_BIT` datatype it is one of BoolFormat */
        // cppcheck-suppress unusedStructMember
        int width_; /**< field width if applicable */
        Callback callback_; /**< for `DTY_CALLBACK` datatype it a callback */
    };

    QString col_name_;
    int col_id_;
    int real_col_id_;
    int length_;
    QString col_label_;
    DataType datatype_;
    bool nulls_;
    bool autoincrement_;
    QString default_value_;
    bool read_only_;
    int virtrefcol_;
    QString foreign_table_; /**< The table that this column references */
    QString foreign_key_; /**< Name of the column in the referenced table */
    QString foreign_ref_; /**< The columns that should replace this column */
    ForeignBehavior foreign_behavior_; /**< how are we going to interact with foreign table */

    QString original_format_; /**< actual format passed to the constructor */
    // following values are extracted from original_format_ in constructor
    ColFormat format_; /**< column format (depends on datatype */
    QChar fill_char_; /**< character used for padding, if any */
    char nr_format_; /**< number format (e, E, f, g, G) */
    int precision_; /**< number of significant digits for real numbers, base for integers */

    //! Default constructor.
    DbColumn ();

    //! Default constructor.
    DbColumn (
            const QString & col_name,
            int col_id,
            int real_col_id,
            int length,
            const QString & col_label,
            DataType datatype,
            bool nulls,
            bool autoincrement,
            const QString & default_value,
            const QString & format,
            bool read_only,
            int virtrefcol,
            const QString & foreign_table,
            const QString & foreign_key,
            const QString & foreign_ref,
            ForeignBehavior foreign_behavior) ;

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

    //! Tell if this column is a virtual one.
    inline bool
    isVirtual () const {
        return virtrefcol_ != -1;
    }

    //! Tell if this column is a virtual one.
    inline bool
    isDynamic () const {
        return datatype_ == DTY_CALLBACK;
    }

    //! Retrieve the data using the callback.
    QVariant kbData (
            const DbTaew & table,
            const QSqlRecord & rec,
            int role = Qt::DisplayRole,
            void * user_data = NULL) const;

    QVariant
    formattedData (
        const QVariant &original_value) const;

protected:

private:

};

#endif // GUARD_DBCOLUMN_H_INCLUDE
