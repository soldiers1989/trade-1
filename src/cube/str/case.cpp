#include "cube\str\case.h"
BEGIN_CUBE_STR_NS
std::string lower(const std::string &str) {
	std::string res("");
	for (size_t i = 0; i < str.length(); i++)
		res.append(1, (char)tolower(str[i]));
	return res;
}

std::wstring lower(const std::wstring &str) {
	std::wstring res(L"");
	for (size_t i = 0; i < str.length(); i++)
		res.append(1, (wchar_t)tolower(str[i]));
	return res;
}

std::string upper(const std::string &str) {
	std::string res("");
	for (size_t i = 0; i < str.length(); i++)
		res.append(1, (char)toupper(str[i]));
	return res;
}

std::wstring upper(const std::wstring &str) {
	std::wstring res(L"");
	for (size_t i = 0; i < str.length(); i++)
		res.append(1, (wchar_t)toupper(str[i]));
	return res;
}
END_CUBE_STR_NS
