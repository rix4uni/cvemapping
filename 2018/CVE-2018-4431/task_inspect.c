switch (flavor) {
    case TASK_INSPECT_BASIC_COUNTS: {
        struct task_inspect_basic_counts *bc;
        uint64_t task_counts[MT_CORE_NFIXED];

        if (size < TASK_INSPECT_BASIC_COUNTS_COUNT) {
            kr = KERN_INVALID_ARGUMENT;
            break;
        }

        mt_fixed_task_counts(task, task_counts);
        bc = (struct task_inspect_basic_counts *)info_out;
#ifdef MT_CORE_INSTRS
        bc->instructions = task_counts[MT_CORE_INSTRS];
#else 
        bc->instructions = 0;
#endif 
        bc->cycles = task_counts[MT_CORE_CYCLES];
        size = TASK_INSPECT_BASIC_COUNTS_COUNT;
        break;
    }
