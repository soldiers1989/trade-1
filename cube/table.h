#pragma once
#include <vector>
#include "cube\ns.h"

BEGIN_CUBE_NAMESPACE
class table
{
public:	
	static std::vector<std::vector<std::string>> load(const char *data, const char *seprow, const char *sepcol);
};
END_CUBE_NAMESPACE
