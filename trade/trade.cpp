#include "stdafx.h"
#include "trade.h"
#include "tdxapi.h"

static tdxapi *_tdxapi = NULL;

int __stdcall load(const char* dllpath, const char* account) {
	_tdxapi = new tdxapi();
	return _tdxapi->load(dllpath, account);
}

void __stdcall open() {
	_tdxapi->open();
}

void __stdcall close() {
	_tdxapi->close();
}

int __stdcall login(const char* ip, unsigned short port, const char* version, unsigned short deptid, const char* login_account, const char* trade_account, const char* trade_password, const char* communicate_password, char* error){
	return _tdxapi->login(ip, port, version, deptid, login_account, trade_account, trade_password, communicate_password, error);
}

void __stdcall logout(int client_id) {
	_tdxapi->logout(client_id);
}

void __stdcall query_data(int client_id, int category, char* result, char* error) {
	_tdxapi->query_data(client_id, category, result, error);
}

void __stdcall query_datas(int client_id, int categories[], int count, char* results[], char* errors[]) {
	_tdxapi->query_datas(client_id, categories, count, results, errors);
}

void __stdcall query_history_data(int client_id, int category, char* start_date, char* end_date, char* result, char* error) {
	_tdxapi->query_history_data(client_id, category, start_date, end_date, result, error);
}

void __stdcall send_order(int client_id, int category, int price_type, char* equity_account, char* stock_code, float price, int quantity, char* result, char* error) {
	_tdxapi->send_order(client_id, category, price_type, equity_account, stock_code, price, quantity, result, error);
}

void __stdcall cancel_order(int client_id, char* exchange_id, char* delegate_num, char* result, char* error) {
	_tdxapi->cancel_order(client_id, exchange_id, delegate_num, result, error);
}

void __stdcall send_orders(int client_id, int categories[], int price_types[], char* equity_accounts[], char* stock_codes[], float prices[], int quantities[], int count, char* results[], char* errors[]) {
	_tdxapi->send_orders(client_id, categories, price_types, equity_accounts, stock_codes, prices, quantities, count, results, errors);
}

void __stdcall cancel_orders(int client_id, char* exchange_ids[], char* delegate_nums[], int count, char* results[], char* errors[]) {
	_tdxapi->cancel_orders(client_id, exchange_ids, delegate_nums, count, results, errors);
}

void __stdcall get_quote(int client_id, char* stock_code, char* result, char* error) {
	_tdxapi->get_quote(client_id, stock_code, result, error);
}

void __stdcall get_quotes(int client_id, char* stock_codes[], int count, char* results[], char* errors[]) {
	_tdxapi->get_quotes(client_id, stock_codes, count, results, errors);
}

void __stdcall repay(int client_id, char* amount, char* result, char* error) {
	_tdxapi->repay(client_id, amount, result, error);
}

