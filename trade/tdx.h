#pragma once
#include <string>
#include "trader.h"
#include "tdxapi.h"

class trade_server {
public:
	trade_server();
	trade_server(const std::string &ip, unsigned short port, const std::string& version, unsigned short deptid);
	virtual ~trade_server();

	void ip(const std::string& ip);
	void port(const unsigned short port);
	void version(const std::string& version);
	void deptid(const unsigned short deptid);

	const std::string& ip();
	unsigned short port();
	const std::string& version();
	unsigned short deptid();

private:
	std::string _ip;
	unsigned short _port;
	std::string _version;
	unsigned short _deptid;
};

class tdx : public trader
{
public:
	tdx(const char* account, const char* password);
	virtual ~tdx();

public:
	virtual int init();

	virtual int login();

	virtual int query(int category);

	virtual int logout();

	virtual int destroy();


private:


private:
	//trade api using tdx
	tdxapi *_tdxapi;

	//trade server information
	trade_server _server;

	//client id after login
	int _client_id;
};
