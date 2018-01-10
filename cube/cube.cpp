#include "cube.h"
#include <string>
#include <cstdarg>
BEGIN_CUBE_NAMESPACE
cexception::cexception(const char *format, ...){
	/*this buffer is properly not safe*/
	static const int BUFSZ = 1024;
	char buf[BUFSZ] = { 0 };

	va_list va;
	va_start(va, format);
	vsnprintf(buf, BUFSZ, format, va);
	va_end(va);

	_msg = std::string(buf);
}

char const* cexception::what() const {
	return _msg.c_str();
}
END_CUBE_NAMESPACE

