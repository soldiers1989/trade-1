#pragma once
#include <string>
#include <fstream>
#include "cube\type.h"
#include "cube\file.h"

BEGIN_CUBE_NAMESPACE
class file: public std::fstream {
public:
	file(){}
	file(const char* filename, std::ios_base::openmode mode = std::ios_base::in | std::ios_base::out):std::fstream(filename, mode){}
	virtual ~file() {}
			
};
END_CUBE_NAMESPACE
