#include "str.h"
#include <locale>
#include <cstdarg>

BEGIN_CUBE_NAMESPACE
str::str()
{
}


str::~str()
{
}

bool str::isnum(const char* str)
{
	return str::isdigit(str);
}

bool str::isdigit(const char* str)
{
	while (*str != 0)
	{
		if (!::isdigit(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isxdigit(const char* str)
{
	while (*str != 0)
	{
		if (!::isxdigit(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isalpha(const char* str)
{
	while (*str != 0)
	{
		if (!::isalpha(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isalnum(const char* str)
{
	while (*str != 0)
	{
		if (!::isalnum(*str))
			return false;
		str++;
	}
	return true;
}

bool str::islower(const char* str)
{
	while (*str != 0)
	{
		if (!::islower(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isupper(const char* str)
{
	while (*str != 0)
	{
		if (!::isupper(*str))
			return false;
		str++;
	}
	return true;
}

bool str::isfloat(const char* str)
{
	bool hasdot = false;
	while (*str != 0)
	{
		if (!::isdigit(*str))
		{
			if (! *str=='.' )
				return false; //float only has number or '.'
			else
			{
				if (hasdot)
					return false; // too many dots
				hasdot = true;
			}
		}
		str++;
	}
	return true;
}

std::string str::lower(const std::string &str)
{
	std::string res("");
	for (size_t i = 0; i<str.length(); i++)
		res.append(1, (char)tolower(str[i]));
	return res;
}

std::wstring str::lower(const std::wstring &str)
{
	std::wstring res(L"");
	for (size_t i = 0; i<str.length(); i++)
		res.append(1, (wchar_t)tolower(str[i]));
	return res;
}

std::string str::upper(const std::string &str)
{
	std::string res("");
	for (size_t i = 0; i<str.length(); i++)
		res.append(1, (char)toupper(str[i]));
	return res;
}

std::wstring str::upper(const std::wstring &str)
{
	std::wstring res(L"");
	for (size_t i = 0; i<str.length(); i++)
		res.append(1, (wchar_t)toupper(str[i]));
	return res;
}


char str::xalpha(int xdigit)
{
	if (xdigit > 0x0F || xdigit < 0x00)
		return -1;

	if (xdigit < 10)
		return xdigit + '0';
	else
		return xdigit + 'A';
}

int str::xdigit(char xalpha)
{
	if (!::isxdigit(xalpha))
		return -1;
	
	if (xalpha < '9' + 1)
		return xalpha - '0';
	else if (xalpha < 'F' + 1)
		return xalpha - 'A';
	else
		return xalpha - 'a';
}

std::string str::hex(int val)
{
	return hex((const byte*)&val, sizeof(int));
}

std::string str::hex(char val)
{
	return hex((const byte*)&val, sizeof(char));
}

std::string str::hex(short val)
{
	return hex((const byte*)&val, sizeof(short));
}

std::string str::hex(long val)
{
	return hex((const byte*)&val, sizeof(long));
}

std::string str::hex(long long val)
{
	return hex((const byte*)&val, sizeof(long long));
}

std::string str::hex(const byte *data, int sz)
{
	std::string res("");
	for (int i = 0; i < sz; i++)
	{
		res.append(1, xalpha((*(data + i) & 0xF0)) >> 4);
		res.append(1, xalpha((*(data + i) & 0x0F)));
	}
	return res;
}

std::string str::hex(const std::string &data)
{
	return hex((const byte*)data.data(), data.length());
}

char str::bytes(char high, char low)
{
	return (char)(xdigit(high) << 4 | xdigit(low));
}

std::string str::bytes(const char* str)
{
	std::string res("");
	while(*str != 0 && *(str+1) != 0)
	{
		if (!::isxdigit(*str) || !::isdigit(*(str + 1)))
			return ""; //input string is invalid
		res.append(1, (char)(xdigit(*str) << 4 | xdigit(*(str + 1))));

		str += 2;
	}

	if (*str != 0)
		return ""; // string length must be multiple of 2

	return res;

}

std::string str::bytes(const char* str, int len)
{
	/*must be multiple of 2*/
	if (len % 2 != 0)
		return ""; //input string's length invalid

	std::string res("");
	for (int i = 0; i < len; i++)
	{
		if (!::isxdigit(*(str + i)) || !::isdigit(*(str + i + 1)))
			return ""; //input string is invalid
		res.append(1, (char)(xdigit(*(str + i)) << 4 | xdigit(*(str + i + 1))));
	}

	return res;
}

std::string str::bytes(const std::string &str)
{
	return bytes(str.c_str(), str.length());
}

std::string str::strip(const char* str, const char* packs/* = SPACES*/)
{
	const char* lpos = 0, *rpos = 0, *pos = str;
	//strip left packs
	while (*pos != 0)
	{
		if (strchr(packs, *pos) == 0)
			break;
		pos++;
	}
	if (*pos == 0)
		return std::string("");
	lpos = pos;

	//strip right packs
	pos++;
	while (*pos != 0)
	{
		if (strchr(packs, *pos) == 0)
			rpos = pos;
		pos++;
	}

	return std::string(lpos, rpos - lpos + 1);
}


std::string str::strip(const std::string &str, const char* packs/* = SPACES*/)
{
	return strip(str.c_str(), str.length(), packs);
}

std::string str::strip(const char *str, int len, const char* packs/* = SPACES*/)
{
	int lpos = 0, rpos = len - 1;
	while (lpos < len)
	{//strip left packs
		if (strchr(packs, *(str + lpos)) != 0)
			lpos++;
		else
			break;
	}
	if (lpos == len)
		return "";

	while (rpos > -1)
	{//strip right packs
		if (strchr(packs, *(str + rpos)) != 0)
			rpos--;
		else
			break;
	}
	
	return std::string(str + lpos, rpos - lpos + 1);
}

std::string str::lstrip(const char* str, const char* packs/* = SPACES*/)
{
	//strip left packs
	while (*str != 0)
	{
		if (strchr(packs, *str) != 0)
			str++;
		else
			break;
	}
	
	return std::string(str);
}

std::string str::lstrip(const std::string &str, const char* packs/* = SPACES*/)
{
	return lstrip(str.c_str(), str.length(), packs);
}

std::string str::lstrip(const char *str, int len, const char* packs/* = SPACES*/)
{
	int lpos = 0;
	while (lpos < len)
	{//strip left packs
		if (strchr(packs, *(str + lpos)) != 0)
			lpos++;
		else
			break;
	}

	if (lpos < len)
		return std::string(str+lpos, len-lpos);

	return std::string("");
}

std::string str::rstrip(const char* str, const char* packs/* = SPACES*/)
{
	const char* pos = str, *rpos = 0;
	while (*pos != 0)
	{//strip right packs
		if (strchr(packs, *pos) == 0)
			rpos = pos;
		pos++;
	}
	return std::string(str, rpos - str + 1);
}

std::string str::rstrip(const std::string &str, const char* packs/* = SPACES*/)
{
	return rstrip(str.c_str(), str.length(), packs);
}

std::string str::rstrip(const char *str, int len, const char* packs/* = SPACES*/)
{
	int rpos = len - 1;
	while (rpos > -1)
	{//strip right packs
		if (strchr(packs, *(str + rpos)) != 0)
			rpos--;
		else
			break;
	}

	return std::string(str, rpos + 1);
}

std::string str::format(const char *format, ...)
{
	/*this buffer is properly not safe*/
	static const int BUFSZ = 1024;
	char buf[BUFSZ] = { 0 };

	va_list va;
	va_start(va, format);
	vsnprintf(buf, BUFSZ, format, va);	
	va_end(va);

	return std::string(buf);
}

std::string str::tostr(int value)
{
	char buf[128] = { 0 };
	sprintf(buf, "%d", value);
	return std::string(buf);
}

std::string str::tostr(float value)
{
	char buf[128] = { 0 };
	sprintf(buf, "%f", value);
	return std::string(buf);
}
END_CUBE_NAMESPACE
