/*
*	os - operating system module
*/
#pragma once
#include "cube.h"

BEGIN_CUBE_NAMESPACE
class os {
public:
	static std::string last_error();
	static std::string last_error(int error_code);
};
END_CUBE_NAMESPACE
