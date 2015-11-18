/**
 * @file dbstruct.h
 * @brief Declarations for DbStruct class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBSTRUCT_H_INCLUDE
#define GUARD_DBSTRUCT_H_INCLUDE

#include <dbstruct/dbstruct-config.h>
#include <dbstruct/dbobject.h>
#include <dbstruct/dbtable.h>
#include <dbstruct/dbview.h>

#include <QSqlDatabase>

class DbTaew;

//! The structure of a database.
class DBSTRUCT_EXPORT DbStructMeta : public DbObject {

public:

    //! Default constructor.
    DbStructMeta ();

    //! Destructor.
    virtual ~DbStructMeta();

    //! The type of this object.
    virtual Type
    type () const {
        return DBO_STRUCT;
    }

    //! Create a table or view based on a table or view name.
    virtual DbTaew *
    taew (
            const QString & value) {
        return taew (idFromName (value));
    }


    /*  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  */
    /** @name Interface
    *  This is the list of method that subclasses must
    * implement.
    */
    ///@{

    //! The name of this database.
    virtual QString
    databaseName () const = 0;

    //! Get the name of the table or view based on its identifier.
    virtual QString
    componentName (
            int index) const = 0;

    //! Get the id based on a table or view name.
    virtual int
    idFromName (
            const QString & value) const = 0;

    //! Create a table or view based on a table or view id.
    virtual DbTaew *
    taew (
            int index) const = 0;


    /*  --  T A B L E S  --  */

    //! Convert between component identifier and table identifier.
    virtual int
    comp2table (
            int value) const = 0;

    //! Convert between table identifier and component identifier.
    virtual int
    table2comp (
            int value) const = 0;

    //! Get the id based on a table name.
    virtual int
    tableIdFromName (
            const QString & value) const = 0;

    //! Get the name of the table based on its identifier.
    virtual QString
    tableName (
            int index) const = 0;


    /*  --  V I E W S  --  */

    //! Convert between component identifier and view identifier.
    virtual int
    comp2view (
            int value) const = 0;

    //! Convert between view identifier and component identifier.
    virtual int
    view2comp (
            int value) const = 0;

    //! Get the id based on a view name.
    virtual int
    viewIdFromName (
            const QString & value) const = 0;


    //! Get the name of the view based on its identifier.
    virtual QString
    viewName (
            int index) const = 0;

    ///@}
    /*  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  */

protected:

private:
}; /* class DbStructMeta */


//! The structure of a database.
class DBSTRUCT_EXPORT DbStruct {

    QSqlDatabase db_; /**< accesor */

public:

    //! Default constructor.
    DbStruct() :
        db_()
    {}

    //! Constructor that also initializes the database.
    DbStruct(const QSqlDatabase & db) :
        db_(db)
    {}

    //! Retreive the database.
    inline QSqlDatabase &
            database () {
        return db_;
    }

    //! Set the database.
    inline void
            setDatabase (const QSqlDatabase & value) {
        db_ = value;
    }

    //! Get metadata instance.
    virtual DbStructMeta *
    metaDatabase () = 0;

}; /* class DbStructMeta */

//! Default constructors for inheritants of DbStruct
#define META_DATA_BASE_CTORS(__name__) \
    __name__() : __name__ ## Meta(), DbStruct() {} \
    __name__(const QSqlDatabase & db) : __name__ ## Meta(), DbStruct(db) {}

//! Inheritants of DbStruct must implement a `metaDatabase()` method.
#define META_DATA_BASE_GETTER \
    virtual DbStructMeta * \
    metaDatabase () { \
        return static_cast<DbStructMeta*>(this); \
    }

//! A complete implementation for a DbStruct inheritant.
#define META_DATA_BASE(__name__) \
class %(EXPORT)s __name__ : public __name__ ## Meta, public DbStruct { \
public: \
    META_DATA_BASE_CTORS(__name__); \
    META_DATA_BASE_GETTER; \
};


#endif // GUARD_DBSTRUCT_H_INCLUDE
