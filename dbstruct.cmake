
# enable/disable cmake debug messages related to this pile
set (DBSTRUCT_DEBUG_MSG ON)

# make sure support code is present; no harm
# in including it twice; the user, however, should have used
# pileInclude() from pile_support.cmake module.
include(pile_support)

# initialize this module
macro    (dbstructInit
          ref_cnt_use_mode)

    # default name
    if (NOT DBSTRUCT_INIT_NAME)
        set(DBSTRUCT_INIT_NAME "DbStruct")
    endif ()

    # compose the list of headers and sources
    set(DBSTRUCT_HEADERS
        "dbobject.h"
        "dbview.h"
        "dbcolumn.h"
        "dbtable.h"
        "dbstruct.h")
    set(DBSTRUCT_SOURCES
        "dbobject.cc"
        "dbview.cc"
        "dbcolumn.cc"
        "dbtable.cc"
        "dbstruct.cc")

    pileSetSources(
        "${DBSTRUCT_INIT_NAME}"
        "${DBSTRUCT_HEADERS}"
        "${DBSTRUCT_SOURCES}")

    pileSetCommon(
        "${DBSTRUCT_INIT_NAME}"
        "0;0;1;d"
        "ON"
        "${ref_cnt_use_mode}"
        ""
        "category1"
        "tag1;tag2")

endmacro ()
