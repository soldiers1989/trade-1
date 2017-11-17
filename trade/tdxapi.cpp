#include "tdxapi.h"
#include "tdxdll.h"
#include <Windows.h>

tdxapi::tdxapi() : _hmodule(0) {

}

tdxapi::~tdxapi() {
	if (_hmodule != 0) {
		::FreeLibrary((HMODULE)_hmodule);
	}
}

int tdxapi::load(const std::string& account, const std::string& rawdll) {
	//generate new dll name
	std::string newdll = dllname(account, rawdll);

	//create new dll by account and raw dll
	int ret = tdxdll::create(account, rawdll, newdll);
	if (ret != 0) {
		return -1;
	}

	//load module first
	HMODULE hmodule = ::LoadLibrary(newdll.c_str());
	if (hmodule == NULL) {
		return -1;
	}
	
	//load functions from module
	open = (func_open)GetProcAddress(hmodule, "OpenTdx");
	close = (func_close)GetProcAddress(hmodule, "CloseTdx");
	login = (func_login)GetProcAddress(hmodule, "Logon");
	logout = (func_logout)GetProcAddress(hmodule, "Logoff");
	
	query_data = (func_query_data)GetProcAddress(hmodule, "QueryData");
	query_datas = (func_query_datas)GetProcAddress(hmodule, "QueryDatas");
	query_history_data = (func_query_history_data)GetProcAddress(hmodule, "QueryHistoryData");

	send_order = (func_send_order)GetProcAddress(hmodule, "SendOrder");
	cancel_order = (func_cancel_order)GetProcAddress(hmodule, "CancelOrder");
	send_orders = (func_send_orders)GetProcAddress(hmodule, "SendOrders");
	cancel_orders = (func_cancel_orders)GetProcAddress(hmodule, "CancelOrders");

	get_quote = (func_get_quote)GetProcAddress(hmodule, "GetQuote");
	get_quotes = (func_get_quotes)GetProcAddress(hmodule, "GetQuotes");
	
	repay = (func_repay)GetProcAddress(hmodule, "Repay");

	// save module handle
	_hmodule = hmodule;

	return 0;
}

std::string tdxapi::dllname(const std::string& account, const std::string& rawdll) {
	return rawdll+"."+account+".dll";
}
