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

template <class V> void safe_assign(V *dest, const V &val) {
	if (dest != 0) {
		*dest = val;
	}
}

template <class T, class V> void safe_push(T *dest, const V &val) {
	if (dest != 0) {
		dest->push_back(val);
	}
}
END_CUBE_NAMESPACE
