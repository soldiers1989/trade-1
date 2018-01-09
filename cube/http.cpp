#include "http.h"
#include "str.h"
#include <algorithm>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//////////////////////////////////////////address class/////////////////////////////////////////
addr::addr(const std::string &str) {
	_parse(str);
}

addr::addr(const char *str, int sz) {
	_parse(str, sz);
}

addr* addr::parse(const std::string &str) {
	return new addr(str);
}

addr* addr::parse(const char* str, int sz) {
	return new addr(str, sz);
}

void addr::_parse(const std::string &str) {
	return _parse(str.c_str(), (int)str.length());
}

void addr::_parse(const char *str, int sz) {
	const char *start = str, *end = str + sz;
	
	//find seperator of host and port
	const char *pos = start;
	while (*pos != ':' && pos < end)
		pos++;

	if (*pos == ':') {
		_host = cube::str::strip(start, pos - start);
		std::string port = cube::str::strip(pos + 1, end - pos - 1);
		if (cube::str::isdigit(port.c_str())) {
			_port = (ushort)::atoi(port.c_str());
		}
	} else {
		//only host found
		_host = cube::str::strip(str);
	}
}

//////////////////////////////////////////parameters class/////////////////////////////////////////
params::params(const std::string &str) {
	_parse(str);
}

params::params(const char *str, int sz) {
	_parse(str, sz);
}

params* params::parse(const std::string &str) {
	return new params(str);
}

params* params::parse(const char* str, int sz) {
	return new params(str, sz);
}

void params::_parse(const std::string &str) {
	return _parse(str.c_str(), str.length());
}

void params::_parse(const char *str, int sz) {
	const char *SEP = "&";
	std::vector<std::string> items = cube::str::splits(str, sz, SEP);
	for (std::size_t i = 0; i < items.size(); i++) {
		std::size_t sep = items[i].find('=');
		if (sep != std::string::npos) {
			std::string key = cube::str::strip(items[i].substr(0, sep));
			std::string val = cube::str::strip(items[i].substr(sep + 1));
			if (!key.empty()) {
				//unescape key
				key = cube::str::unescape(key);

				if (_params.find(key) == _params.end()) {
					_params.insert(std::pair<std::string, std::vector<std::string>>(key, std::vector<std::string>()));
				}
				
				//unescape value
				val = cube::str::unescape(val);

				_params[key].push_back(val);
			}
		}
	}
}

std::string params::get(const std::string &key) const {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end() || citer->second.empty())
		return "";

	return citer->second[0];
}

std::vector<std::string> params::gets(const std::string &key) const {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end())
		return std::vector<std::string>();

	return citer->second;
}

//////////////////////////////////////////header class/////////////////////////////////////////
header::header(const std::string &str) {
	_parse(str);
}

header::header(const char *str, int sz) {
	_parse(str, sz);
}

header* header::parse(const std::string &str) {
	return new header(str);
}

header* header::parse(const char *str, int sz) {
	return new header(str, sz);
}

void header::_parse(const std::string &str) {
	_parse(str.c_str(), str.length());
}

void header::_parse(const char *str, int sz) {
	const char *SEP = "\r\n";
	std::vector<std::string> items = cube::str::split(str, sz, SEP);
	for (std::size_t i = 0; i < items.size(); i++) {
		std::size_t sep = items[i].find(':');
		if (sep != std::string::npos) {
			std::string key = cube::str::strip(items[i].substr(0, sep));
			std::string val = cube::str::strip(items[i].substr(sep + 1));
			if (!key.empty()) {
				if (_items.find(key) == _items.end()) {
					_items.insert(std::pair<std::string, std::vector<std::string>>(key, std::vector<std::string>()));
				}

				_items[key].push_back(val);
			}
		}
	}
}

//////////////////////////////////////////uri class/////////////////////////////////////////
uri::uri(const std::string &str) : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") {
	_parse(str);
}

