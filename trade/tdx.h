#pragma once
#include "trade.h"
#include "tdxdll.h"

BEGIN_TRADE_NAMESPACE
class tdx : public trade
{
public:
	tdx();
	virtual ~tdx();

public:
	virtual int init(std::string account, std::string *error = 0);

	virtual int login(std::string ip, ushort port, std::string version, int deptid, std::string login_account, std::string trade_account, std::string trade_pwd, std::string communicate_pwd, std::string &error);
	
	virtual int query(ccategory_t category, table_t &result, std::string &error);

	virtual int query(std::vector<ccategory_t> categories, std::vector<table_t> &results, std::vector<std::string> &errors);

	virtual int query(hcategory_t category, std::string start_date, std::string end_date, table_t &result, std::string &error);

	virtual int send(ocategory_t category, pricetype_t type, std::string gddm, std::string zqdm, float price, int count, table_t &result, std::string& error);

	virtual int send(order_t order, table_t &result, std::string& error);

	virtual int send(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string> &errors);

	virtual int cancel(std::string exchangeid, std::string order_no, table_t &result, std::string& error);

	virtual int cancel(order_t order, table_t &result, std::string& error);

	virtual int cancel(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string>& errors);

	virtual int quote(std::string stock_code, table_t &result, std::string& error);

	virtual int quote(std::vector<std::string> stock_codes, std::vector<table_t> &results, std::vector<std::string>& errors);

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

	//dll module account limit
	std::string _dll_account;


	//login account name
	std::string _login_account;
	//trade account name
	std::string _trade_account;
	//trade password
	std::string _trade_pwd;
	//communicate password
	std::string _communicate_pwd;

private:
	//trade api using tdx
	tdxdll *_trade;

	//client id after login
	int _client_id;

	//result holder
	char *_results[TDX_BATCH_LIMIT];

	//error holder
	char *_errors[TDX_BATCH_LIMIT];
};
END_TRADE_NAMESPACE
