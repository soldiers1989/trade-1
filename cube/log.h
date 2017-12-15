#pragma once
#include "cube.h"
BEGIN_CUBE_NAMESPACE
class log {
public:
	static void debug(const char* format, ...);
	static void info(const char* format, ...);
	static void warn(const char* format, ...);
	static void error(const char* format, ...);
	static void fatal(const char* format, ...);
};
END_CUBE_NAMESPACE
