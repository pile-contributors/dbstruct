/**
 * @file dbstruct-private.h
 * @brief Declarations for DbStruct class
 * @author Nicu Tofan <nicu.tofan@gmail.com>
 * @copyright Copyright 2015 piles contributors. All rights reserved.
 * This file is released under the
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */

#ifndef GUARD_DBSTRUCT_PRIVATE_H_INCLUDE
#define GUARD_DBSTRUCT_PRIVATE_H_INCLUDE

#include <dbstruct/dbstruct-config.h>

#if 0
#    define DBSTRUCT_DEBUGM printf
#else
#    define DBSTRUCT_DEBUGM black_hole
#endif

#if 0
#    define DBSTRUCT_TRACE_ENTRY printf("DBSTRUCT ENTRY %s in %s[%d]\n", __func__, __FILE__, __LINE__)
#else
#    define DBSTRUCT_TRACE_ENTRY
#endif

#if 0
#    define DBSTRUCT_TRACE_EXIT printf("DBSTRUCT EXIT %s in %s[%d]\n", __func__, __FILE__, __LINE__)
#else
#    define DBSTRUCT_TRACE_EXIT
#endif

#ifdef _MSC_VER
#   ifndef __func__
#       define __func__ __FUNCTION__
#   endif
#endif

#ifndef TMP_A
#   define TMP_A(__s__) __s__.toLatin1 ().constData ()
#endif

#ifndef STRINGIFY
#   define STRINGIFY(s) STRINGIFY_HELPER(s)
#   define STRINGIFY_HELPER(s) #s
#endif

#ifndef DBG_ASSERT
#ifdef DBSTRUCT_DEBUG
#  define DBG_ASSERT(a) if (!(a)) {\
        printf("\nDBG_ASSERT Failed: " STRINGIFY(a) "\n"); \
        printf("%s[%d]: %s\n\n",__FILE__, __LINE__, __func__); \
        }
#else
#  define DBG_ASSERT(a)
#endif
#endif

static inline void black_hole (...)
{}

#endif // GUARD_DBSTRUCT_PRIVATE_H_INCLUDE
