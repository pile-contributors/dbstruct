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

/**
 * @class DbColumn
 *
 * Detailed description.
 */

/* ------------------------------------------------------------------------- */
DbColumn::DbColumn (
        const QString & col_name,
        int col_id,
        int length,
        const QString & col_label,
        DataType datatype,
        bool nulls,
        bool autoincrement,
        const QString & default_value,
        const QString & format,
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
    foreign_ref_(foreign_ref),
    original_format_(format),
    format_(),
    fill_char_(),
    nr_format_('f'),
    precision_(-1)
{
    switch (datatype_) {
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
        if (sl.length() == 0) {
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
        if (sl.length() == 0) {
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
                DBSTRUCT_DEBUGM("Format width for real numbers "
                                "in column %s is not an integer\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            }
            if (sl.at(1).length() != 1) {
                DBSTRUCT_DEBUGM("Format character for real numbers "
                                "in column %s is not a single character\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            } else {
                nr_format_ = sl.at(2).at(0).toLatin1();
            }
            precision_ = sl.at(2).toInt (&b_ok);
            if (!b_ok) {
                DBSTRUCT_DEBUGM("Precision for real numbers "
                                "in column %s is not an integer\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            }
            if (sl.at(2).length() != 1) {
                DBSTRUCT_DEBUGM("Padding character for real numbers "
                                "in column %s is not a single character\n",
                                TMP_A(original_format_),
                                TMP_A(col_name));
            } else {
                fill_char_ = sl.at(3).at(0);
            }
        }
        break; }
    }
}
/* ========================================================================= */


/* ------------------------------------------------------------------------- */
/**
 * Detailed description for .
 */
DbColumn::DbColumn() : DbObject(),
    col_name_(),
    col_id_(-1),
    length_(-1),
    col_label_(),
    datatype_(),
    nulls_(false),
    autoincrement_(false),
    default_value_(),
    read_only_(),
    foreign_table_(),
    foreign_key_(),
    foreign_ref_(),
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
 * Detailed description for decolumnor.
 */
DbColumn::~DbColumn()
{
    DBSTRUCT_TRACE_ENTRY;

    DBSTRUCT_TRACE_EXIT;
}
/* ========================================================================= */
