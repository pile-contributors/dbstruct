/**
 * @file dbcolumn.h
 * @brief Declarations for DbColumn class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBDATATYPE_H_INCLUDE
#define GUARD_DBDATATYPE_H_INCLUDE

#include <qglobal.h>

QT_BEGIN_NAMESPACE
class QVariant;
class QSqlRecord;
QT_END_NAMESPACE

class DbTaew;
class DbColumn;
class DbTaew;

namespace DbDataType {
enum Dty {
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
}

//! Callback used to retrieve the value for a DTY_CALLBACK column.
typedef QVariant (*DbColKb) (
        const DbTaew & table,
        const DbColumn & colorig,
        const QSqlRecord & rec,
        int role,
        void * user_data);

#endif // GUARD_DBDATATYPE_H_INCLUDE
