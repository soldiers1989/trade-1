#include <iostream>
#include "cube\sys\time.h"
#include "cube\sys\file.h"
#include "cube\sys\path.h"
#include "cube\str\strip.h"
#include "cube\str\format.h"
#include "cube\log\printer.h"
BEGIN_CUBE_LOG_NS
//////////////////////////////console printer//////////////////////////////
void console_printer::print(const char *msg) {
	std::cout << msg;
}

//////////////////////////////file printer//////////////////////////////
file_printer::file_printer(const std::string &dir, const std::string &name, roll ropt, uint fszlimit) : _dir(dir), _name(name), _ropt(ropt), _currday(0), _fszlimit(fszlimit), _currnum(0), _currfsz(fszlimit) {

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
	switch (_ropt) {
	case roll::none:
		if (!_file.is_open()) {
			_file.open(next_normal_file(), std::ios::out | std::ios::app);
		}
		break;
	case roll::sized:
		if (!_file.is_open()) {
			_file.open(next_sized_file(msgsz), std::ios::out | std::ios::app);
		} else {
			if (_currfsz + msgsz > _fszlimit) {
				_file.close();
				_file.open(next_sized_file(msgsz), std::ios::out | std::ios::app);
			}
		}
		break;
	case roll::daily:
		if (!_file.is_open()) {
			_file.open(next_daily_file(), std::ios::out | std::ios::app);
		} else {
			if (_currday != sys::time::now(sys::time::timeunit::mday)) {
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
	if (!sys::file::exist(_dir)) {
		sys::path::mkdirs(_dir);
	}

	return sys::path::mkpath(_dir, _name);
}

std::string file_printer::next_daily_file() {
	if (!sys::file::exist(_dir)) {
		sys::path::mkdirs(_dir);
	}

	return sys::path::mkpath(_dir, _name + "." + sys::time::now("%Y%m%d"));
}

std::string file_printer::next_sized_file(int msgsz) {
	//make log directory
	if (!sys::file::exist(_dir)) {
		sys::path::mkdirs(_dir);
	}

	//get next sized file path
	_currnum++;
	std::string fpath = sys::path::mkpath(_dir, str::format("%s.%d", _name.c_str(), _currnum));
	while (true) {
		if (sys::file::exist(fpath)) {
			size_t sz = 0;
			if (sys::file::size(fpath, sz) == 0 && sz + msgsz < _fszlimit) {
				_currfsz = sz;
				break;
			}

		} else {
			_currfsz = 0;
			break;
		}
		_currnum++;
		fpath = sys::path::mkpath(_dir, str::format("%s.%d", _name.c_str(), _currnum));
	}

	return fpath;
}
END_CUBE_LOG_NS