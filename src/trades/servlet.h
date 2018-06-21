#pragma once
#include "stdtrds.h"
#include "cube\http\servlet.h"
BEGIN_TRADES_NAMESPACE
class protocol {
public:
	static std::string ctype;
	static std::string resp(int status, const std::string &msg, const std::string &data = "");
};

class authority {
public:
	static bool allow(const std::string &ip);
};

class login : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class quote : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class querycurrent : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class queryhistory : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class order : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class cancel : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class logout : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};

class echo : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};
END_TRADES_NAMESPACE
