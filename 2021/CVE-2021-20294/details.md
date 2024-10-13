## details

 - vuln https://nvd.nist.gov/vuln/detail/CVE-2021-20294
 - description 
    * https://sourceware.org/bugzilla/show_bug.cgi?id=26929
    * https://p.ost2.fyi/courses/course-v1:OpenSecurityTraining2+Vulns1001_C-derived+2022_v1/courseware/15185a52d4c64760be76911a9edacc8f/a3c5de12340f4b50ab45443de90770e3/6?activate_block_id=block-v1%3AOpenSecurityTraining2%2BVulns1001_C-derived%2B2022_v1%2Btype%40vertical%2Bblock%400420b3b38e004946834899f83d65fbcb


### chatgpt session

**Q:** Can you describe me where is the vuln in CVE-2021-20294 of readelf ?

**A:** CVE-2021-20294 is a vulnerability that was discovered in the GNU Binutils readelf utility, which is ..  // he was describing the vuln and basically telling which data structures where in touch but then suddenly removing the answer. I think because the info is of 2021


**Q:** In binutils project, what does the following function do?

```c
static const char * get_symbol_version_string (Filedata *                   filedata,
                           bfd_boolean                  is_dynsym,
                           const char *                 strtab,
                           unsigned long int            strtab_size,
                           unsigned int                 si,
                           Elf_Internal_Sym *           psym,
                           enum versioned_symbol_info * sym_info,
                           unsigned short *             vna_other)
```

**A:** The function `static const char * get_symbol_version_string (Filedata *filedata, bfd_boolean is_dynsym, const char *strtab, unsigned long int strtab_size, unsigned int si, Elf_Internal_Sym *psym, enum versioned_symbol_info *sym_info, unsigned short *vna_other)` is a function that is part of the binutils project. It appears to be used to extract version information from a symbol in an ELF object file.

In more detail, this function takes several parameters as input:

    Filedata *filedata: pointer to a struct containing information about the ELF object file being parsed.
    bfd_boolean is_dynsym: a boolean value indicating whether the symbol being processed is from the dynamic symbol table or the regular symbol table.
    const char *strtab: pointer to the string table of the ELF object file.
    unsigned long int strtab_size: size of the string table.
    unsigned int si: index of the symbol in the symbol table.
    Elf_Internal_Sym *psym: pointer to the symbol's data.
    enum versioned_symbol_info *sym_info: pointer to a struct where the version information will be stored.
    unsigned short *vna_other: pointer to a variable where the version index of the symbol will be stored.

The function uses the provided information to extract the symbol's version information, such as its version name and version index, from the ELF object file and stores them in the sym_info and vna_other variables. It then returns a pointer to the version name string in the string table.

It's worth noting that this function is part of the binutils project, which is a collection of binary utilities, including tools like ld, ar, and objdump, that perform various operations on object files, such as linking and disassembling.
It's important to note that the codebase of binutils is constantly changing, so the functionality of this function may be different in the current version of the project.
I recommend checking the documentation, comments or the context of the codebase of the specific version you're using to find more information about the function you're looking for.

**Q:** how to compile an ELF to have symbol version information ?

**A:** etc.


