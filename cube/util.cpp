#include "util.h"
#include <iomanip>
#include <iostream>

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

std::vector<std::string> util::splits(const std::string& str, const std::string& seps) {
	std::vector<std::string> result;

	int startpos = 0, endpos = 0, pos = 0;
	while (pos < (int)str.size()) {
		if (seps.find(str[pos]) != std::string::npos) {
			result.push_back(str.substr(startpos, pos - startpos));
			pos++;
			while (pos < (int)str.size()) {
				if (seps.find(str[pos] == std::string::npos)) {
					startpos = pos;
					break;
				}
				pos++;
			}
		}
		else
			pos++;
	}

	if (startpos < (int)str.size()) {
		result.push_back(str.substr(startpos));
	}

	return result;
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

char* util::fast_search(char* content, int content_length, const char* target, int target_length) {
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

char* util::slow_search(char* content, int content_length, const char* target, int target_length) {
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

char* util::search(char* content, int content_length, const char* target, int target_length, bool fast/* = true*/) {
	if (fast) {
		return util::fast_search(content, content_length, target, target_length);
	}
	else {
		return util::slow_search(content, content_length, target, target_length);
	}
}

int util::overwrite(char* data, int datalen, const char* src, int srclen, const char* dest, int destlen, char default/* = 0*/, bool onlyfirst/* = true*/) {
	//overwrite number
	int ownum = 0;

	while (data != 0 && datalen > 0) {
		//first search the source position in data
		char* pdata = util::search(data, datalen, src, srclen);
		if (destlen > srclen && (datalen - (pdata - data) < destlen))
			break;

		//overwrite with destination data
		if (destlen < srclen)
			memset(pdata, default, srclen);
		memcpy(pdata, dest, destlen);
		ownum++;

		if (onlyfirst)
			break;

		//next search from new position
		data = pdata + (destlen > srclen ? destlen : srclen);
		datalen = datalen - (destlen > srclen ? destlen : srclen);
	}	

	return ownum;
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

void util::print(const std::vector<std::vector<std::string>> &table, int colwidth) {
	for (size_t nrow = 0; nrow < table.size(); nrow++) {
		for (size_t ncol = 0; ncol < table[nrow].size(); ncol++) {
			std::cout <<std::setw(colwidth) << table[nrow][ncol].c_str();
		}
		std::cout << std::endl;
	}
}

END_CUBE_NAMESPACE
