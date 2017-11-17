#pragma once
#include <string>
#include "tdxdef.h"

class tdxapi {
public:
	tdxapi();
	virtual ~tdxapi();

	/*
	*	initialize tdx api, load moudle from dll and load the export api in the module
	*@param dllpath: dll file path for the module
	*@return
	*	0--on sucess, otherwise for failure
	*/
	int load(const std::string& account, const std::string& rawdll);

public:
	func_open open = 0;
	func_close close = 0;
	
	func_login login = 0;
	func_logout logout = 0;
	
	func_query_data query_data = 0;
	func_query_datas query_datas = 0;
	func_query_history_data query_history_data = 0;

	func_send_order send_order = 0;
	func_cancel_order cancel_order = 0;
	func_send_orders send_orders = 0;
	func_cancel_orders cancel_orders = 0;

	func_get_quote get_quote = 0;
	func_get_quotes get_quotes = 0;

	func_repay repay = 0;

private:
	//new dll name for account
	std::string dllname(const std::string& account, const std::string& rawdll);

	//module of dll
	void * _hmodule = 0;
};
