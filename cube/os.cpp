#include "os.h"
#include <Windows.h>

BEGIN_CUBE_NAMESPACE
std::string os::last_error() {
	return last_error(::GetLastError());
}

std::string os::last_error(int error_code) {
	HLOCAL LocalAddress = NULL;

	FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_FROM_SYSTEM, NULL, error_code, 0, (PTSTR)&LocalAddress, 0, NULL);
	std::string error((const char*)LocalAddress);

	LocalFree(LocalAddress);

	return error;
}
END_CUBE_NAMESPACE
