#include "cube.h"
#include <Windows.h>

BEGIN_CUBE_NAMESPACE
std::string sys::getlasterror() {
	DWORD ErrorCode = GetLastError();
	HLOCAL LocalAddress = NULL;

	FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_FROM_SYSTEM, NULL, ErrorCode, 0, (PTSTR)&LocalAddress, 0, NULL);
	std::string error((const char*)LocalAddress);

	LocalFree(LocalAddress);

	return error;
}

std::string sys::geterrormsg(int code) {
	HLOCAL LocalAddress = NULL;

	FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_FROM_SYSTEM, NULL, code, 0, (PTSTR)&LocalAddress, 0, NULL);
	std::string error((const char*)LocalAddress);

	LocalFree(LocalAddress);

	return error;
}
END_CUBE_NAMESPACE
