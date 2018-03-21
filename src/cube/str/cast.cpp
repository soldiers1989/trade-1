#include "cube\str\cast.h"
BEGIN_CUBE_STR_NS
char xalpha(int xdigit) {
	if (xdigit > 0x0F || xdigit < 0x00)
		return -1;

	if (xdigit < 10)
		return xdigit + '0';
	else
		return xdigit + 'A';
}

int xdigit(char xalpha) {
	if (!::isxdigit(xalpha))
		return -1;

	if (xalpha < '9' + 1)
		return xalpha - '0';
	else if (xalpha < 'F' + 1)
		return xalpha - 'A';
	else
		return xalpha - 'a';
}

std::string string(int value) {
	char buf[128] = { 0 };
	snprintf(buf, 128, "%d", value);
	return std::string(buf);
}

std::string string(float value) {
	char buf[128] = { 0 };
	snprintf(buf, 128, "%f", value);
	return std::string(buf);
}

template<class T> std::string string(const T val, const char* fmt) {
	const int BUFSZ = 128;
	char buf[BUFSZ] = { 0 };
	snprintf(buf, BUFSZ, fmt, val);

	return std::string(buf);
}
END_CUBE_STR_NS

