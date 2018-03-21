#pragma once
#include "cube\log\printer.h"
#include <mutex>
BEGIN_CUBE_LOG_NS
//log level option
enum class level { debug = 0, info = 1, warn = 2, error = 3, fatal = 4 };

//log output option
enum class output { console = 0, file = 1 };

//log class
class logger {
public:
	logger() : _level(level::debug), _printer(new console_printer()) { }
	~logger() {
		if (_printer != 0) {
			delete _printer;
			_printer = 0;
		}
	}

	/*
	*	log method with 5 level
	*@param format: message format
	*@return:
	*	void
	*/
	void debug(const char* format, ...);
	void info(const char* format, ...);
	void warn(const char* format, ...);
	void error(const char* format, ...);
	void fatal(const char* format, ...);

	/*
	*	print message to output
	*/
	void print(level lvl, const char *msg);

public:
	/*
	*	set log output level option, less than specified level will filter out
	*@param lvl: in, level output
	*@return:
	*	void
	*/
	void set(level lvl);

	/*
	*	set log output printer, directory/name/cut method must be specified if output is file, file size limit
	*must be specified if output is file and cut method is size limit.
	*@param out: in, output method, file or console
	*@param dir: in, log file directory
	*@param name: in, log file name
	*@param ropt: in, log file roll method, none, size or daily
	*@param fszlimit: in, file size limit if cut method is size cutting
	*@return:
	*	void
	*/
	void set(output out, const char *dir = ".", const char *name = "log", roll ropt = roll::none, uint fszlimit = -1);

private:
	//output printer for log
	printer *_printer;

	//mutex for log
	std::mutex _mutex;

	//level option
	level _level;
};
END_CUBE_LOG_NS

