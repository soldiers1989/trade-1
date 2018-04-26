#include "cube\sys\dump.h"
#include <DbgHelp.h>

#pragma comment(lib,"DbgHelp.lib")

BEGIN_CUBE_SYS_NS
std::string dump::_name = "cube";

void dump::setup(const char * name) {
	// set dump file prefix name
	_name = name;

	// setup dump handler
	SetUnhandledExceptionFilter(dump_handler);
}

LONG WINAPI dump::dump_handler(LPEXCEPTION_POINTERS lps) {
	// get current system time
	SYSTEMTIME lt;
	GetLocalTime(&lt);

	// create dump file name
	char szFileName[MAX_PATH] = { 0 };
	wsprintf(szFileName, "%s.%04d%02d%02d%02d%02d%02d.dmp", _name.c_str(), lt.wYear, lt.wMonth, lt.wDay, lt.wHour, lt.wMinute, lt.wSecond);

	// create dump file
	HANDLE hDumpFile = CreateFile(szFileName, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hDumpFile == INVALID_HANDLE_VALUE)
		return EXCEPTION_CONTINUE_EXECUTION;

	// create dump informations
	MINIDUMP_EXCEPTION_INFORMATION dumpInfo;
	dumpInfo.ExceptionPointers = lps;
	dumpInfo.ThreadId = GetCurrentThreadId();
	dumpInfo.ClientPointers = TRUE;
	
	// write dump file
	MiniDumpWriteDump(GetCurrentProcess(), GetCurrentProcessId(), hDumpFile, MiniDumpNormal, &dumpInfo, NULL, NULL);
	CloseHandle(hDumpFile);

	return EXCEPTION_EXECUTE_HANDLER;
}
END_CUBE_SYS_NS


