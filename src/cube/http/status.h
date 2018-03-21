#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_HTTP_NS
class status {
public:
	status() : _version("1.1"), _code(""), _reason("") {}
	status(const std::string &code, const std::string &reason) : _version("1.1"), _code(code), _reason(reason) {}
	status(const std::string &version, const std::string &code, const std::string &reason) : _version(version), _code(code), _reason(reason) {}
	virtual ~status() {}

	std::string pack() const;
	int parse(const std::string &str);

public:
	const std::string &code() const { return _code; }
	void code(const std::string &code) { _code = code; }

	const std::string& version() const { return _version; }
	void version(const std::string &version) { _version = version; }

	const std::string& reason() const { return _reason; }
	void reason(const std::string &reason) {_reason = reason;}

private:
	//response code
	std::string _code;
	//response description
	std::string _reason;
	//http version
	std::string _version;
};

static const status status_200_ok("200", "OK");
static const status status_301_moved_permanently("301", "Moved Permanently");
static const status status_302_found("302", "Found");
static const status status_400_bad_request("400", "Bad Request");
static const status status_401_unauthorized("401", "Unauthorized");
static const status status_403_forbidden("403", "Forbidden");
static const status status_404_not_found("404", "Not Found");
static const status status_405_method_not_allowed("405", "Method Not Allowed");
static const status status_500_interval_server_error("500", "Interval Server Error");
static const status status_505_http_version_not_supported("505", "Http Version Not Supportted");

END_CUBE_HTTP_NS
