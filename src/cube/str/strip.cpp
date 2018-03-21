#include "cube\str\strip.h"
BEGIN_CUBE_STR_NS
std::string strip(const char* str, const char* packs/* = SPACES*/) {
	const char* lpos = 0, *rpos = 0, *pos = str;
	//strip left packs
	while (*pos != 0) {
		if (::strchr(packs, *pos) == 0)
			break;
		pos++;
	}
	if (*pos == 0)
		return std::string("");
	lpos = pos;

	//strip right packs
	pos++;
	while (*pos != 0) {
		if (::strchr(packs, *pos) == 0)
			rpos = pos;
		pos++;
	}

	return std::string(lpos, rpos - lpos + 1);
}

std::string strip(const std::string &str, const char* packs/* = SPACES*/) {
	return strip(str.c_str(), str.length(), packs);
}

std::string strip(const char *str, int len, const char* packs/* = SPACES*/) {
	int lpos = 0, rpos = len - 1;
	while (lpos < len) {//strip left packs
		if (::strchr(packs, *(str + lpos)) != 0)
			lpos++;
		else
			break;
	}
	if (lpos == len)
		return "";

	while (rpos > -1) {//strip right packs
		if (::strchr(packs, *(str + rpos)) != 0)
			rpos--;
		else
			break;
	}

	return std::string(str + lpos, rpos - lpos + 1);
}

std::string lstrip(const char* str, const char* packs/* = SPACES*/) {
	//strip left packs
	while (*str != 0) {
		if (::strchr(packs, *str) != 0)
			str++;
		else
			break;
	}

	return std::string(str);
}

std::string lstrip(const std::string &str, const char* packs/* = SPACES*/) {
	return lstrip(str.c_str(), str.length(), packs);
}

std::string lstrip(const char *str, int len, const char* packs/* = SPACES*/) {
	int lpos = 0;
	while (lpos < len) {//strip left packs
		if (::strchr(packs, *(str + lpos)) != 0)
			lpos++;
		else
			break;
	}

	if (lpos < len)
		return std::string(str + lpos, len - lpos);

	return std::string("");
}

std::string rstrip(const char* str, const char* packs/* = SPACES*/) {
	const char* pos = str, *rpos = 0;
	while (*pos != 0) {//strip right packs
		if (::strchr(packs, *pos) == 0)
			rpos = pos;
		pos++;
	}
	return std::string(str, rpos - str + 1);
}

std::string rstrip(const std::string &str, const char* packs/* = SPACES*/) {
	return rstrip(str.c_str(), str.length(), packs);
}

std::string rstrip(const char *str, int len, const char* packs/* = SPACES*/) {
	int rpos = len - 1;
	while (rpos > -1) {//strip right packs
		if (::strchr(packs, *(str + rpos)) != 0)
			rpos--;
		else
			break;
	}

	return std::string(str, rpos + 1);
}

END_CUBE_STR_NS
