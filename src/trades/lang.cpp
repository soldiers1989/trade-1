#include "trades\lang.h"
#include "cube\str\conv.h"
BEGIN_TRADES_NAMESPACE
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


int lang::process(trade::table &result, const trade::table &tbl) {
	//no need to convert
	if (_codepage == CODEPAGE) {
		result = tbl;
		return 0;
	}

	//convert every items
	for (std::size_t i = 0; i < tbl.size(); i++) {
		std::vector<std::string> row;
		for (std::size_t j = 0; j < tbl[i].size(); j++) {
			std::string newstr("");
			if (cube::str::iconv(newstr, tbl[i][j], CODEPAGE, _codepage) != 0) {
				return -1;
			}
			row.push_back(newstr);
		}
		result.push_back(row);
	}

	return 0;
}

bool lang::needconv() {
	if (_codepage == CODEPAGE) {
		return false;
	}
	return true;
}
END_TRADES_NAMESPACE
