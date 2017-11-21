#include "util.h"

BEGIN_CUBE_NAMESPACE
std::vector<std::string> util::split(const char* str, const char sep) {
	std::vector<std::string> result;

	int lenstr = strlen(str);
	const char *start = str, *end = 0;
	while (start < str + lenstr) {
		end = strchr(start, sep);
		if (end != 0) {
			result.push_back(std::string(start, end - start));
			start = end + 1;
		}
		else
			break;
	}
	if (start < str + lenstr) {
		result.push_back(std::string(start, str + lenstr));
	}

	return result;
}


std::vector<std::string> util::split(const char* str, const char* sep) {
	std::vector<std::string> result;

	int lenstr = strlen(str), lensep = strlen(sep);
	const char *start = str, *end = 0;
	while (start < str + lenstr) {
		end = strstr(start, sep);
		if (end != 0) {
			result.push_back(std::string(start, end - start));
			start = end + lensep;
		}
		else
			break;
	}
	if (start < str + lenstr) {
		result.push_back(std::string(start, str + lenstr));
	}

	return result;
}

std::vector<std::string> util::split(const std::string& str, const char sep) {
	std::vector<std::string> result;

	std::size_t startpos = 0, endpos = str.find(sep, startpos);
	while (endpos != std::string::npos) {
		result.push_back(str.substr(startpos, endpos - startpos));
		startpos = endpos + 1;
		endpos = str.find(sep, startpos);
	}

	if (startpos != std::string::npos) {
		result.push_back(str.substr(startpos));
	}

	return result;
}

std::vector<std::string> util::split(const std::string& str, const std::string& sep) {
	std::vector<std::string> result;

	std::size_t startpos = 0, endpos = str.find(sep.c_str(), 0, sep.length());
	while (endpos != std::string::npos) {
		result.push_back(str.substr(startpos, endpos - startpos));
		startpos = endpos + sep.length();
		endpos = str.find(sep.c_str(), startpos, sep.length());
	}

	if (startpos != std::string::npos) {
		result.push_back(str.substr(startpos));
	}

	return result;
}

std::vector<std::vector<std::string>> util::split(const char *str, const char *seprow, const char *sepcol) {
	std::vector<std::vector<std::string>> table;

	std::vector<std::string> rows = util::split(str, seprow);
	for (int i = 0; i < (int)rows.size(); i++) {
		std::vector<std::string> cols = util::split(rows[i], sepcol);
		table.push_back(cols);
	}

	return table;
}

int util::max_same_prefix_and_postfix(const char* blk, int len) {
	int rptlen = 0;
	for (rptlen = len - 1; rptlen > 0; rptlen--) {
		bool same = true;
		for (int i = 0, j = len - rptlen; i < rptlen; i++, j++) {
			if (*(blk + i) != *(blk + j)) {
				same = false;
				break;
			}
		}

		if (same) {
			return rptlen;
		}
	}
	return 0;
}

char* util::fast_search(const char* content, int content_length, const char* target, int target_length) {
	int * next = new int[target_length];
	for (int sublen = 0; sublen < target_length; sublen++) {
		next[sublen] = util::max_same_prefix_and_postfix(target, sublen + 1) + 1;
	}

	int i = 0, j = 0;
	while (i < content_length - target_length + 1 && j < target_length) {
		for (j = 0; j < target_length; j++) {
			if (*(content + i + j) != *(target + j)) {
				i += next[j];
				break;
			}
		}
	}

	if (i < content_length - target_length) {
		return (char*)content + i;
	}

	return 0;
}

char* util::slow_search(const char* content, int content_length, const char* target, int target_length) {
	int i = 0, j = 0;
	for (i = 0; i < content_length - target_length + 1; i++) {
		for (j = 0; j < target_length; j++) {
			if (*(content + i + j) != *(target + j)) {
				break;
			}
		}
		if (j == target_length) {
			break;
		}
	}
	if (i < content_length - target_length + 1) {
		return (char*)(content + i);
	}

	return 0;
}

char* util::search(const char* content, int content_length, char* target, int target_length, bool fast/* = true*/) {
	if (fast) {
		return util::fast_search(content, content_length, target, target_length);
	}
	else {
		return util::slow_search(content, content_length, target, target_length);
	}
}

bool util::empty(const char* str) {
	if (str != 0 && *str == 0) {
		return true;
	}
	return false;
}

template<class T> std::string util::tostr(const T val, const char* fmt) {
	const int BUFSZ = 128;
	char buf[BUFSZ] = { 0 };
	sprintf_s(buf, BUFSZ, fmt, val);

	return std::string(buf);
}

END_CUBE_NAMESPACE
