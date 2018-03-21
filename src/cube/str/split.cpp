#include "cube\str\split.h"
#include "cube\str\find.h"
BEGIN_CUBE_STR_NS
std::vector<std::string> split(const char *str, char ch) {
	std::vector<std::string> result;
	split(str, ch, result);
	return result;
}

void split(const char *str, char ch, std::vector<std::string> &result) {
	const char *start = str, *pos = str;
	while (*pos != 0) {
		if (*pos == ch) {
			result.push_back(std::string(start, pos - start));
			pos++;
			start = pos;
		} else {
			pos++;
		}
	}

	result.push_back(std::string(start, pos - start));
}

std::vector<std::string> split(const char *str, int sz, char ch) {
	std::vector<std::string> result;
	split(str, sz, ch, result);
	return result;
}

void split(const char *str, int sz, char ch, std::vector<std::string> &result) {
	const char *start = str, *pos = str;
	while (pos - str < sz) {
		if (*pos == ch) {
			result.push_back(std::string(start, pos - start));
			pos++;
			start = pos;
		} else {
			pos++;
		}
	}

	result.push_back(std::string(start, pos - start));
}

std::vector<std::string> split(const char *str, const char *sep) {
	std::vector<std::string> result;
	split(str, sep, result);
	return result;
}

void split(const char *str, const char *sep, std::vector<std::string> &result) {
	int seplen = (int)::strlen(sep);
	const char *start = str, *end = ::strstr(start, sep);
	while (end != 0) {
		result.push_back(std::string(start, end - start));
		start = end + seplen;
		end = ::strstr(start, sep);
	}
	//last split string
	result.push_back(std::string(start));
}

std::vector<std::string> split(const char *str, int sz, const char *sep) {
	std::vector<std::string> result;
	split(str, sz, sep, result);
	return result;
}

void split(const char *str, int sz, const char *sep, std::vector<std::string> &result) {
	int seplen = (int)::strlen(sep);
	const char *start = str, *end = find(start, sz, sep);
	while (end != 0) {
		result.push_back(std::string(start, end - start));
		start = end + seplen;
		end = find(start, sz - (start - str), sep);
	}
	//last split string
	result.push_back(std::string(start));
}

std::vector<std::vector<std::string>> split(const std::string &str, const std::string &seprow, const std::string &sepcol) {
	std::vector<std::vector<std::string>> table;
	split(str, seprow, sepcol, table);
	return table;
}

void split(const std::string &str, const std::string &seprow, const std::string &sepcol, std::vector<std::vector<std::string>> &result) {
	std::vector<std::string> rows = split(str.c_str(), seprow.c_str());
	for (int i = 0; i < (int)rows.size(); i++) {
		std::vector<std::string> cols = split(rows[i].c_str(), sepcol.c_str());
		result.push_back(cols);
	}
}
END_CUBE_STR_NS