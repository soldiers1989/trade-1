#include <Windows.h>
#include "tdxdll1.h"
#include "cube\os.h"

BEGIN_QUOTE_NAMESPACE
int tdxdll1::load(std::string path/* = "TdxHqApi.dll"*/, std::string *error/* = 0*/) {
	//first load dll module
	_hmodule = LoadLibrary(path.c_str());
	if (_hmodule == NULL) {
		if(error != 0)
			*error = cube::os::last_error();
		return -1;
	}

	//load api from dll module
	TdxHq_Connect = (TdxHq_ConnectDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_Connect");
	TdxHq_Disconnect = (TdxHq_DisconnectDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_Disconnect");
	TdxHq_GetSecurityCount = (TdxHq_GetSecurityCountDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetSecurityCount");
	TdxHq_GetSecurityList = (TdxHq_GetSecurityListDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetSecurityList");
	TdxHq_GetSecurityBars = (TdxHq_GetSecurityBarsDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetSecurityBars");
	TdxHq_GetIndexBars = (TdxHq_GetIndexBarsDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetIndexBars");
	TdxHq_GetMinuteTimeData = (TdxHq_GetMinuteTimeDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetMinuteTimeData");
	TdxHq_GetHistoryMinuteTimeData = (TdxHq_GetHistoryMinuteTimeDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetHistoryMinuteTimeData");
	TdxHq_GetTransactionData = (TdxHq_GetTransactionDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetTransactionData");
	TdxHq_GetHistoryTransactionData = (TdxHq_GetHistoryTransactionDataDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetHistoryTransactionData");
	TdxHq_GetSecurityQuotes = (TdxHq_GetSecurityQuotesDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetSecurityQuotes");
	TdxHq_GetCompanyInfoCategory = (TdxHq_GetCompanyInfoCategoryDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetCompanyInfoCategory");
	TdxHq_GetCompanyInfoContent = (TdxHq_GetCompanyInfoContentDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetCompanyInfoContent");
	TdxHq_GetXDXRInfo = (TdxHq_GetXDXRInfoDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetXDXRInfo");
	TdxHq_GetFinanceInfo = (TdxHq_GetFinanceInfoDelegate)GetProcAddress((HMODULE)_hmodule, "TdxHq_GetFinanceInfo");

	return 0;
}

int tdxdll1::free() {
	if (_hmodule != 0) {
		FreeModule((HMODULE)_hmodule);
		_hmodule = 0;
	}
	return 0;
}
END_QUOTE_NAMESPACE
