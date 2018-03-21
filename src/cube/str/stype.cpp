#include <cctype>
#include "cube\str\stype.h"
BEGIN_CUBE_STR_NS
bool empty(const char* str) {
	if (str != 0 && *str == 0) {
		return true;
	}
	return false;
}

bool isnum(const char* str) {
	return isdigit(str);
}

bool isdigit(const char* str) {
	while (*str != 0) {
		if (!::isdigit(*str))
			return false;
		str++;
	}
	return true;
}

bool isxdigit(const char* str) {
	while (*str != 0) {
		if (!::isxdigit(*str))
			return false;
		str++;
	}
	return true;
}

bool isalpha(const char* str) {
	while (*str != 0) {
		if (!::isalpha(*str))
			return false;
		str++;
	}
	return true;
}

bool isalnum(const char* str) {
	while (*str != 0) {
		if (!::isalnum(*str))
			return false;
		str++;
	}
	return true;
}

bool islower(const char* str) {
	while (*str != 0) {
		if (!::islower(*str))
			return false;
		str++;
	}
	return true;
}

bool isupper(const char* str) {
	while (*str != 0) {
		if (!::isupper(*str))
			return false;
		str++;
	}
	return true;
}

bool isfloat(const char* str) {
	bool hasdot = false;
	while (*str != 0) {
		if (!::isdigit(*str)) {
			if (!(*str == '.'))
				return false; //float only has number or '.'
			else {
				if (hasdot)
					return false; // too many dots
				hasdot = true;
			}
		}
		str++;
	}
	return true;
}
END_CUBE_STR_NS
