# Reproducer
Kudos to Mike Dalessio, Francois Chagnon, Florian Weingarten and Jun Kokatsu.
See [BZ 746048](https://bugzilla.gnome.org/show_bug.cgi?id=746048)

# Building on Linux

    $ cmake ../CVE-2015-8710/ -G "Unix Makefiles" -DLIBXML2_LIBRARIES=/path/to/your/library/libxml2.so.2 -DLIBXML2_INCLUDE_DIR=/path/to/your/sources/libxml2-2.9.1/include/
    $ make

## Reproducing on Linux

    $ valgrind ./bin/CVE_2015_8710
    
    Conditional jump or move depends on uninitialised value(s)

# Building on Windows

    λ vcvars32.bat
    λ cmake -G"NMake Makefiles" ..\CVE-2015-8710 
    -DCMAKE_BUILD_TYPE=Release
    -DCMAKE_C_FLAGS_RELEASE="/MT /O2 /Ob2 /Wall /Zi"
    -DLIBXML2_LIBRARIES=C:\Users\karm\WORKSPACE\libxmldevel\lib\libxml2.lib
    -DLIBXML2_INCLUDE_DIR=C:\Users\karm\WORKSPACE\libxmldevel\include\libxml2\

## Reproducing on Windows

    λ drmemory.exe -- CVE_2015_8710.exe
    
    UNINITIALIZED READ: reading

