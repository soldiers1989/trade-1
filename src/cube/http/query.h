#pragma once
#include <string>
#include "cube\http\param.h"
BEGIN_CUBE_HTTP_NS
class query {
public:
	query() : _method(""), _path(""), _version("") {}
	virtual ~query() {}

	std::string pack() const;
	int parse(const std::string &str);

public:
	const std::string &method() const { return _method; }
	const std::string &path() const { return _path; }
	const http::params &params() const { return _params; }
	const std::string &version() const { return _version; }

private:
	//request method
	std::string _method;
	//request path
	std::string _path;
	//request params
	http::params _params;
	//request http version
	std::string _version;
};
END_CUBE_HTTP_NS
