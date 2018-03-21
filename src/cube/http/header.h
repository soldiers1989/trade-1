#pragma once
#include "cube\http\pair.h"
#include "cube\http\param.h"
BEGIN_CUBE_HTTP_NS
//field element
class element : public pair {
public:
	element() {}
	element(const std::string &name, const std::string &value) : pair(name, value) {}
	virtual ~element() {}

	std::string pack() const;
	int parse(const std::string &str);

public:
	http::params &params() { return _params; }

private:
	//parameter of element
	http::params _params;
};

//header field
class header : public pair {
public:
	header() {}
	header(const std::string &name, const std::string &value) : pair(name, value) {}
	virtual ~header() {}

	std::string pack() const;
	int parse(const std::string &str);

public:
	bool operator==(const header &header) const;
	bool operator==(const std::string &name) const;
};

//http header
class headers {
public:
	headers() {}
	virtual ~headers() {}

	std::string pack() const;
	int parse(const std::string &str);

public:
	std::string get(const std::string &name) const;
	std::string get(const std::string &name, const char *default) const;
	std::vector<std::string> gets(const std::string &name) const;

	void add(const std::string &name, const std::string &value);
	void set(const std::string &name, const std::string &value);
private:
	std::vector<header> _headers;
};
END_CUBE_HTTP_NS
