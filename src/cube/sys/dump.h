#pragma once
#include <string>
#include "cube\ns.h"
#include <Windows.h>

BEGIN_CUBE_SYS_NS
class dump {
public:
	static void setup(const char *name = "cube");

	static LONG WINAPI dump_handler(LPEXCEPTION_POINTERS lps);

private:
	static std::string _name;
};
END_CUBE_SYS_NS




