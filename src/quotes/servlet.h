#pragma once
#include "stdqots.h"
#include "cube\http\servlet.h"
BEGIN_QUOTES_NAMESPACE
class protocol {
public:
	static std::string succ(const std::string &msg, const std::string &data = "");
	static std::string fail(const std::string &msg, const std::string &data = "");
};

class authority {
public:
	static bool allow(const std::string &ip);
};

class connect : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class query_security_count : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class disconnect : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class echo : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};
END_QUOTES_NAMESPACE
