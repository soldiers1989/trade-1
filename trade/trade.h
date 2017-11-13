#pragma once
#define DLLAPI __declspec(dllexport)

DLLAPI int __stdcall load(const char* dllpath, const char* account);

DLLAPI void __stdcall open();
DLLAPI void __stdcall close();

DLLAPI int __stdcall login(const char* ip, unsigned short port, const char* version, unsigned short deptid, const char* login_account, const char* trade_account, const char* trade_password, const char* communicate_password, char* error);
DLLAPI void __stdcall logout(int client_id);

DLLAPI void __stdcall query_data(int client_id, int category, char* result, char* error);
DLLAPI void __stdcall query_datas(int client_id, int categories[], int count, char* results[], char* errors[]);
DLLAPI void __stdcall query_history_data(int client_id, int category, char* start_date, char* end_date, char* result, char* error);

DLLAPI void __stdcall send_order(int client_id, int category, int price_type, char* equity_account, char* stock_code, float price, int quantity, char* result, char* error);
DLLAPI void __stdcall cancel_order(int client_id, char* exchange_id, char* delegate_num, char* result, char* error);

DLLAPI void __stdcall send_orders(int client_id, int categories[], int price_types[], char* equity_accounts[], char* stock_codes[], float prices[], int quantities[], int count, char* results[], char* errors[]);
DLLAPI void __stdcall cancel_orders(int client_id, char* exchange_ids[], char* delegate_nums[], int count, char* results[], char* errors[]);

DLLAPI void __stdcall get_quote(int client_id, char* stock_code, char* result, char* error);
DLLAPI void __stdcall get_quotes(int client_id, char* stock_codes[], int count, char* results[], char* errors[]);

DLLAPI void __stdcall repay(int client_id, char* amount, char* result, char* error);
