/**
 * @file dbcolumn.cc
 * @brief Definitions for DbColumn class.
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#include "dbcolumn.h"
#include "dbstruct-private.h"

#include <QVariant>
#include <QCoreApplication>

/**
 * @class DbColumn
 *
 *
 */

/* ------------------------------------------------------------------------- */
DbColumn::DbColumn (
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
        ForeignBehavior foreign_behavior) : DbObject(),
    col_name_(col_name),
    col_id_(col_id),
    real_col_id_(real_col_id),
    length_(length),
    col_label_(col_label),
    datatype_(datatype),
    nulls_(nulls),
    autoincrement_(autoincrement),
    default_value_(default_value),
    read_only_(read_only),
    virtrefcol_(virtrefcol),
    foreign_table_(foreign_table),
    foreign_key_(foreign_key),
    foreign_ref_(foreign_ref),
    foreign_behavior_(foreign_behavior),
    original_format_(format),
    format_(),
    fill_char_(),
    nr_format_('f'),
    precision_(-1)
{
    switch (datatype_) {
    case DTY_TRISTATE:
    case DTY_BIT: {
        if (!original_format_.compare(QLatin1String ("Yes"), Qt::CaseSensitive)) {
            format_.bit_ = BF_YES_CAMEL;
        } else if (!original_format_.compare(QLatin1String ("yes"), Qt::CaseSensitive)) {
            format_.bit_ = BF_YES_LOWER;
        } else if (!original_format_.compare(QLatin1String ("YES"), Qt::CaseSensitive)) {
            format_.bit_ = BF_YES_UPPER;
        } else if (!original_format_.compare(QLatin1String ("On"), Qt::CaseSensitive)) {
            format_.bit_ = BF_ON_CAMEL;
        } else if (!original_format_.compare(QLatin1String ("on"), Qt::CaseSensitive)) {
            format_.bit_ = BF_ON_LOWER;
        } else if (!original_format_.compare(QLatin1String ("ON"), Qt::CaseSensitive)) {
            format_.bit_ = BF_ON_UPPER;
        } else if (!original_format_.compare(QLatin1String ("True"), Qt::CaseSensitive)) {
            format_.bit_ = BF_TRUE_CAMEL;
        } else if (!original_format_.compare(QLatin1String ("true"), Qt::CaseSensitive)) {
            format_.bit_ = BF_TRUE_LOWER;
        } else if (!original_format_.compare(QLatin1String ("TRUE"), Qt::CaseSensitive)) {
            format_.bit_ = BF_TRUE_UPPER;
        } else if (!original_format_.compare(QLatin1String ("Y"), Qt::CaseSensitive)) {
            format_.bit_ = BF_Y_UPPER;
        } else if (!original_format_.compare(QLatin1String ("T"), Qt::CaseSensitive)) {
            format_.bit_ = BF_T_UPPER;
        } else {
            format_.bit_ = BF_STRING_ON;
        }
        break; }
    case DTY_SMALLINT:
    case DTY_BIGINT:
    case DTY_TINYINT:
    case DTY_INTEGER: {
        QStringList sl = original_format_.split(QChar('`'));
        if ((sl.length() == 0) || ((sl.length() == 1) && sl.at(0).isEmpty())) {
            format_.width_ = 0;
            precision_ = 10;
            fill_char_ = ' ';
        } else if (sl.length() != 3) {
            DBSTRUCT_DEBUGM("instead of 3, the format for integers (%s) "
                            "in column %s has %d elements\n",
                            TMP_A(original_format_),
                            TMP_A(col_name),
                            sl.length());
            format_.width_ = 0;
            precision_ = 10;
            fill_char_ = ' ';
        } else {
            bool b_ok;
            format_.width_ = sl.at(0).toInt (&b_ok);
            if (!b_ok) {
                DBSTRUCT_DEBUGM("Format width for integers (%s) in column %s "
                                "is not an integer\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            }
            precision_ = sl.at(1).toInt (&b_ok);
            if (!b_ok) {
                DBSTRUCT_DEBUGM("Base for integers (%s) in column %s "
                                "is not an integer\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            }
            if (sl.at(2).length() != 1) {
                DBSTRUCT_DEBUGM("Padding character for integers (%s) "
                                "in column %s "
                                "is not a single character\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            } else {
                fill_char_ = sl.at(2).at(0);
            }
        }
        break; }
    case DTY_REAL:
    case DTY_MONEY:
    case DTY_SMALLMONEY:
    case DTY_NUMERIC:
    case DTY_NUMERICSCALE:
    case DTY_FLOAT:
    case DTY_DECIMALSCALE:
    case DTY_DECIMAL: {
        QStringList sl = original_format_.split(QChar('`'));
        if ((sl.length() == 0) || ((sl.length() == 1) && sl.at(0).isEmpty())) {
            format_.width_ = 0;
            precision_ = 8;
            nr_format_ = 'f';
            fill_char_ = ' ';
        } else if (sl.length() != 4) {
            DBSTRUCT_DEBUGM("instead of 4, the format for real numbers (%s) "
                            "in column %s has %d elements\n",
                            TMP_A(original_format_),
                            TMP_A(col_name),
                            sl.length());
            format_.width_ = 0;
            precision_ = 8;
            nr_format_ = 'f';
            fill_char_ = ' ';
        } else {
            bool b_ok;
            format_.width_ = sl.at(0).toInt (&b_ok);
            if (!b_ok) {
                DBSTRUCT_DEBUGM("Format width for real numbers (%s) "
                                "in column %s is not an integer\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            }
            if (sl.at(1).length() != 1) {
                DBSTRUCT_DEBUGM("Format character for real numbers (%s) "
                                "in column %s is not a single character\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            } else {
                nr_format_ = sl.at(1).at(0).toLatin1();
            }
            precision_ = sl.at(2).toInt (&b_ok);
            if (!b_ok) {
                DBSTRUCT_DEBUGM("Precision for real numbers (%s) "
                                "in column %s is not an integer\n",
                                TMP_A(sl.at(1)),
                                TMP_A(col_name));
            }
            if (sl.at(3).length() != 1) {
                DBSTRUCT_DEBUGM("Padding character for real numbers (%s) "
                                "in column %s is not a single character\n",
                                TMP_A(sl.at(3)),
                                TMP_A(col_name));
            } else {
                fill_char_ = sl.at(3).at(0);
            }
        }
        break; }
    case DTY_CALLBACK: {
        format_.callback_ = NULL;
        break; }
    }
}
/* ========================================================================= */


/* ------------------------------------------------------------------------- */
/**
 *
 */
DbColumn::DbColumn() : DbObject(),
    col_name_(),
    col_id_(-1),
    real_col_id_(-1),
    length_(-1),
    col_label_(),
    datatype_(DTY_INVALID),
    nulls_(false),
    autoincrement_(false),
    default_value_(),
    read_only_(false),
    virtrefcol_(-1),
    foreign_table_(),
    foreign_key_(),
    foreign_ref_(),
    foreign_behavior_(FB_CHOOSE),
    original_format_(),
    format_(),
    fill_char_(),
    nr_format_('f'),
    precision_(-1)
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 *
 */
DbColumn::~DbColumn()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
/**
 * If the callback was not set QVariant() is returned.
 *
 * @param table The table where this column belongs.
 * @param rec The record for which data is being requested.
 * @param role Requested role.
 * @param user_data Opaque data passed along to the callback.
 * @return The data for this record and column.
 */
QVariant DbColumn::kbData (const DbTaew &table, const QSqlRecord & rec, int role, void * user_data) const
{
    if (!isDynamic()) {
        DBSTRUCT_DEBUGM ("Column %d is NOT dynamic but callback was used\n",
                        col_id_);
        return QVariant ();
    }

    if (format_.callback_ == NULL) {
        DBSTRUCT_DEBUGM ("Column %d is dynamic but no callback is installed\n",
                        col_id_);
        return QVariant ();
    }

    return format_.callback_ (table, *this, rec, role, user_data);
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
QString tristateToString (
        int value, const QString & s_true,
        const QString & s_false, const QString & s_undef = QString())
{
    if (value == Qt::Unchecked) return s_false;
    else if (value == Qt::Checked) return s_true;
    else return s_undef;
}
/* ========================================================================= */

/* ------------------------------------------------------------------------- */
QVariant DbColumn::formattedData (const QVariant & original_value) const
{
    QVariant result = original_value;
    switch (datatype_) {
    case DbColumn::DTY_DATE: {
        // see [here](http://doc.qt.io/qt-5/qdatetime.html#toString)
        QDate dt = result.toDate ();
        if (dt.year() == 1970 && dt.month() == 1 && dt.day() == 1) {
            result = QString ();
        } else {
            result = dt.toString(
                        QCoreApplication::translate("UserTime", "yyyy-MMM-dd"));
        }
        break; }
    case DbColumn::DTY_TIME: {
        // see [here](http://doc.qt.io/qt-5/qdatetime.html#toString)
        result = result.toTime().toString(
            QCoreApplication::translate(
                "UserTime", "h:mm:ss"));
        break; }
    case DbColumn::DTY_DATETIME: {
        // see [here](http://doc.qt.io/qt-5/qdatetime.html#toString)
        QDateTime dt (result.toDateTime());
        if (!dt.isValid ()) {
            dt.fromString (result.toString ());
        }
        if (
                dt.date ().year() == 1970 &&
                dt.date ().month() == 1 &&
                dt.date ().day() == 1) {
            result = QString ();
        } else {
            result = dt.toString(
                QCoreApplication::translate(
                    "UserTime", "yyyy-MMM-dd h:mm:ss"));
        }
        break; }
    case DbColumn::DTY_SMALLINT:
    case DbColumn::DTY_BIGINT:
    case DbColumn::DTY_TINYINT:
    case DbColumn::DTY_INTEGER: {
        if (!original_format_.isEmpty()) {
            result = QString("%1").arg(
                        result.toLongLong(),
                        format_.width_,
                        precision_,
                        fill_char_);
        }
        break; }
    case DbColumn::DTY_REAL:
    case DbColumn::DTY_MONEY:
    case DbColumn::DTY_SMALLMONEY:
    case DbColumn::DTY_NUMERIC:
    case DbColumn::DTY_NUMERICSCALE:
    case DbColumn::DTY_FLOAT:
    case DbColumn::DTY_DECIMALSCALE:
    case DbColumn::DTY_DECIMAL: {
        if (!original_format_.isEmpty()) {
            double intermed = result.toReal();
            if (result.isNull() || qIsNaN (intermed)) {
                result = QString ();
            } else {
                result = QString("%1").arg(
                            intermed,
                            format_.width_,
                            nr_format_,
                            precision_,
                            fill_char_);
            }
        }
        break;}
    case DbColumn::DTY_BIT: {
        switch (format_.bit_) {
        case DbColumn::BF_YES_CAMEL: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "Yes") :
                        QCoreApplication::translate("DbModel", "No");
            break; }
        case DbColumn::BF_YES_LOWER: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "yes") :
                        QCoreApplication::translate("DbModel", "no");
            break; }
        case DbColumn::BF_YES_UPPER: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "YES") :
                        QCoreApplication::translate("DbModel", "NO");
            break; }
        case DbColumn::BF_ON_CAMEL: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "On") :
                        QCoreApplication::translate("DbModel", "Off");
            break; }
        case DbColumn::BF_ON_LOWER: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "on") :
                        QCoreApplication::translate("DbModel", "off");
            break; }
        case DbColumn::BF_ON_UPPER: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "ON") :
                        QCoreApplication::translate("DbModel", "OFF");
            break; }
        case DbColumn::BF_TRUE_CAMEL: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "True") :
                        QCoreApplication::translate("DbModel", "False");
            break; }
        case DbColumn::BF_TRUE_LOWER: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "true") :
                        QCoreApplication::translate("DbModel", "false");
            break; }
        case DbColumn::BF_TRUE_UPPER: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "TRUE") :
                        QCoreApplication::translate("DbModel", "FALSE");
            break; }
        case DbColumn::BF_Y_UPPER: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "Y") :
                        QCoreApplication::translate("DbModel", "N");
            break; }
        case DbColumn::BF_T_UPPER: {
            result = result.toBool() ?
                        QCoreApplication::translate("DbModel", "T") :
                        QCoreApplication::translate("DbModel", "F");
            break; }
        default: // DbColumn::BF_STRING_ON
            result = result.toBool() ?
                        original_format_ :
                        QString();
        }

        break;}
    case DbColumn::DTY_TRISTATE: {
        switch (format_.bit_) {
        case DbColumn::BF_YES_CAMEL: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "Yes"),
                        QCoreApplication::translate("DbModel", "No"));
            break; }
        case DbColumn::BF_YES_LOWER: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "yes"),
                        QCoreApplication::translate("DbModel", "no"));
            break; }
        case DbColumn::BF_YES_UPPER: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "YES"),
                        QCoreApplication::translate("DbModel", "NO"));
            break; }
        case DbColumn::BF_ON_CAMEL: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "On"),
                        QCoreApplication::translate("DbModel", "Off"));
            break; }
        case DbColumn::BF_ON_LOWER: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "on"),
                        QCoreApplication::translate("DbModel", "off"));
            break; }
        case DbColumn::BF_ON_UPPER: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "ON"),
                        QCoreApplication::translate("DbModel", "OFF"));
            break; }
        case DbColumn::BF_TRUE_CAMEL: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "True"),
                        QCoreApplication::translate("DbModel", "False"));
            break; }
        case DbColumn::BF_TRUE_LOWER: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "true"),
                        QCoreApplication::translate("DbModel", "false"));
            break; }
        case DbColumn::BF_TRUE_UPPER: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "TRUE"),
                        QCoreApplication::translate("DbModel", "FALSE"));
            break; }
        case DbColumn::BF_Y_UPPER: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "Y"),
                        QCoreApplication::translate("DbModel", "N"));
            break; }
        case DbColumn::BF_T_UPPER: {
            result = tristateToString (
                        result.toInt(),
                        QCoreApplication::translate("DbModel", "T"),
                        QCoreApplication::translate("DbModel", "F"));
            break; }
        default: // DbColumn::BF_STRING_ON
            result = tristateToString (
                        result.toInt(),
                        original_format_,
                        QString());
        }

        break;}
    default: break;
    };

    return result;
}
/* ========================================================================= */
