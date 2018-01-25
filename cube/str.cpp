#include "str.h"
#include <locale>
#include <cstdarg>
#include <iomanip>
#include <iostream>

BEGIN_CUBE_NAMESPACE
bool str::isnum(const char* str) {
	return str::isdigit(str);
}

bool str::isdigit(const char* str) {
	while (*str != 0) {
		if (!::isdigit(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isxdigit(const char* str) {
	while (*str != 0) {
		if (!::isxdigit(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isalpha(const char* str) {
	while (*str != 0) {
		if (!::isalpha(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isalnum(const char* str) {
	while (*str != 0) {
		if (!::isalnum(*str))
			return false;
		str++;
	}
	return true;
}

bool str::islower(const char* str) {
	while (*str != 0) {
		if (!::islower(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isupper(const char* str) {
	while (*str != 0) {
		if (!::isupper(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isfloat(const char* str) {
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

std::string str::lower(const std::string &str) {
	std::string res("");
	for (size_t i = 0; i < str.length(); i++)
		res.append(1, (char)tolower(str[i]));
	return res;
}

std::wstring str::lower(const std::wstring &str) {
	std::wstring res(L"");
	for (size_t i = 0; i < str.length(); i++)
		res.append(1, (wchar_t)tolower(str[i]));
	return res;
}

std::string str::upper(const std::string &str) {
	std::string res("");
	for (size_t i = 0; i < str.length(); i++)
		res.append(1, (char)toupper(str[i]));
	return res;
}

std::wstring str::upper(const std::wstring &str) {
	std::wstring res(L"");
	for (size_t i = 0; i < str.length(); i++)
		res.append(1, (wchar_t)toupper(str[i]));
	return res;
}


char str::xalpha(int xdigit) {
	if (xdigit > 0x0F || xdigit < 0x00)
		return -1;

	if (xdigit < 10)
		return xdigit + '0';
	else
		return xdigit + 'A';
}

int str::xdigit(char xalpha) {
	if (!::isxdigit(xalpha))
		return -1;

	if (xalpha < '9' + 1)
		return xalpha - '0';
	else if (xalpha < 'F' + 1)
		return xalpha - 'A';
	else
		return xalpha - 'a';
}

std::string str::hex(int val) {
	return hex((const byte*)&val, sizeof(int));
}

std::string str::hex(char val) {
	return hex((const byte*)&val, sizeof(char));
}

std::string str::hex(short val) {
	return hex((const byte*)&val, sizeof(short));
}

std::string str::hex(long val) {
	return hex((const byte*)&val, sizeof(long));
}

std::string str::hex(long long val) {
	return hex((const byte*)&val, sizeof(long long));
}

std::string str::hex(const byte *data, int sz) {
	std::string res("");
	for (int i = 0; i < sz; i++) {
		res.append(1, xalpha((*(data + i) & 0xF0)) >> 4);
		res.append(1, xalpha((*(data + i) & 0x0F)));
	}
	return res;
}

std::string str::hex(const std::string &data) {
	return hex((const byte*)data.data(), data.length());
}

char str::bytes(char high, char low) {
	return (char)(xdigit(high) << 4 | xdigit(low));
}

std::string str::bytes(const char* str) {
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

std::string str::bytes(const char* str, int len) {
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

std::string str::bytes(const std::string &str) {
	return bytes(str.c_str(), str.length());
}

std::string str::strip(const char* str, const char* packs/* = SPACES*/) {
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


std::string str::strip(const std::string &str, const char* packs/* = SPACES*/) {
	return strip(str.c_str(), str.length(), packs);
}

std::string str::strip(const char *str, int len, const char* packs/* = SPACES*/) {
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

std::string str::lstrip(const char* str, const char* packs/* = SPACES*/) {
	//strip left packs
	while (*str != 0) {
		if (::strchr(packs, *str) != 0)
			str++;
		else
			break;
	}

	return std::string(str);
}

std::string str::lstrip(const std::string &str, const char* packs/* = SPACES*/) {
	return lstrip(str.c_str(), str.length(), packs);
}

std::string str::lstrip(const char *str, int len, const char* packs/* = SPACES*/) {
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

std::string str::rstrip(const char* str, const char* packs/* = SPACES*/) {
	const char* pos = str, *rpos = 0;
	while (*pos != 0) {//strip right packs
		if (::strchr(packs, *pos) == 0)
			rpos = pos;
		pos++;
	}
	return std::string(str, rpos - str + 1);
}

std::string str::rstrip(const std::string &str, const char* packs/* = SPACES*/) {
	return rstrip(str.c_str(), str.length(), packs);
}

std::string str::rstrip(const char *str, int len, const char* packs/* = SPACES*/) {
	int rpos = len - 1;
	while (rpos > -1) {//strip right packs
		if (::strchr(packs, *(str + rpos)) != 0)
			rpos--;
		else
			break;
	}

	return std::string(str, rpos + 1);
}

char * str::strchr(char *str, int sz, int ch) {
	return (char*)::memchr(str, ch, sz);
}

const char * str::strchr(const char *str, int sz, int ch) {
	return (const char*)::memchr(str, ch, sz);
}

char *str::strstr(char *str, int sz, const char *substr) {
	char *pos = str;
	while (pos - str < sz) {
		char *ppos = pos;
		const char *spos = substr;
		while (*spos != 0 && ppos - str < sz && *ppos == *spos) {
			spos++;
			ppos++;
		}

		if (*spos == 0)
			return pos;
		else
			pos++;
	}

	return 0;
}

const char *str::strstr(const char *str, int sz, const char *substr) {
	const char *pos = str;
	while (pos - str < sz) {
		const char *spos = substr, *ppos = pos;
		while (*spos != 0 && ppos - str < sz && *ppos == *spos) {
			spos++;
			ppos++;
		}

		if (*spos == 0)
			return pos;
		else
			pos++;
	}

	return 0;
}

std::string str::format(const char *format, ...) {
	/*this buffer is properly not safe*/
	static const int BUFSZ = 1024;
	char buf[BUFSZ] = { 0 };

	va_list va;
	va_start(va, format);
	vsnprintf(buf, BUFSZ, format, va);
	va_end(va);

	return std::string(buf);
}

void str::format(std::string &result, const char *format, ...) {
	static const int BUFSZ = 1024;
	char buf[BUFSZ] = { 0 };

	va_list va;
	va_start(va, format);
	vsnprintf(buf, BUFSZ, format, va);
	va_end(va);

	result.assign(buf);
}

std::string str::tostr(int value) {
	char buf[128] = { 0 };
	sprintf(buf, "%d", value);
	return std::string(buf);
}

std::string str::tostr(float value) {
	char buf[128] = { 0 };
	sprintf(buf, "%f", value);
	return std::string(buf);
}

template<class T> std::string str::tostr(const T val, const char* fmt) {
	const int BUFSZ = 128;
	char buf[BUFSZ] = { 0 };
	sprintf_s(buf, BUFSZ, fmt, val);

	return std::string(buf);
}

bool str::empty(const char* str) {
	if (str != 0 && *str == 0) {
		return true;
	}
	return false;
}

void str::print(const std::vector<std::vector<std::string>> &table, int colwidth) {
	for (size_t nrow = 0; nrow < table.size(); nrow++) {
		for (size_t ncol = 0; ncol < table[nrow].size(); ncol++) {
			std::cout << std::setw(colwidth) << table[nrow][ncol].c_str();
		}
		std::cout << std::endl;
	}
}

std::vector<std::string> str::split(const char *str, char ch) {
	std::vector<std::string> result;
	split(str, ch, result);
	return result;
}

void str::split(const char *str, char ch, std::vector<std::string> &result) {
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

std::vector<std::string> str::split(const char *str, int sz, char ch) {
	std::vector<std::string> result;
	split(str, sz, ch, result);
	return result;
}

void str::split(const char *str, int sz, char ch, std::vector<std::string> &result) {
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

std::vector<std::string> str::split(const char *str, const char *sep) {
	std::vector<std::string> result;
	split(str, sep, result);
	return result;
}

void str::split(const char *str, const char *sep, std::vector<std::string> &result) {
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

std::vector<std::string> str::split(const char *str, int sz, const char *sep) {
	std::vector<std::string> result;
	split(str, sz, sep, result);
	return result;
}

void str::split(const char *str, int sz, const char *sep, std::vector<std::string> &result) {
	int seplen = (int)::strlen(sep);
	const char *start = str, *end = strstr(start, sz, sep);
	while (end != 0) {
		result.push_back(std::string(start, end - start));
		start = end + seplen;
		end = strstr(start, sz - (start - str), sep);
	}
	//last split string
	result.push_back(std::string(start));
}

std::vector<std::string> str::strtok(const char *str, const char *delimiters, int maxwant) {
	std::vector<std::string> result;
	strtok(str, delimiters, result, maxwant);
	return result;
}

void str::strtok(const char *str, const char *delimiters, std::vector<std::string> &result, int maxwant) {
	//clear result
	result.clear();

	//split string
	const char *start = str;
	while ((int)result.size() < maxwant-1) {
		//find first split start pos
		while (*start != 0 && ::strchr(delimiters, *start) != 0)
			start++;

		//find first split end pos
		if (*start != 0) {
			const char *end = start + 1;
			while (*end != 0 && ::strchr(delimiters, *end) == 0)
				end++;
			
			result.push_back(std::string(start, end - start));

			//continue next split
			if (*end != 0)
				start = end + 1;
			else {
				start = end;
				break;
			}
		} else {
			break;
		}
	}

	//push the end string
	while (*start != 0 && ::strchr(delimiters, *start) != 0)
		start++;
	if (*start != 0) {
		result.push_back(start);
	}
}

std::vector<std::string> str::strtok(const char *str, int sz, const char *delimiters, int maxwant) {
	std::vector<std::string> result;
	strtok(str, sz, delimiters, result, maxwant);
	return result;
}

void str::strtok(const char *str, int sz, const char *delimiters, std::vector<std::string> &result, int maxwant) {
	//clear result
	result.clear();

	//split string
	const char *start = str;
	while ((int)result.size() < maxwant-1) {
		//find first split start pos
		while (start - str < sz && ::strchr(delimiters, *start) != 0)
			start++;

		//find first split end pos
		if (start - str < sz) {
			const char *end = start + 1;
			while (end - str < sz && ::strchr(delimiters, *end) == 0)
				end++;
			result.push_back(std::string(start, end - start));

			//continue next split
			if (end - str < sz)
				start = end + 1;
			else {
				start = end;
				break;
			}
		} else {
			break;
		}
	}

	//push the end string
	while (start - str < sz && ::strchr(delimiters, *start) != 0)
		start++;
	if (start - str < sz) {
		result.push_back(std::string(start, sz - (start -str)));
	}
}

std::vector<std::vector<std::string>> str::split(const std::string &str, const std::string &seprow, const std::string &sepcol) {
	std::vector<std::vector<std::string>> table;
	split(str, seprow, sepcol, table);
	return table;
}

void str::split(const std::string &str, const std::string &seprow, const std::string &sepcol, std::vector<std::vector<std::string>> &result) {
	std::vector<std::string> rows = str::split(str.c_str(), seprow.c_str());
	for (int i = 0; i < (int)rows.size(); i++) {
		std::vector<std::string> cols = str::split(rows[i].c_str(), sepcol.c_str());
		result.push_back(cols);
	}
}

std::string str::escape(char ch) {
	std::string res("%");
	res.append(str::hex(ch));
	return res;
}

std::string str::escape(const char* str) {
	std::string res("");
	while (*str != 0) {
		if (::isalnum(*str))
			res.append(1, *str);
		else
			res.append(escape(*str));
		str++;
	}
	return res;
}

std::string str::escape(const std::string &str) {
	return escape(str.c_str(), str.length());
}

std::string str::escape(const char *str, int len) {
	std::string res("");
	for (int i = 0; i < len; i++) {
		char ch = *(str + i);
		if (::isalnum(ch))
			res.append(1, ch);
		else
			res.append(escape(ch));
	}
	return res;
}

std::string str::unescape(const char* str) {
	std::string res("");
	while (*str != 0) {
		if (*str == '%') {
			if (*(str + 1) != 0 && *(str + 2) != 0 && ::isxdigit(*(str + 1)) && ::isxdigit(*(str + 2))) {
				res.append(1, str::bytes(*(str + 1), *(str + 2)));
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

std::string str::unescape(const std::string &str) {
	return unescape(str.c_str(), str.length());
}

std::string str::unescape(const char *str, int len) {
	std::string res("");
	for (int i = 0; i < len; ) {
		if (*(str + i) == '%') {
			if (*(str + i + 1) != 0 && *(str + i + 2) != 0 && ::isxdigit(*(str + i + 1)) && ::isxdigit(*(str + i + 2))) {
				res.append(1, str::bytes(*(str + i + 1), *(str + i + 2)));
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

std::string str::random(int len) {
	//string set for peeking the random character
	const static std::string strset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

	//generate random string
	std::string randstr("");
	for (int i = 0; i < len; i++) {
		int pos = rand() % strset.length();
		randstr.append(1, strset[pos]);
	}

	return randstr;
}
END_CUBE_NAMESPACE
