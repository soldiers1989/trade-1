#include "http.h"
#include "str.h"
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

void params::_parse(const char *str, int sz) {
	return _parse(std::string(str, sz));
}

void params::_parse(const std::string &str) {
	std::vector<std::string> items = cube::str::split(str, '&');
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

std::string params::get(const std::string &key) {
	std::string val("");
	if (_params.find(key) == _params.end() || _params[key].empty())
		return val;

	return _params[key][0];
}

std::vector<std::string> params::gets(const std::string &key) {
	if (_params.find(key) == _params.end())
		return std::vector<std::string>();

	return _params[key];
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
	std::vector<std::string> items = cube::str::split(str,"\r\n");
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

void header::_parse(const char *str, int sz) {
	_parse(std::string(str, sz));
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

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
