#pragma once

typedef void(__stdcall* func_open)();
typedef void(__stdcall* func_close)();

typedef int(__stdcall* func_login)(const char* ip, unsigned short port, const char* version, unsigned short deptid, const char* login_account, const char* trade_account, const char* trade_password, const char* communicate_password, char* error);
typedef void(__stdcall* func_logout)(int client_id);

typedef void(__stdcall* func_query_data)(int client_id, int category, char* result, char* error);
typedef void(__stdcall* func_query_datas)(int client_id, int categories[], int count, char* results[], char* errors[]);
typedef void(__stdcall* func_query_history_data)(int client_id, int category, const char* start_date, const char* end_date, char* result, char* error);

typedef void(__stdcall* func_send_order)(int client_id, int category, int price_type, const char* equity_account, const char* stock_code, float price, int quantity, char* result, char* error);
typedef void(__stdcall* func_cancel_order)(int client_id, const char* exchange_id, const char* delegate_num, char* result, char* error);
typedef void(__stdcall* func_send_orders)(int client_id, int categories[], int price_types[], const char* equity_accounts[], const char* stock_codes[], float prices[], int quantities[], int count, char* results[], char* errors[]);
typedef void(__stdcall* func_cancel_orders)(int client_id, const char* exchange_ids[], const char* delegate_nums[], int count, char* results[], char* errors[]);

typedef void(__stdcall* func_get_quote)(int client_id, const char* stock_code, char* result, char* error);
typedef void(__stdcall* func_get_quotes)(int client_id, const char* stock_codes[], int count, char* results[], char* errors[]);

typedef void(__stdcall* func_repay)(int client_id, const char* amount, char* result, char* error);
