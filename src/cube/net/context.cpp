#include "cube\net\context.h"
BEGIN_CUBE_NET_NS
ioctxt::ioctxt(void *ptr, const char *data, int sz) : opt(IO_SEND) {
	ptr = ptr;
	buf.len = sz;
	buf.buf = new char[sz];
	memcpy(buf.buf, data, sz);
	memset(&overlapped, 0, sizeof(overlapped));
}
ioctxt::ioctxt(int sz, void *ptr) : opt(IO_RECV) {
	ptr = ptr;
	buf.len = sz;
	buf.buf = new char[sz];
	memset(&overlapped, 0, sizeof(overlapped));
}

ioctxt::~ioctxt() {
	delete[](buf.buf);
	buf.len = 0;
}
END_CUBE_NET_NS
