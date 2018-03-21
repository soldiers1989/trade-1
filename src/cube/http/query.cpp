#include "cube\log\log.h"
#include "cube\str\part.h"
#include "cube\http\query.h"
BEGIN_CUBE_HTTP_NS
std::string query::pack() const {
	const int BUFSZ = 4096;
	char data[BUFSZ] = { 0 };

	int sz = 0;
	if(_params.empty())
		sz = snprintf(data, BUFSZ, "%s %s HTTP/%s\r\n", _method.c_str(), _path.c_str(), _version.c_str());
	else
		sz = snprintf(data, BUFSZ, "%s %s?%s HTTP/%s\r\n", _method.c_str(), _path.c_str(), _params.pack().c_str(), _version.c_str());

	return std::string(data, sz);
}

int query::parse(const std::string &str) {
	std::vector<std::string> items;
	cube::str::part(str.c_str(), " ", items, 3);
	if (items.size() != 3) {
		log::error("query line: %s, invalid request", str);
		return -1;
	}

	//parse method
	_method = items[0];

	//parse query
	::size_t pos = items[1].find("?");
	if (pos == std::string::npos)
		_path = items[1];
	else {
		_path = items[1].substr(0, pos);
		if(_params.parse(items[1].substr(pos + 1)) != 0)
			return -1;
	}

	//parse protocol & version
	pos = items[2].find('/');
	if (pos == std::string::npos) {
		log::error("http version: %s, invalid http version", items[2].c_str());
		return -1;
	}
	_version = items[2].substr(pos + 1);
	
	return 0;
}
END_CUBE_HTTP_NS
