#pragma once
#include <string>
#include "tdxexpt.h"

BEGIN_QUOTE_NAMESPACE
//tdx level-2 quote module configure
class tdxdll2cfg {
public:
	static const char* DLLDIR; //raw dll directory
	static const char* DLLNAME; //raw dll name
};

//tdx level-2 quote module api
class tdxdll2
{
public:
	tdxdll2() : _hmodule(0) {}
	~tdxdll2() {}

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
	TdxL2Hq_ConnectDelegate TdxL2Hq_Connect;
	TdxL2Hq_DisconnectDelegate TdxL2Hq_Disconnect;

	TdxL2Hq_GetDetailTransactionDataDelegate TdxL2Hq_GetDetailTransactionData;
	TdxL2Hq_GetDetailOrderDataDelegate TdxL2Hq_GetDetailOrderData;
	TdxL2Hq_GetSecurityQuotes10Delegate TdxL2Hq_GetSecurityQuotes10;
	TdxL2Hq_GetBuySellQueueDelegate TdxL2Hq_GetBuySellQueue;

	TdxL2Hq_GetSecurityCountDelegate TdxL2Hq_GetSecurityCount;
	TdxL2Hq_GetSecurityListDelegate TdxL2Hq_GetSecurityList;
	TdxL2Hq_GetSecurityBarsDelegate TdxL2Hq_GetSecurityBars;
	TdxL2Hq_GetIndexBarsDelegate TdxL2Hq_GetIndexBars;
	TdxL2Hq_GetMinuteTimeDataDelegate TdxL2Hq_GetMinuteTimeData;
	TdxL2Hq_GetHistoryMinuteTimeDataDelegate TdxL2Hq_GetHistoryMinuteTimeData;
	TdxL2Hq_GetTransactionDataDelegate TdxL2Hq_GetTransactionData;
	TdxL2Hq_GetHistoryTransactionDataDelegate TdxL2Hq_GetHistoryTransactionData;
	TdxL2Hq_GetSecurityQuotesDelegate TdxL2Hq_GetSecurityQuotes;
	TdxL2Hq_GetCompanyInfoCategoryDelegate TdxL2Hq_GetCompanyInfoCategory;
	TdxL2Hq_GetCompanyInfoContentDelegate TdxL2Hq_GetCompanyInfoContent;
	TdxL2Hq_GetXDXRInfoDelegate TdxL2Hq_GetXDXRInfo;
	TdxL2Hq_GetFinanceInfoDelegate TdxL2Hq_GetFinanceInfo;


private:
	//dll module
	void * _hmodule;

};
END_QUOTE_NAMESPACE
