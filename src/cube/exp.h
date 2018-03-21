#pragma once
#include <string>
#include <stdarg.h>
#include <exception>
#include "cube\ns.h"
BEGIN_CUBE_NS
//cube exception
class cexception : public std::exception {
public:
	cexception() : _msg("unkown exception") {}
	explicit cexception(const char *format, ...) {
		/*this buffer is properly not safe*/
		static const int BUFSZ = 1024;
		char buf[BUFSZ] = { 0 };

		va_list va;
		va_start(va, format);
		vsnprintf(buf, BUFSZ, format, va);
		va_end(va);

		_msg = std::string(buf);
	}

	virtual ~cexception() {}

	char const* what() const {
		return _msg.c_str();
	}

public:
	std::string _msg;
};

template<class T> void throw_assign(std::string *dest, const std::string &val) {
	if (dest != 0) {
		*dest = val;
	} else {
		throw T(val.c_str());
	}
}
END_CUBE_NS
