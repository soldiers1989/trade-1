#pragma once
#include "cube.h"
#include <mutex>
#include <fstream>
BEGIN_CUBE_NAMESPACE
class printer;

//log class
class log {
public:
	//log output option
	typedef enum out { console = 0, file = 1 } out;
	//cut option for file output 
	typedef enum cut { none = 0, size = 1, daily = 2 } cut;

	//log level option
	typedef enum level { debug = 0, info = 1, warn = 2, error = 3, fatal = 4 } level;

public:
	/*
	*	log method with 5 level
	*@param format: message format
	*@return:
	*	void
	*/
	static void debug(const char* format, ...);
	static void info(const char* format, ...);
	static void warn(const char* format, ...);
	static void error(const char* format, ...);
	static void fatal(const char* format, ...);

public:
	/*
	*	set log output level option, less than specified level will filter out
	*@param lvl: in, level output
	*@return:
	*	void
	*/
	static void set(level lvl);

	/*
	*	set log output printer, directory/name/cut method must be specified if output is file, file size limit 
	*must be specified if output is file and cut method is size limit.
	*@param out: in, output method, file or console
	*@param dir: in, log file directory
	*@param name: in, log file name
	*@param ct: in, log file cut method, none, size or daily
	*@param fszlimit: in, file size limit if cut method is size cutting
	*@return:
	*	void
	*/
	static void set(out out, const char *dir = 0, const char *name = 0, cut ct = cut::none, uint fszlimit = -1);

private:
	/*
	*	print message to output
	*/
	static void print(level lvl , const char *msg);

private:
	//output printer for log
	static printer *_printer;
	
	//mutex for log
	static std::mutex _mutex;

	//level option
	static level _level;
};

//printer class
class printer {
public:
	virtual void print(const char *msg) = 0;
};

//console printer class
class console_printer : public printer {
public:
	void print(const char *msg);
};

//file printer class
class file_printer : public printer {
public:
	file_printer(const std::string &dir, const std::string &name, log::cut ct = log::cut::none, uint fszlimit = -1);
	virtual ~file_printer();

	void print(const char *msg);

private:
	//cut file if need
	void check_and_cut(int msgsz);

	void open_sized_file();

	void open_daily_file();

	void open_normal_file();
private:
	//output file
	std::ofstream _file;

	//file directory
	std::string _dir;
	//file name prefix
	std::string _name;
	//cut option
	log::cut _cutopt;
	//file size limit for cutting file
	uint _fszlimit;
	//file number for sized cutting file
	int _num;
};
END_CUBE_NAMESPACE
