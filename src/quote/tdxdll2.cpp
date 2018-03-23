#include <Windows.h>
#include "quote\tdxdll2.h"
#include "cube\safe.h"
#include "cube\sys\file.h"
#include "cube\sys\path.h"
#include "cube\sys\error.h"

BEGIN_QUOTE_NAMESPACE
const char* tdxdll2cfg::DLLDIR = "dll\\raw";
const char* tdxdll2cfg::DLLNAME = "TdxL2HqApi.dll";

int tdxdll2::load(const std::string &workdir, std::string *error/* = 0*/) {
	//first load dll module
	std::string dllfile = cube::sys::path::mkpath(workdir, cube::sys::path::mkpath(tdxdll2cfg::DLLDIR, tdxdll2cfg::DLLNAME));
	_hmodule = LoadLibrary(dllfile.c_str());
	if (_hmodule == NULL) {
		cube::safe_assign<std::string>(error, cube::sys::last_error());
		return -1;
	}

	//load api from dll module
	TdxL2Hq_Connect = (TdxL2Hq_ConnectDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_Connect");
	TdxL2Hq_Disconnect = (TdxL2Hq_DisconnectDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_Disconnect");

	TdxL2Hq_GetDetailTransactionData = (TdxL2Hq_GetDetailTransactionDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetDetailTransactionData");
	TdxL2Hq_GetDetailOrderData = (TdxL2Hq_GetDetailOrderDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetDetailOrderData");
	TdxL2Hq_GetSecurityQuotes10 = (TdxL2Hq_GetSecurityQuotes10Delegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetSecurityQuotes10");
	TdxL2Hq_GetBuySellQueue = (TdxL2Hq_GetBuySellQueueDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetBuySellQueue");

	TdxL2Hq_GetSecurityCount = (TdxL2Hq_GetSecurityCountDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetSecurityCount");
	TdxL2Hq_GetSecurityList = (TdxL2Hq_GetSecurityListDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetSecurityList");
	TdxL2Hq_GetSecurityBars = (TdxL2Hq_GetSecurityBarsDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetSecurityBars");
	TdxL2Hq_GetIndexBars = (TdxL2Hq_GetIndexBarsDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetIndexBars");
	TdxL2Hq_GetMinuteTimeData = (TdxL2Hq_GetMinuteTimeDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetMinuteTimeData");
	TdxL2Hq_GetHistoryMinuteTimeData = (TdxL2Hq_GetHistoryMinuteTimeDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetHistoryMinuteTimeData");
	TdxL2Hq_GetTransactionData = (TdxL2Hq_GetTransactionDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetTransactionData");
	TdxL2Hq_GetHistoryTransactionData = (TdxL2Hq_GetHistoryTransactionDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetHistoryTransactionData");
	TdxL2Hq_GetSecurityQuotes = (TdxL2Hq_GetSecurityQuotesDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetSecurityQuotes");
	TdxL2Hq_GetCompanyInfoCategory = (TdxL2Hq_GetCompanyInfoCategoryDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetCompanyInfoCategory");
	TdxL2Hq_GetCompanyInfoContent = (TdxL2Hq_GetCompanyInfoContentDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetCompanyInfoContent");
	TdxL2Hq_GetXDXRInfo = (TdxL2Hq_GetXDXRInfoDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetXDXRInfo");
	TdxL2Hq_GetFinanceInfo = (TdxL2Hq_GetFinanceInfoDelegate)GetProcAddress((HMODULE)_hmodule, "TdxL2Hq_GetFinanceInfo");

	return 0;
}

int tdxdll2::free() {
	if (_hmodule != 0) {
		FreeModule((HMODULE)_hmodule);
		_hmodule = 0;
	}
	return 0;
}
END_QUOTE_NAMESPACE