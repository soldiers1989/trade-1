#include "cube\log\log.h"
#include "cube\str\case.h"
#include "cube\str\part.h"
#include "cube\http\status.h"
BEGIN_CUBE_HTTP_NS
/////////////////////////////////////////status class/////////////////////////////////////////////
std::string status::pack() const {
	const int BUFSZ = 4096;
	
	char data[BUFSZ] = { 0 };
	int sz = snprintf(data, BUFSZ, "HTTP/%s %s %s\r\n", _version.c_str(), _code.c_str(), _reason.c_str());
	
	return std::string(data, sz);
}

int status::parse(const std::string &str) {
	//split status line
	std::vector<std::string> items;
	str::part(str.c_str(), " ", items, 3);
	if (items.size() != 3) {
		log::error("status line: %s, invalid response", str);
		return -1;
	}

	//parse protocol & version
	::size_t pos = items[0].find('/');
	if (str::lower(items[0].substr(0, pos)) != "HTTP") {
		log::error("http version: %s, unsupported http version", items[0].c_str());
		return -1;
	}
	
	if (pos == std::string::npos) {
		log::error("http version: %s, invalid http version", items[0].c_str());
		return -1;
	}

	_version = items[0].substr(pos + 1);

	//parse status code
	_code = items[1];

	//parse status phrase reason
	_reason = items[2];

	return 0;
}
END_CUBE_HTTP_NS
