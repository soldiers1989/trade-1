#include "cube\sys\cpu.h"
#include <Windows.h>

BEGIN_CUBE_SYS_NS
int get_cpu_cores() {
	SYSTEM_INFO si;
	::GetSystemInfo(&si);
	return si.dwNumberOfProcessors;
}
END_CUBE_SYS_NS
