#pragma once
#include <string>
#include "trader.h"
#include "tdxapi.h"

#define TDX_BATCH_LIMIT 20

class tdx : public trader
{
public:
	tdx();
	virtual ~tdx();

public:
	virtual int init(std::string ip, unsigned short port, std::string version, int deptid);

	virtual int login(std::string account, std::string password, std::string &error);

	virtual int query(ccategory_t category, table_t &result, std::string &error);

	virtual int query(std::vector<ccategory_t> categories, std::vector<table_t> &results, std::vector<std::string> &errors);

	virtual int query(hcategory_t category, std::string start_date, std::string end_date, table_t &result, std::string &error);

	virtual int send(order_t order, table_t &result, std::string& error);

	virtual int send(ocategory_t category, price_t type, std::string gddm, std::string zqdm, float price, int count, table_t &result, std::string& error);

	virtual int send(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string> &errors);

	virtual int cancel(order_t order, table_t &result, std::string& error);

	virtual int cancel(std::string seid, std::string orderno, table_t &result, std::string& error);

	virtual int cancel(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string>& errors);

	virtual int quote(std::string stock, table_t &result, std::string& error);

	virtual int quote(std::vector<std::string> stocks, std::vector<table_t> &results, std::vector<std::string>& errors);

	virtual int repay(std::string amount, table_t &result, std::string& error);

	virtual int logout();

	virtual int destroy();

private:
	//remote trade server ip
	std::string _ip;
	//remote trader server port
	unsigned short _port;
	//department id
	int _deptid;
	//client verion
	std::string _verion;

	//account name
	std::string _account;
	//account password
	std::string _password;

private:
	//trade api using tdx
	tdxapi *_tdxapi;

	//client id after login
	int _client_id;

	//result holder
	char *_results[TDX_BATCH_LIMIT];

	//error holder
	char *_errors[TDX_BATCH_LIMIT];
};
