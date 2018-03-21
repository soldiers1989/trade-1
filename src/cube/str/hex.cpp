#include "cube\str\hex.h"
#include "cube\str\cast.h"
BEGIN_CUBE_STR_NS
std::string hex(int val) {
	return hex((const byte*)&val, sizeof(int));
}

std::string hex(char val) {
	return hex((const byte*)&val, sizeof(char));
}

std::string hex(short val) {
	return hex((const byte*)&val, sizeof(short));
}

std::string hex(long val) {
	return hex((const byte*)&val, sizeof(long));
}

std::string hex(long long val) {
	return hex((const byte*)&val, sizeof(long long));
}

std::string hex(const byte *data, int sz) {
	std::string res("");
	for (int i = 0; i < sz; i++) {
		res.append(1, xalpha((*(data + i) & 0xF0)) >> 4);
		res.append(1, xalpha((*(data + i) & 0x0F)));
	}
	return res;
}

std::string hex(const std::string &data) {
	return hex((const byte*)data.data(), data.length());
}


char octet(char high, char low) {
	return (char)(xdigit(high) << 4 | xdigit(low));
}

std::string octet(const std::string &str) {
	return octet(str.c_str(), str.length());
}

std::string octet(const char* str) {
	std::string res("");
	while (*str != 0 && *(str + 1) != 0) {
		if (!::isxdigit(*str) || !::isdigit(*(str + 1)))
			return ""; //input string is invalid
		res.append(1, (char)(xdigit(*str) << 4 | xdigit(*(str + 1))));

		str += 2;
	}

	if (*str != 0)
		return ""; // string length must be multiple of 2

	return res;

}

std::string octet(const char* str, int len) {
	/*must be multiple of 2*/
	if (len % 2 != 0)
		return ""; //input string's length invalid

	std::string res("");
	for (int i = 0; i < len; i++) {
		if (!::isxdigit(*(str + i)) || !::isdigit(*(str + i + 1)))
			return ""; //input string is invalid
		res.append(1, (char)(xdigit(*(str + i)) << 4 | xdigit(*(str + i + 1))));
	}

	return res;
}

END_CUBE_STR_NS
