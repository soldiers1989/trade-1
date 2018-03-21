#include "cube\str\format.h"
#include <stdarg.h>
BEGIN_CUBE_STR_NS
std::string format(const char *format, ...) {
	/*this buffer is properly not safe*/
	static const int BUFSZ = 1024;
	char buf[BUFSZ] = { 0 };

	va_list va;
	va_start(va, format);
	vsnprintf(buf, BUFSZ, format, va);
	va_end(va);

	return std::string(buf);
}

void format(std::string &result, const char *format, ...) {
	static const int BUFSZ = 1024;
	char buf[BUFSZ] = { 0 };

	va_list va;
	va_start(va, format);
	vsnprintf(buf, BUFSZ, format, va);
	va_end(va);

	result.assign(buf);
}
END_CUBE_STR_NS
