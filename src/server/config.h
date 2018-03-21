/*
*	config - configure access module
*/
#pragma once
#include "stdsvr.h"
#include "cube\ini.h"
BEGIN_SVR_NAMESPACE
BEGIN_MGR_NAMESPACE
class cfg {
public:
	//http service configure
	class chttp{
	public:
		chttp() : port(80) {}
		~chttp() {}

		ushort port;
	};

	//database configure
	class cdb{
	public:
		cdb() : host(""), user(""), pwd(""), name(""), port(3306) {}
		~cdb() {}

		std::string host;
		std::string user;
		std::string pwd;
		std::string name;
		ushort port;
	};
public:
	//load configure file
	static int load(const std::string &path);

public:
	//db configure
	static cfg::cdb db;
	//http configure
	static cfg::chttp http;
private:
	//ini file
	static cube::ini _ini;
};
END_MGR_NAMESPACE
END_SVR_NAMESPACE
