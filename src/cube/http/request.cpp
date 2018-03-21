#include "cube\safe.h"
#include "cube\log\log.h"
#include "cube\str\part.h"
#include "cube\str\case.h"
#include "cube\str\format.h"
#include "cube\http\request.h"
BEGIN_CUBE_HTTP_NS

std::string request::pack() const {
	std::string res("");

	//pack query
	res.append(_query.pack());

	//pack headers
	res.append(_headers.pack());

	//pack empty line
	res.append("\r\n");

	return res;
}

int request::parse(const std::string &str) {
	//find request line seperator
	std::size_t pos = str.find("\r\n");
	if (pos == std::string::npos) {
		log::error("parse request failed.");
		return -1;
	}

	std::string squery = str.substr(0, pos);
	std::string sheaders = str.substr(pos + 2);

	//parse query
	if (_query.parse(squery) != 0)
		return -1;

	//parse headers
	if (_headers.parse(sheaders) != 0)
		return -1;

	return 0;
}
END_CUBE_HTTP_NS
