#pragma once
#include <string>
#define BEGIN_CUBE_NAMESPACE namespace cube{
#define END_CUBE_NAMESPACE }

BEGIN_CUBE_NAMESPACE
typedef unsigned char byte;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;

template <class T> void safe_assign(T *dest, const T &val) {
	if (dest != 0) {
		*dest = val;
	}
}

class sys {
public:
	static std::string getlasterror();
	static std::string geterrormsg(int code);
};
END_CUBE_NAMESPACE
