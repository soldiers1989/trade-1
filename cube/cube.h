#pragma once
#include <string>
#define BEGIN_CUBE_NAMESPACE namespace cube{
#define END_CUBE_NAMESPACE }

#define BEGIN_NET_NAMESPACE namespace net{
#define END_NET_NAMESPACE }

#define BEGIN_TCP_NAMESPACE namespace tcp{
#define END_TCP_NAMESPACE }

#define BEGIN_HTTP_NAMESPACE namespace http{
#define END_HTTP_NAMESPACE }

#define BEGIN_IOS_NAMESPACE namespace cube { namespace ios {
#define END_IOS_NAMESPACE }}

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

template <class V> void safe_append(V *dest, const V &val) {
	if (dest != 0) {
		dest->append(val);
	}
}

template<class T> void throw_assign(std::string *dest, const std::string &val) {
	if (dest != 0) {
		*dest = val;
	} else {
		throw T(val.c_str());
	}
}

template <class T, class V> void safe_push(T *dest, const V &val) {
	if (dest != 0) {
		dest->push_back(val);
	}
}

template<class T> void safe_delete(T *&ptr) {
	if (ptr != 0) {
		delete ptr;
		ptr = 0;
	}
}

//cube exception
class cexception : public std::exception{
public:
	cexception() : _msg("unkown exception") {}
	explicit cexception(const char *format, ...);
	virtual ~cexception() {}

	char const* what() const;

public:
	std::string _msg;
};
END_CUBE_NAMESPACE
