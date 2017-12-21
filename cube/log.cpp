#include "log.h"
#include "fd.h"
#include "tm.h"
#include "str.h"
#include <stdarg.h>
#include <iostream>
BEGIN_CUBE_NAMESPACE
//////////////////////////////logger class//////////////////////////////
const char *log::levelstr[] = { "debug", "info", "warn", "error", "fatal" };
log::level log::_level = log::level::debug;
printer *log::_printer = new console_printer();
std::mutex log::_mutex;

log::log() {

}

log::~log() {
	if (_printer != 0) {
		delete _printer;
		_printer = 0;
	}
}

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

	//add level and time to message
	const int BUFSZ = 1024;
	char buf[BUFSZ] = { 0 };
	int pos = sprintf(buf, "%s[%s]%s\n", tm::now("[%Y%m%d][%H:%M:%S]").c_str(), levelstr[(int)lvl], msg);
	if (pos > 0 && pos<BUFSZ) {
		buf[pos] = 0;
		msg = buf;
	}

	//print message to output
	if (_printer != 0)
		_printer->print(msg);
}

void log::set(level lvl) {
	std::lock_guard<std::mutex> lock(_mutex);
	_level = lvl;
}

void log::set(out out, const char *dir/* = "."*/, const char *name/* = "log"*/, cut ct/* = cut::none*/, uint fszlimit/* = -1*/) {
	std::lock_guard<std::mutex> lock(_mutex);
	//free old printer
	if (_printer != 0) {
		delete _printer;
	}

	//create new printer
	switch (out) {
	case log::out::console:
		_printer = new console_printer();
		break;
	case log::out::file:
		_printer = new file_printer(dir, name, ct, fszlimit);
		break;
	default:
		_printer = 0;
		break;
	}
}

//////////////////////////////console printer//////////////////////////////
void console_printer::print(const char *msg) {
	std::cout << msg;
}


//////////////////////////////file printer//////////////////////////////
file_printer::file_printer(const std::string &dir, const std::string &name, log::cut ct, uint fszlimit) : _dir(dir), _name(name), _cutopt(ct), _currday(0), _fszlimit(fszlimit), _currnum(0), _currfsz(fszlimit) {

}

file_printer::~file_printer() {
	if (_file.is_open()) {
		_file.flush();
		_file.close();
	}
}

void file_printer::print(const char *msg) {
	//get new message size
	int sz = (int)strlen(msg);

	//check if need to cut file
	check_and_cut(sz);

	//write to file
	if (_file.good()) {
		_file.write(msg, sz);
		_currfsz += sz;
	}
}

void file_printer::check_and_cut(int msgsz) {
	switch (_cutopt) {
	case log::cut::none:
		if (!_file.is_open()) {
			_file.open(next_normal_file(), std::ios::out | std::ios::app);
		}
		break;
	case log::cut::sized:
		if (!_file.is_open()) {
			_file.open(next_sized_file(msgsz), std::ios::out | std::ios::app);
		} else {
			if (_currfsz + msgsz > _fszlimit) {
				_file.close();
				_file.open(next_sized_file(msgsz), std::ios::out | std::ios::app);
			}
		}
		break;
	case log::cut::daily:
		if (!_file.is_open()) {
			_file.open(next_daily_file(), std::ios::out | std::ios::app);
		} else {
			if (_currday != tm::now(tm::unit::day)) {
				_file.close();
				_file.open(next_daily_file(), std::ios::out | std::ios::app);
			}
		}
		break;
	default:
		break;
	}
}

std::string file_printer::next_normal_file() {
	if (!fd::exist(_dir)) {
		dir::mkdirs(_dir);
	}

	return path::make(_dir, _name);
}

std::string file_printer::next_daily_file()	{
	if (!fd::exist(_dir)) {
		dir::mkdirs(_dir);
	}

	return path::make(_dir, _name + "." + tm::now("%Y%m%d"));
}

std::string file_printer::next_sized_file(int msgsz) {
	//make log directory
	if (!fd::exist(_dir)) {
		dir::mkdirs(_dir);
	}

	//get next sized file path
	_currnum++;
	std::string fpath = path::make(_dir, str::format("%s.%d", _name.c_str(), _currnum));
	while (true) {
		if (fd::exist(fpath)) {
			size_t sz = 0;
			if (fd::size(fpath, sz) == 0 && sz + msgsz < _fszlimit) {
				_currfsz = sz;
				break;
			}

		} else {
			_currfsz = 0;
			break;
		}		
		_currnum++;
		fpath = path::make(_dir, str::format("%s.%d", _name.c_str(), _currnum));
	}

	return fpath;
}
END_CUBE_NAMESPACE
