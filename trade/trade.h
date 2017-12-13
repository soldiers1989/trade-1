#pragma once
#include "stdtrd.h"

BEGIN_TRADE_NAMESPACE

//table structure for holding the results for query from remote server
typedef std::vector<std::vector<std::string>> table;

class query {
public:
	//当前信息查询：0-资金 1-股份 2-当日委托 3-当日成交 4-可撤委托 5-股东代码 6-融资余额 7-融券余额 8-可融证券
	//历史信息查询：0 - 历史委托 1 - 历史成交 2 - 交割单
	typedef enum type{ zj = 0, gf = 1, drwt = 2, drcj = 3, kcwt = 4, gddm = 5, rzye = 6, rqye = 7, krzq = 8, lswt = 0, lscj = 1, jgd = 2, other = -1 } type;

};

class price {
public:
	//0上海限价委托 深圳限价委托 1(市价委托)深圳对方最优价格  2(市价委托)深圳本方最优价格  3(市价委托)深圳即时成交剩余撤销  4(市价委托)上海五档即成剩撤 深圳五档即成剩撤 5(市价委托)深圳全额成交或撤销 6(市价委托)上海五档即成转限价
	typedef enum type{ xjwt = 0, sjwt1 = 1, sjwt2 = 2, sjwt3 = 3, sjwt4 = 4, sjwt5 = 5, sjwt6 = 6, other = -1 } type;
};

//order class
class order {
public:
	//委托类型：0-买入 1-卖出  2-融资买入  3-融券卖出   4-买券还券   5-卖券还款  6-现券还券
	typedef enum type { buy = 0, sell = 1, rzmr = 2, rqmc = 3, mqhq = 4, mqhk = 5, xqhk = 6, other = -1 } type;

public:
	order(type t, std::string g, std::string z, price::type pt, float p, int ct) : otype(t), gddm(g), zqdm(z), ptype(pt), price(p), count(ct) {}
	~order() {}

	type otype; //委托类型
	std::string gddm; //股东代码
	std::string zqdm; //证券代码

	price::type ptype; //出价类型
	float price; //价格
	int count; //股数
};

//order result class
class orderres {
public:
	orderres(std::string exchangeid, std::string orderno) : exchangeid(exchangeid), orderno(orderno) {}
	~orderres() {}

	// response of send order
	std::string exchangeid;
	std::string orderno;
};

//exchange class
class exchange {
public:
	static char* SHENZHEN; //普通账户-深圳交易所
	static char* SHANGHAI; //普通账户-上海交易所
	static char* SHENZHENZS; //招商证券普通账户-深圳交易所
};

//trade interface
class trade
{
public:
	//trade exceptions
	typedef std::exception error;

public:
	/*
	*	initialize trade service
	*@param workdir: in, working directory
	*@param error: out, error message when failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int init(const std::string &workdir, std::string *error = 0) = 0;

	/*
	*	account login to the remote trading server
	*@param ip: in, remote trading server ip
	*@param port: in, remote trading server port
	*@param version: in, version of client
	*@param deptid: in, department of account belongs to
	*@param login_account: in, login account, may be the capital account or customer account of security broker
	*@param trade_account: in, trade account, usually same as the login account
	*@param trade_pwd: in, trade password
	*@param communicate_pwd: in, communication passowrd, usually same as the trade passowrd
	*@param error: out, error message when login failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int login(const std::string &ip, ushort port, const std::string &version, int deptid,
					  const std::string &login_account, const std::string &trade_account, const std::string &trade_pwd, const std::string &communicate_pwd, 
					  std::string *error = 0) = 0;

	/*
	*	query current trading data of account by specified data category
	*@param category: in, data category
	*@param result: out, query result
	*@param error: out, error message when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(query::type category, table &result, std::string *error = 0) = 0;
	
	/*
	*	query current trading data of accounts by specified data categories
	*@param categories: in, data categories
	*@param results: out, query results
	*@param errors: out, error messages when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(const std::vector<query::type> &categories, std::vector<table> &results, std::vector<std::string> *errors = 0) = 0;

	/*
	*	query history trading data of accounts by specified data categories
	*@param category: in, data category
	*@param results: out, query results
	*@param errors: out, error messages when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(query::type category, const std::string &start_date, const std::string &end_date, table &result, std::string *error = 0) = 0;

	/*
	*	send delegate order to remote server
	*@param order, order data with an order_t object
	*@param result: out, send order result
	*@param error: out, error message when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int send(order order, table &result, std::string *error = 0) = 0;

	/*
	*	send delegate order to remote server
	*@param category: in, order category
	*@param type: in, delegate price type
	*@param gddm: in, order's shareholder code
	*@param zqdm: in, order's stock code
	*@param price: in, delegate price
	*@param count: in, delegate count
	*@param result: out, send order result
	*@param error: out, error message when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int send(order::type category, price::type type, const std::string &gddm, const std::string &zqdm, float price, int count, table &result, std::string *error = 0) = 0;

	/*
	*	send delegate orders to remote server
	*@param orders, orders data
	*@param results: out, send order results
	*@param errors: out, error messages when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int send(const std::vector<order> &orders, std::vector<table> &results, std::vector<std::string> *errors = 0) = 0;

	/*
	*	cancel order by specified order object
	*@param order: in, order object
	*@param result: out, cancel result
	*@param error, out, error message when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(const orderres &order, table &result, std::string *error = 0) = 0;

	/*
	*	cancel order by specified order number
	*@param exchange_id: in, exchange id of the order sent
	*@param order_no: in, order number want to cancel
	*@param result: out, cancel result
	*@param error, out, error message when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(const std::string &exchangeid, const std::string &orderno, table &result, std::string *error = 0) = 0;

	/*
	*	cancel orders by specified order object
	*@param orders: in, orders object
	*@param results: out, cancel results
	*@param errors, out, error messages when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(const std::vector<orderres> &orders, std::vector<table> &results, std::vector<std::string> *errors = 0) = 0;

	/*
	*	get current quotation of specfied stock by stock code
	*@param code: in, stock code
	*@param result: out, quotation of stock
	*@param error: out, error message when get quotation failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int quote(const std::string &code, table &result, std::string *error = 0) = 0;
	
	/*
	*	get current quotation of specifed stocks
	*@param codes: in, stock codes
	*@param results: out, quotation of stocks
	*@param errors: out, error messages when get quotation failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int quote(const std::vector<std::string> &codes, std::vector<table> &results, std::vector<std::string> *errors = 0) = 0;

	/*
	*	repay the borrowing of securites margin trading
	*@param amount: in, repay money amount
	*@param result: out, repay result
	*@param error: out, error message when get repay failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int repay(const std::string &amount, table &result, std::string *error = 0) = 0;

	/*
	*	logout from remote service
	*@return:
	*	always 0
	*/
	virtual int logout() = 0;

	/*
	*	destroy the trade service
	*@return:
	*	always 0
	*/
	virtual int destroy() = 0;

public:
	//current support trading channel
	typedef enum class channel { tdx = 0 } channel;

	//create a new trading object by specified channel
	static channel _channel;
	static void select(channel chnl);
	static trade * __stdcall create();
};
END_TRADE_NAMESPACE
