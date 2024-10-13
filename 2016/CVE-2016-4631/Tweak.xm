#include <substrate.h>

int donothing() {
  HBLogDebug(@"Stubbing TIFF init");
  return 0;
}

%ctor {
  HBLogDebug(@"Disabling TIFF loading");
  MSHookFunction(MSFindSymbol(NULL, "_initImageTIFF"), (void*)&donothing);
}
