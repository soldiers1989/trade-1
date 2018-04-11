#include "quotes\lang.h"
#include "cube\str\conv.h"
BEGIN_QUOTES_NAMESPACE
lang* lang::_inst = 0;
int lang::CODEPAGE = 54936; //default character code is gb18030
std::string lang::CHARSET = "gbk";//default character set

lang* lang::instance() {
	if (_inst == 0) {
		_inst = new lang();
	}
	return _inst;
}

void lang::set(int codepage, const std::string &charset) {
	_codepage = codepage;
	_charset = charset;
}

std::string lang::conv(const std::string &src) {
	std::string dest("");
	if (cube::str::iconv(dest, src, CODEPAGE, _codepage) != 0) {
		return src;
	}

	return dest;
}

int lang::conv(std::string &dest, const std::string &src) {
	if (cube::str::iconv(dest, src, CODEPAGE, _codepage) != 0) {
		return -1;
	}

	return 0;
}

quote::table lang::process(const quote::table &tbl) {
	quote::table result;
	process(result, tbl);
	return result;
}

void lang::process(quote::table &result, const quote::table &tbl) {
	//no need to convert
	if (_codepage == CODEPAGE) {
		result = tbl;
		return;
	}

	//convert every items
	for (std::size_t i = 0; i < tbl.size(); i++) {
		std::vector<std::string> row;
		for (std::size_t j = 0; j < tbl[i].size(); j++) {
			row.push_back(conv(tbl[i][j]));
		}
		result.push_back(row);
	}
}

bool lang::needconv() {
	if (_codepage == CODEPAGE) {
		return false;
	}
	return true;
}

const std::string& lang::charset() {
	return instance()->_charset;
}
END_QUOTES_NAMESPACE
