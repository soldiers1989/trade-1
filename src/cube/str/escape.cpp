#include "cube\str\hex.h"
#include "cube\str\escape.h"
BEGIN_CUBE_STR_NS
std::string escape(char ch) {
	std::string res("%");
	res.append(hex(ch));
	return res;
}

std::string escape(const char* str) {
	std::string res("");
	while (*str != 0) {
		if (isalnum(*str))
			res.append(1, *str);
		else
			res.append(escape(*str));
		str++;
	}
	return res;
}

std::string escape(const std::string &str) {
	return escape(str.c_str(), str.length());
}

std::string escape(const char *str, int len) {
	std::string res("");
	for (int i = 0; i < len; i++) {
		char ch = *(str + i);
		if (isalnum(ch))
			res.append(1, ch);
		else
			res.append(escape(ch));
	}
	return res;
}

std::string unescape(const char* str) {
	std::string res("");
	while (*str != 0) {
		if (*str == '%') {
			if (*(str + 1) != 0 && *(str + 2) != 0 && isxdigit(*(str + 1)) && isxdigit(*(str + 2))) {
				res.append(1, octet(*(str + 1), *(str + 2)));
				str += 3;
			} else
				return ""; //error input escaped string
		} else {
			res.append(1, *str);
			str++;
		}
	}
	return res;
}

std::string unescape(const std::string &str) {
	return unescape(str.c_str(), str.length());
}

std::string unescape(const char *str, int len) {
	std::string res("");
	for (int i = 0; i < len; ) {
		if (*(str + i) == '%') {
			if (*(str + i + 1) != 0 && *(str + i + 2) != 0 && isxdigit(*(str + i + 1)) && isxdigit(*(str + i + 2))) {
				res.append(1, octet(*(str + i + 1), *(str + i + 2)));
				i += 3;
			} else
				return ""; //error input escaped string
		} else {
			res.append(1, *(str + i));
			i++;
		}
	}
	return res;
}
END_CUBE_STR_NS
