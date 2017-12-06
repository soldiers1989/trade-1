/*
*	os - operating system module
*/
#pragma once
#include "cube.h"

BEGIN_CUBE_NAMESPACE
class os {
public:
	/*
	*	get last error
	*/
	static int last_error_code();
	static std::string last_error();
	static std::string last_error(int error_code);

	/*
	*	get cpu core number
	*/
	static int get_cpu_cores();
};
END_CUBE_NAMESPACE
