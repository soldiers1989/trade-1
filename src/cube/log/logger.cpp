#include <stdarg.h>
#include "cube\sys\time.h"
#include "cube\log\logger.h"
BEGIN_CUBE_LOG_NS
//////////////////////////////logger class//////////////////////////////
void logger::debug(const char* format, ...) {
	//message buffer
	const int MSGSZ = 1024;
	char msg[MSGSZ] = { 0 };

	//format message
	va_list args;
	va_start(args, format);
	int sz = vsnprintf(msg, MSGSZ - 1, format, args);
	va_end(args);

	//check message
	if (sz < 0)
		return;

	//print message
	print(level::debug, msg);
}

void logger::info(const char* format, ...) {
	//message buffer
	const int MSGSZ = 1024;
	char msg[MSGSZ] = { 0 };

	//format message
	va_list args;
	va_start(args, format);
	int sz = vsnprintf(msg, MSGSZ - 1, format, args);
	va_end(args);

	//check message
	if (sz < 0)
		return;

	//print message
	print(level::info, msg);
}

void logger::warn(const char* format, ...) {
	//message buffer
	const int MSGSZ = 1024;
	char msg[MSGSZ] = { 0 };

	//format message
	va_list args;
	va_start(args, format);
	int sz = vsnprintf(msg, MSGSZ - 1, format, args);
	va_end(args);

	//check message
	if (sz < 0)
		return;

	//print message
	print(level::warn, msg);
}

void logger::error(const char* format, ...) {
	//message buffer
	const int MSGSZ = 1024;
	char msg[MSGSZ] = { 0 };

	//format message
	va_list args;
	va_start(args, format);
	int sz = vsnprintf(msg, MSGSZ - 1, format, args);
	va_end(args);

	//check message
	if (sz < 0)
		return;

	//print message
	print(level::error, msg);
}

void logger::fatal(const char* format, ...) {
	//message buffer
	const int MSGSZ = 1024;
	char msg[MSGSZ] = { 0 };

	//format message
	va_list args;
	va_start(args, format);
	int sz = vsnprintf(msg, MSGSZ - 1, format, args);
	va_end(args);

	//check message
	if (sz < 0)
		return;

	//print message
	print(level::fatal, msg);
}

void logger::print(level lvl, const char *msg) {
	//log level string
	const char * LEVEL[] = { "debug", "info", "warn", "error", "fatal" };
	std::lock_guard<std::mutex> lock(_mutex);

	//check level
	if (lvl < _level)
		return;

	//add level and time to message
	const int BUFSZ = 1024;
	char buf[BUFSZ] = { 0 };
	int pos = snprintf(buf, BUFSZ, "%s[%s]%s\n", sys::time::now("[%Y%m%d][%H:%M:%S]").c_str(), LEVEL[(int)lvl], msg);
	if (pos > 0 && pos<BUFSZ) {
		buf[pos] = 0;
		msg = buf;
	}

	//print message to output
	if (_printer != 0)
		_printer->print(msg);
}

void logger::set(level lvl) {
	std::lock_guard<std::mutex> lock(_mutex);
	_level = lvl;
}

void logger::set(output out, const char *dir/* = "."*/, const char *name/* = "log"*/, roll ropt/* = roll::none*/, uint fszlimit/* = -1*/) {
	std::lock_guard<std::mutex> lock(_mutex);
	//free old printer
	if (_printer != 0) {
		delete _printer;
	}

	//create new printer
	switch (out) {
	case output::console:
		_printer = new console_printer();
		break;
	case output::file:
		_printer = new file_printer(dir, name, ropt, fszlimit);
		break;
	default:
		_printer = 0;
		break;
	}
}
END_CUBE_LOG_NS
