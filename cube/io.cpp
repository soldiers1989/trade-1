#include "io.h"
#include "os.h"

BEGIN_CUBE_NAMESPACE
iocp::iocp() {
	open();
}

iocp::~iocp() {
	close();
}

void iocp::open() {
	//create io complete port
	_iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, os::get_cpu_cores());
	if (_iocp == NULL) {
		throw os::last_error();
	}
}

void iocp::bind(HANDLE handle, ULONG_PTR key) {
	if (CreateIoCompletionPort(handle, _iocp, key, 0) == NULL) {
		throw efatal(os::last_error().c_str());
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
END_CUBE_NAMESPACE
