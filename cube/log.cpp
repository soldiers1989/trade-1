#include "log.h"
#include "fd.h"
#include <stdarg.h>
#include <iostream>
BEGIN_CUBE_NAMESPACE
void log::debug(const char* format, ...) {
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

void log::info(const char* format, ...) {
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

void log::warn(const char* format, ...) {
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

void log::error(const char* format, ...) {
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

void log::fatal(const char* format, ...) {
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

void log::print(level lvl, const char *msg) {
	std::lock_guard<std::mutex> lock(_mutex);

	//check level
	if (lvl < _level)
		return;

	//print message to output
	if (_printer != 0)
		_printer->print(msg);
}

void log::set(level lvl) {
	std::lock_guard<std::mutex> lock(_mutex);
	_level = lvl;
}

void log::set(out out, const char *dir = ".", const char *name = "log", cut ct = cut::none, uint fszlimit = -1) {
	std::lock_guard<std::mutex> lock(_mutex);
	//free old printer
	if (_printer != 0) {
		delete _printer;
	}

	//create new printer
	switch (out) {
	case cube::log::console:
		_printer = new console_printer();
		break;
	case cube::log::file:
		_printer = new file_printer(dir, name, ct, fszlimit);
		break;
	default:
		_printer = 0;
		break;
	}
}

void console_printer::print(const char *msg) {
	std::cout << msg;
}

file_printer::file_printer(const std::string &dir, const std::string &name, log::cut ct = log::cut::none, uint fszlimit = -1) : _dir(dir), _name(name), _cutopt(ct), _fszlimit(fszlimit), _num(-1) {
	switch (ct) {
	case cube::log::none:
		open_normal_file();
		break;
	case cube::log::size:
		open_sized_file();
		break;
	case cube::log::daily:
		open_daily_file();
		break;
	default:
		break;
	}
}

file_printer::~file_printer() {
	if (_file.is_open()) {
		_file.flush();
		_file.close();
	}
}

void file_printer::print(const char *msg) {
	//check if need to cut file
	int sz = (int)strlen(msg);
	check_and_cut(sz);

	//write to file
	if (_file.good()) {
		_file.write(msg, sz);
	}
}

void file_printer::check_and_cut(int msgsz) {

}

void file_printer::open_sized_file() {

}

void file_printer::open_daily_file() {

}

void file_printer::open_normal_file() {
	_file.open(cube::path::make(_dir, _name+".log"), std::ios::out);
}
END_CUBE_NAMESPACE
