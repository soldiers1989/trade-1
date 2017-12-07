#pragma once
#include <string>
#define BEGIN_CUBE_NAMESPACE namespace cube{
#define END_CUBE_NAMESPACE }

BEGIN_CUBE_NAMESPACE
typedef unsigned char byte;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;
typedef __int64	int64;
typedef unsigned __int64 uint64;

template <class T> void safe_assign(T *dest, const T &val) {
	if (dest != 0) {
		*dest = val;
	}
}
END_CUBE_NAMESPACE
