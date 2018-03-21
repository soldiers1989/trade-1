#pragma once
#include "cube\log\logger.h"
BEGIN_CUBE_LOG_NS
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
END_CUBE_LOG_NS