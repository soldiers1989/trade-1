#include "cube\sys\cpu.h"
#include "cube\net\iocp.h"
#include "cube\sys\error.h"
BEGIN_CUBE_NET_NS
void iocp::open() {
	//create io complete port
	_iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, sys::get_cpu_cores());
	if (_iocp == NULL) {
		throw sys::last_error();
	}
}

void iocp::bind(HANDLE handle, ULONG_PTR key) {
	if (CreateIoCompletionPort(handle, _iocp, key, 0) == NULL) {
		throw efatal(sys::last_error().c_str());
	}
}

iores iocp::pull(int waitmsec/* = -1*/) {
	iores res;
	if (!GetQueuedCompletionStatus(_iocp, &res.transfered, &res.completionkey, (LPOVERLAPPED*)&res.overlapped, waitmsec)) {
		res.error = WSAGetLastError();
	}

	return res;
}

void iocp::close() {
	if (_iocp != INVALID_HANDLE_VALUE) {
		CloseHandle(_iocp);
		_iocp = INVALID_HANDLE_VALUE;
	}
}
END_CUBE_NET_NS
