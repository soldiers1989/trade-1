#include "io.h"
#include "sa.h"
#include <Windows.h>

BEGIN_CUBE_NAMESPACE
iocp::iocp() {
	//current thread limit for complete port
	static const DWORD CONCURRENT_THREADS = 0;

	//create io complete port
	_iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, CONCURRENT_THREADS);
	if (_iocp == NULL) {
		throw sa::last_exception();
	}
}

iocp::~iocp() {
	CloseHandle(_iocp);
}

void iocp::bind(void *handle) {
	if (CreateIoCompletionPort(handle, _iocp, (ULONG_PTR)(*&handle), 0) == NULL) {
		throw sa::last_exception();
	}
}

void iocp::unbind(void *handle) {

}

iocp_res iocp::pull(int waitsec/* = -1*/) {
	iocp_res res;
	if (!GetQueuedCompletionStatus(_iocp, &res.transfered, &res.completionkey, (LPOVERLAPPED*)&res.overlapped, waitsec)) {
		res.error = WSAGetLastError();
	}
	return res;
}
END_CUBE_NAMESPACE
