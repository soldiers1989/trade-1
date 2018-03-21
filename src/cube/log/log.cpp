#include <stdarg.h>
#include "cube\log\log.h"
BEGIN_CUBE_LOG_NS
logger g_logger;
void debug(const char* format, ...) {
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
	g_logger.print(level::debug, msg);
}

void info(const char* format, ...) {
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
	g_logger.print(level::info, msg);
}

void warn(const char* format, ...) {
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
	g_logger.print(level::warn, msg);
}

void error(const char* format, ...) {
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
	g_logger.print(level::error, msg);
}

void fatal(const char* format, ...) {
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
	g_logger.print(level::fatal, msg);
}

void set(level lvl) {
	g_logger.set(lvl);
}

void set(output out, const char *dir, const char *name, roll ropt, uint fszlimit) {
	g_logger.set(out, dir, name, ropt, fszlimit);
}
END_CUBE_LOG_NS