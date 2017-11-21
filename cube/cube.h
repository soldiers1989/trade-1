#pragma once
#include <string>
#define BEGIN_CUBE_NAMESPACE namespace cube{
#define END_CUBE_NAMESPACE }

BEGIN_CUBE_NAMESPACE
class sys {
public:
	static std::string getlasterror();
};
END_CUBE_NAMESPACE
