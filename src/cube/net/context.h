#pragma once
#include "cube\ns.h"
#include <WinSock2.h>
BEGIN_CUBE_NET_NS
//iocp operation
typedef enum io_opt { IO_SEND, IO_RECV } io_opt;

//iocp session context with overlapped structure class
class ioctxt {
public:
	OVERLAPPED overlapped;
	void  *ptr;
	io_opt opt;
	WSABUF buf;

public:
	ioctxt(int sz) : ioctxt(0, sz) {}
	ioctxt(const char *data, int sz) : ioctxt(0, data, sz) {}

	ioctxt(void *ptr, const char *data, int sz);
	ioctxt(int sz, void *ptr);
	~ioctxt();
};
END_CUBE_NET_NS

