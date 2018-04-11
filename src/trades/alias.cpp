#include "trades\lang.h"
#include "trades\alias.h"
#include "cube\cfg\ini.h"
#include "cube\str\part.h"
BEGIN_TRADES_NAMESPACE
alias *alias::_inst = 0;
alias *alias::instance() {
	if (_inst == 0) {
		_inst = new alias();
	}
	return _inst;
}

int alias::load(const char *cfg) {
	//load configure
	cube::cfg::ini tmpcfg;
	if (tmpcfg.load(cfg) != 0) {
		_enabled = false;
		return -1;
	}

	//get alias section
	std::map<std::string, std::string> nalias = tmpcfg.items("alias");
	
	//inverse to alias->name
	std::map<std::string, std::string>::iterator iter = nalias.begin(), iterend = nalias.end();
	while (iter != iterend) {
		std::string name = iter->first;

		std::vector<std::string> alias = cube::str::part(iter->second.c_str(), " ");
		for (std::size_t i = 0; i < alias.size(); i++) {
			_alias[alias[i]] = name;
		}

		iter++;
	}

	//get need character encoding converting column names(after alias)
	std::string sconvs = tmpcfg.get_string_value("conv", "columns", "");
	if (!sconvs.empty()) {
		std::vector<std::string> vconvs = cube::str::part(sconvs.c_str(), " ");
		for (std::size_t i = 0; i < vconvs.size(); i++) {
			_convs[vconvs[i]] = vconvs[i];
		}
	}

	//set enabled flag
	_enabled = true;

	return 0;
}

/*
*	process table result by filter
*@param tbl: table data with table header as the first line
*@return:
*	filter result
*/
trade::table alias::process(const trade::table &tbl) {
	//process result
	trade::table result;

	//empty table
	if (tbl.size() == 0)
		return result;

	//filter result for column names
	std::vector<std::string> colnames;
	//filter result for column numbers(start with 0)
	std::vector<int> colnums;
	//columns need to convert charaset
	std::map<int, int> colconvs;

	//filter column by original names
	for (std::size_t i = 0; i < tbl[0].size(); i++) {
		std::map<std::string, std::string>::iterator iter = _alias.find(tbl[0][i]);
		if (iter != _alias.end()) {
			//new column names after alias convert
			colnames.push_back(iter->second);
			//keep columns after alias filter
			colnums.push_back(i);
			//column need to convert charset
			if (_convs.find(iter->second) != _convs.end())
				colconvs[i] = i;
		}
	}

	//all columns has filtered
	if (colnames.empty())
		return result;

	//set matched column names
	result.push_back(colnames);

	//extract matched column values
	for (std::size_t j = 1; j < tbl.size(); j++) {
		std::vector<std::string> col;
		for (std::size_t k = 0; k < colnums.size(); k++) {
			std::string val = tbl[j][colnums[k]];
			if (colconvs.find(colnums[k]) != colconvs.end()) {
				val = lang::instance()->conv(val);
			}
				
			col.push_back(val);
		}

		result.push_back(col);
	}

	return result;
}

bool alias::enabled() {
	return _enabled;
}

void alias::disable() {
	_enabled = false;
}
END_TRADES_NAMESPACE
