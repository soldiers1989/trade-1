#pragma once
#include "tdxdef.h"
#include <Windows.h>

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
	int load(const char* dllpath, const char* account);

	/*
	*	free module
	*@return
	*	0
	*/
	int free();

public:
	func_open open = NULL;
	func_close close = NULL;
	
	func_login login = NULL;
	func_logout logout = NULL;
	
	func_query_data query_data = NULL;
	func_query_datas query_datas = NULL;
	func_query_history_data query_history_data = NULL;

	func_send_order send_order = NULL;
	func_cancel_order cancel_order = NULL;
	func_send_orders send_orders = NULL;
	func_cancel_orders cancel_orders = NULL;

	func_get_quote get_quote = NULL;
	func_get_quotes get_quotes = NULL;

	func_repay repay = NULL;

private:
	//encrypt key for change dll relate with account
	char *generate_key(const char* account);

	//generate new dll
	char* generate_dll(const char* dllpath, const char* account);

	//load data from file
	char* read_file(const char* path, int &sz);

	//write data to file
	int write_file(const char* path, const char* content, int sz);

	//find byte
	char* find(char* src, int sz, const char* sub, int subsz);

	//module of dll
	HMODULE _hmodule = NULL;
};
