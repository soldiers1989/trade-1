/*
*	ds - data structure module
*/
#pragma once
#include "stdsvr.h"
#include <string>
BEGIN_SERVICE_NAMESPACE
//admin property
class admin_t {
public:
	admin_t() {}
	admin_t(const std::string &name, const std::string &user, const std::string &pwd, int role, bool disable) : id(-1), name(name), user(user), pwd(pwd), role(role), disable(disable), ctime(ctime), online(false) {}
	~admin_t() {}

	int id; //admin id
	std::string name; //admin name
	std::string user; //admin account
	std::string pwd; //admin password
	int role; //admin role
	bool disable;//disable status
	uint ctime; //create time
	bool online; //online status
};

//account's fee property
class fee_t {
public:
	fee_t() {}
	fee_t(float cfrate, float cflimit, float bfrate, float sfrate) : cfrate(cfrate), cflimit(cflimit), bfrate(bfrate), sfrate(sfrate) {}
	~fee_t() {}

	//commission fee rate
	float cfrate;
	//commission fee lower limit
	float cflimit;
	//buy in fee rate
	float bfrate;
	//sell out fee rate
	float sfrate;
};

//account's money property
class money_t {
public:
	money_t() {}
	money_t(float smoney, float lmoney) : smoney(smoney), lmoney(lmoney) {}
	~money_t() {}

	//start money
	float smoney;
	//left money
	float lmoney;
};

//account property class
class account_t {
public:
	account_t() {}
	account_t(const account_t &acnt) :
		id(acnt.id), broker(acnt.broker), admin(acnt.admin), name(acnt.name), user(acnt.user), pwd(acnt.pwd),
		smoney(acnt.smoney), lmoney(acnt.smoney), cfrate(acnt.cfrate), cflimit(acnt.cflimit), bfrate(acnt.bfrate),
		sfrate(acnt.sfrate), disable(acnt.disable), ctime(acnt.ctime), online(acnt.online) {
	}

	account_t(int broker, int admin, const std::string &name, const std::string &user, const std::string &pwd, float smoney, float lmoney, float cfrate, float cflimit, float bfrate, float sfrate, bool disable) :
		id(-1), broker(broker), admin(admin), name(name), user(user), pwd(pwd), smoney(smoney), lmoney(lmoney), cfrate(cfrate), cflimit(cflimit), bfrate(bfrate), sfrate(sfrate), disable(disable), ctime(0), online(false) {
	}

	account_t(int id, int broker, const std::string &name, const std::string &user, const std::string &pwd, float smoney, float lmoney, float cfrate, float cflimit, float bfrate, float sfrate, bool disable, uint ctime) :
		id(id), broker(broker), name(name), user(user), pwd(pwd), smoney(smoney), lmoney(lmoney), cfrate(cfrate), cflimit(cflimit), bfrate(bfrate), sfrate(sfrate), disable(disable), ctime(ctime), online(false) {
	}

	~account_t() {}

	//acccount id
	int id;
	//broker id
	int broker;
	//admin id
	int admin;
	//account name
	std::string name;
	//trade account
	std::string user;
	//trade account password
	std::string pwd;
	//start money
	float smoney;
	//left money
	float lmoney;
	//commission fee rate
	float cfrate;
	//commission fee lower limit
	float cflimit;
	//buy in fee rate
	float bfrate;
	//sell out fee rate
	float sfrate;
	//disable status
	bool disable;
	//account create time
	uint ctime;
	//online status
	bool online;
};

//broker department class
class dept {
public:
	dept(int id, const std::string &name, const std::string &code, bool disable, uint ctime) : id(id), code(code), name(name), disable(disable), ctime(ctime) {}
	dept(const std::string &name, const std::string &code) : name(name), code(code) {}
	dept() {}

	int id; //department id
	std::string code; //department code
	std::string name; //department name
	bool disable; //disable flag
	uint ctime; //create time
};

//broker's server class
class server {
public:
	//server type
	typedef enum class type { trade = 0, quote = 1 } type;

public:
	server(int id, const std::string &name, const std::string &host, ushort port, int stype, bool disable, uint ctime) : id(id), name(name), host(host), port(port), stype((type)stype), disable(disable), ctime(ctime) {}
	server(const std::string &name, const std::string &host, ushort port) : name(name), host(host), port(port) {}
	~server() {}

	int id; //server id
	std::string name; //server name
	std::string host; //host address, ip or domain name
	ushort port; //service port
	type stype; //server type;
	bool disable; //disable flag
	uint ctime; //create time
};

//broker property class
class broker_t {
public:
	broker_t() {}
	broker_t(const broker_t &brkr) : id(brkr.id), code(brkr.code), name(brkr.name), version(brkr.version), disable(brkr.disable), ctime(brkr.ctime) {}
	broker_t(const std::string &code, const std::string &name, const std::string &version, bool disable) : id(-1), code(code), name(name), version(version), disable(disable), ctime(0) {}
	broker_t(int id, const std::string &code, const std::string &name, const std::string &version, bool disable, uint ctime) : id(id), code(code), name(name), version(version), disable(disable), ctime(ctime) {}
	~broker_t() {}

	int id; //broker id
	std::string code; //broker code
	std::string name; //broker name
	std::string version; //client version
	bool disable; //disable flag
	uint ctime; //create time
};
END_SERVICE_NAMESPACE
