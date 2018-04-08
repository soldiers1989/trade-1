#include <Windows.h>
#include "cube\str\conv.h"
BEGIN_CUBE_STR_NS
int iconv(std::string &dest, const std::string &src, uint fromcp, uint tocp) {
	//get wide char size of @src
	int wsz = ::MultiByteToWideChar(fromcp, 0, src.c_str(), src.length(), NULL, 0);
	if (wsz <= 0) {
		return -1;
	}

	//create wide char buffer
	wchar_t *wchs = new wchar_t[wsz];
	int tsz = ::MultiByteToWideChar(fromcp, 0, src.c_str(), src.length(), wchs, wsz);
	if (tsz != wsz) {
		delete []wchs;
		return -1;
	}

	//get target multi bytes size
	int msz = ::WideCharToMultiByte(tocp, 0, wchs, tsz, NULL, 0, NULL, NULL);
	if (msz <= 0) {
		delete[]wchs;
		return -1;
	}

	//create multi bytes buffer
	char *mchs = new char[msz];
	tsz = ::WideCharToMultiByte(tocp, 0, wchs, tsz, mchs, msz, NULL, NULL);
	if (tsz != msz) {
		delete[]wchs;
		delete[]mchs;
		return -1;
	}

	dest = std::string(mchs, tsz);

	delete[]wchs;
	delete[]mchs;
	return 0;
	
}

int iconv(std::string &dest, const std::string &src, const char *from, const char *to) {
	return -1;
}
END_CUBE_STR_NS
