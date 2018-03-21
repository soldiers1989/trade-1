#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_SYS_NS
int last_error_code();
std::string last_error();
std::string last_error(int error_code);
END_CUBE_SYS_NS
