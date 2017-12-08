#pragma once
#include <string>
#include "tdxexpt.h"

BEGIN_QUOTE_NAMESPACE
//tdx level-1 quote module configure
class tdxdll1cfg {
public:
	static const char* DLLDIR; //raw dll directory
	static const char* DLLNAME; //raw dll name
};

//tdx level-1 quote module api
class tdxdll1
{
public:
	tdxdll1() : _hmodule(0) {}
	~tdxdll1() {}

	/*
	*	load tdx quote dll module
	*@param workdir: in, working directory
	*@param error: out, save the error message when something wrong happened and error is not null
	*@return:
	*	0 for success, otherwise <0
	*/
	int load(const std::string &workdir, std::string *error = 0);

	/*
	*	free tdx quote dll module
	*@return:
	*	always 0
	*/
	int free();

public:
	////////////////api export by dll module/////////////////////////
	TdxHq_ConnectDelegate TdxHq_Connect;
	TdxHq_GetSecurityCountDelegate TdxHq_GetSecurityCount;
	TdxHq_GetSecurityListDelegate TdxHq_GetSecurityList;
	TdxHq_DisconnectDelegate TdxHq_Disconnect;
	TdxHq_GetSecurityBarsDelegate TdxHq_GetSecurityBars;
	TdxHq_GetIndexBarsDelegate TdxHq_GetIndexBars;
	TdxHq_GetMinuteTimeDataDelegate TdxHq_GetMinuteTimeData;
	TdxHq_GetHistoryMinuteTimeDataDelegate TdxHq_GetHistoryMinuteTimeData;
	TdxHq_GetTransactionDataDelegate TdxHq_GetTransactionData;
	TdxHq_GetHistoryTransactionDataDelegate TdxHq_GetHistoryTransactionData;
	TdxHq_GetSecurityQuotesDelegate TdxHq_GetSecurityQuotes;
	TdxHq_GetCompanyInfoCategoryDelegate TdxHq_GetCompanyInfoCategory;
	TdxHq_GetCompanyInfoContentDelegate TdxHq_GetCompanyInfoContent;
	TdxHq_GetXDXRInfoDelegate TdxHq_GetXDXRInfo;
	TdxHq_GetFinanceInfoDelegate TdxHq_GetFinanceInfo;

private:
	//dll module
	void * _hmodule;
};
END_QUOTE_NAMESPACE