uri::uri(const char *str, int sz) : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") {
	_parse(str, sz);
}

uri* uri::parse(const std::string &str) {
	return new uri(str);
}

uri* uri::parse(const char *str, int sz) {
	return new uri(str, sz);
}

void uri::_parse(const std::string &str) {
	return _parse(str.c_str(), (int)str.length());
}

void uri::_parse(const char *str, int sz) {
	const char *start = str, *end = str+sz;

	//skip head spaces
	while (::isspace(*start))
		start++;

	//skip end spaces
	while (::isspace(*end))
		end--;

	//input is spaces
	if (start > end) {
		return;
	}

	const char *pos = start;
	////parse scheme////
	//find scheme end flag
	while (*pos != ':' && pos < end)
		pos++;

	//save scheme if flag found
	if (*pos == ':') {
		_scheme = std::string(start, pos - start);
		start = ++pos;
	} else {
		pos = start;
	}


	////parse authority////
	//find authority start flag
	int slashnum = 0;
	while (slashnum != 2 && pos < end) {
		//skip space character
		if (::isspace(*pos)) {
			pos++;
			continue;
		}

		if (*pos == '/') {
			slashnum++;
			pos++;
		} else {
			//authority flag not found
			break;
		}
	}

	if (slashnum == 2) {
		//set authority start pos
		start = pos;

		//find authority end flag
		while (*pos != '/' && *pos != '?' && *pos != '#' && pos < end)
			pos++;

		//save authority
		_auth = std::string(start, pos - start);

		//reset start pos
		start = pos;
	} else {
		//authority flag not found, reset pos
		pos = start;
	}

	////parse path////
	if (*pos == '/' && pos < end) {
		//skip path start flag
		start = pos++;

		//find path end flag(query or fragment start flag)
		while (*pos != '?' && *pos != '#' && pos < end)
			pos++;

		//save path
		_path = std::string(start, pos - start);
	}

	////parse query////
	if (*pos == '?' && pos < end) {
		//skip query start flag
		start = ++pos;

		while (*pos != '#' && pos < end)
			pos++;

		//save query
		_query = std::string(start, pos - start);
	}

	////parse fragment////
	if (*pos == '#' && pos < end) {
		//skip fragment start flag
		start = ++pos;

		//save fragment
		_fragment = std::string(start, end - start);
	}
}

std::string uri::description() {
	return cube::str::format("scheme:%s\nauthority:%s\npath:%s\nquery:%s\nfragment:%s\n", _scheme.c_str(), _auth.c_str(), _path.c_str(), _query.c_str(), _fragment.c_str());
}

//////////////////////////////////////////request class/////////////////////////////////////////
bool request::feed(const char *data, int sz) {
	//seperator strings
	static const char *SEP_HEADER_END = "\r\n\r\n";
	static const int LEN_SEP_HEADER_END = 4;
	static const char *SEP_LINE = "\r\n";
	static const int LEN_SEP_LINE = 2;

	//append new data
	_data.append(data, sz);

	//check if header completed
	std::size_t pos_header_end = _data.find(SEP_HEADER_END);
	if (pos_header_end == std::string::npos)
		return false;
	
	/////header completed, try to parse request////
	//parse request line//
	std::size_t pos_request_line_end = _data.find(SEP_LINE);
	std::vector<std::string> reqs = cube::str::splits(_data.c_str(), pos_request_line_end, " ");
	if (reqs.size() != 3) {
		throw ebad("invalid request line");
	}
	_method = cube::str::lower(cube::str::strip(reqs[0]));
	_query = cube::str::strip(reqs[1]);
	_version = cube::str::strip(reqs[2]);
	
	//parse request uri//
	_uri._parse(_query);

	//parse header items//
	std::size_t pos_header_start = pos_request_line_end + LEN_SEP_LINE;
	_header._parse(_data.c_str() + pos_header_start, pos_header_end - pos_header_start);
	
	return true;
}
END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
