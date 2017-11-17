#include "cube\str.h"
#include <string.h>
BEGIN_CUBE_NAMESPACE
std::vector<std::string> str::split(const char* str, const char sep) {
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


std::vector<std::string> str::split(const char* str, const char* sep) {
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

std::vector<std::string> str::split(const std::string& str, const char sep) {
	std::vector<std::string> result;

	std::size_t startpos = 0, endpos = str.find(sep, startpos);
	while (endpos != std::string::npos) {
		result.push_back(str.substr(startpos, endpos - startpos));
		startpos = endpos + 1;
		endpos = str.find(sep, startpos);
	}

	if (startpos < str.length()) {
		result.push_back(str.substr(startpos));
	}

	return result;
}

std::vector<std::string> str::split(const std::string& str, const std::string& sep) {
	std::vector<std::string> result;

	std::size_t startpos = 0, endpos = str.find(sep.c_str(), 0, sep.length());
	while (endpos != std::string::npos) {
		result.push_back(str.substr(startpos, endpos - startpos));
		startpos = endpos + sep.length();
		endpos = str.find(sep.c_str(), startpos, sep.length());
	}

	if (startpos < str.length()) {
		result.push_back(str.substr(startpos));
	}

	return result;
}
END_CUBE_NAMESPACE
