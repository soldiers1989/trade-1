// server.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "cube\str.h"

int main()
{
	const char* str = "\n\nabc\tedf\t\n\n123\t456\t";
	std::vector<std::string> result;

	result = cube::str::split(str, "\n");
	result = cube::str::split(str, '\n');
	result = cube::str::split(std::string(str), '\n');
	result = cube::str::split(std::string(str), std::string("\n"));

    return 0;
}

