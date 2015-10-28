if (NOT DBSTRUCT_BUILD_MODE)
    set (DBSTRUCT_BUILD_MODE STATIC)
endif ()

include(pile_support)
pileInclude (DbStruct)
dbstructInit(${DBSTRUCT_BUILD_MODE})
