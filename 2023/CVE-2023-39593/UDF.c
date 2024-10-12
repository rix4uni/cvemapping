#include <stdio.h>
#include <stdlib.h>

enum Item_result {STRING_RESULT, REAL_RESULT, INT_RESULT, ROW_RESULT};

typedef struct st_udf_args {
    unsigned int        arg_count;   // number of arguments
    enum Item_result    *arg_type;   // pointer to item_result
    char                **args;      // pointer to arguments
    unsigned long       *lengths;    // length of string args
    char                *maybe_null; // 1 for maybe_null args
} UDF_ARGS;

typedef struct st_udf_init {
    char                maybe_null;  // 1 if func can return NULL
    unsigned int        decimals;    // for real functions
    unsigned long       max_length;  // for string functions
    char                *ptr;        // free ptr for func data
    char                const_item;  // 0 if result is constant
} UDF_INIT;

int do_system(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error)
{
    if (args->arg_count != 1)
        return(0);

    system(args->args[0]);

    return(0);
}

char do_system_init(UDF_INIT *initid, UDF_ARGS *args, char *message)
{
    return(0);
}
