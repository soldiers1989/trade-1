#pragma once
#include "stdtrd.h"
#include "tdxexpt.h"
BEGIN_TRADE_NAMESPACE
//tdx dll error message
class tdxdllerr {
public:
	static const char* ERR_INIT_DLL;
};

//tdx dll module configure
class tdxdllcfg {
public:
	static const char* RAWDLL_DIR; //raw dll directory
	static const char* RAWDLL_NAME; //raw dll name

	static const char* NEWDLL_DIR; //new dll directory
};

//tdx dll module api
class tdxdll
{
public:
	tdxdll() {}
	~tdxdll() {}

	/*
	*	load tdx trade dll module
	*@param workdir: in, dll path of tdx trade module
	*@param account: in, security account used to initialize the dll module
	*@param error: out, save the error message when something wrong happened and error is not null
	*@return:
	*	0 for success, otherwise <0
	*/
	int load(const std::string &workdir, const std::string &account, std::string *error = 0);

	/*
	*	free tdx quote dll module
	*@return:
	*	always 0
	*/
	int free();

public:
	////////////////api export by dll module/////////////////////////
	//normal api
	OpenTdxDelegate OpenTdx;
	CloseTdxDelegate CloseTdx;
	LogonDelegate Logon;
	LogoffDelegate Logoff;
	QueryDataDelegate QueryData;
	SendOrderDelegate SendOrder;
	CancelOrderDelegate CancelOrder;
	GetQuoteDelegate GetQuote;
	RepayDelegate Repay;

	//batch api
	QueryDatasDelegate QueryDatas;
	QueryHistoryDataDelegate QueryHistoryData;
	SendOrdersDelegate SendOrders;
	CancelOrdersDelegate CancelOrders;
	GetQuotesDelegate GetQuotes;

private:
	//module of dll
	void * _hmodule = 0;

private:
	/*
	*	create a new dll for account by raw dll
	*@param account: account of stock exchange
	*@param rawdll: raw dll path of tdx
	*@param newdll: new dll path of tdx for input account
	*@return:
	*	0--success, otherwise for failure
	*/
	static int create_newdll(const std::string& account, const std::string& rawdll, const std::string& newdll);

	/*
	*	encrypt account
	*@param account: in, security account
	*@return:
	*	encrypted string of input account
	*/
	static std::string encrypt_account(const std::string& account);
};
END_TRADE_NAMESPACE
