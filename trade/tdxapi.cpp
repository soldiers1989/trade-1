#include "stdafx.h"
#include "tdxapi.h"
#include <stdio.h>
#include <fcntl.h>
#include <io.h>

tdxapi::tdxapi() {

}

tdxapi::~tdxapi() {

}

int tdxapi::load(const char* dllpath, const char* account) {
	//create new dll
	char* newdll = generate_dll(dllpath, account);

	//load module first
	_hmodule = ::LoadLibrary(newdll);
	delete []newdll;

	if (_hmodule == NULL) {
		return -1;
	}
	
	//load functions from module
	open = (func_open)GetProcAddress(_hmodule, "OpenTdx");
	close = (func_close)GetProcAddress(_hmodule, "CloseTdx");
	login = (func_login)GetProcAddress(_hmodule, "Logon");
	logout = (func_logout)GetProcAddress(_hmodule, "Logoff");
	
	query_data = (func_query_data)GetProcAddress(_hmodule, "QueryData");
	query_datas = (func_query_datas)GetProcAddress(_hmodule, "QueryDatas");
	query_history_data = (func_query_history_data)GetProcAddress(_hmodule, "QueryHistoryData");

	send_order = (func_send_order)GetProcAddress(_hmodule, "SendOrder");
	cancel_order = (func_cancel_order)GetProcAddress(_hmodule, "CancelOrder");
	send_orders = (func_send_orders)GetProcAddress(_hmodule, "SendOrders");
	cancel_orders = (func_cancel_orders)GetProcAddress(_hmodule, "CancelOrders");

	get_quote = (func_get_quote)GetProcAddress(_hmodule, "GetQuote");
	get_quotes = (func_get_quotes)GetProcAddress(_hmodule, "GetQuotes");
	
	repay = (func_repay)GetProcAddress(_hmodule, "Repay");

	return 0;
}

int tdxapi::free() {
	BOOL res = ::FreeLibrary(_hmodule);
	if (!res) {
		return -1;
	}
	return 0;
}

char* tdxapi::generate_key(const char* account) {
	//get the account string length
	int len = (int)strlen(account);

	//result of encrypt
	int pos = 0;
	char* result = new char[len + 2];
	memset(result, 0, len + 2);

	//encrypt every char in odd position of account string
	unsigned short salt = 0x055E;
	for (int i = 0; i < len; i += 2) {
		int c = (int)account[i] ^ (salt >> 8);
		salt = (unsigned short)(0x207F * (salt + c) - 0x523D);

		bool flag = true;
		for (int j = (int)'A'; j <= (int)'Z'&&flag; j++) {
			for (int k = (int)'Z'; k >= (int)'A'&&flag; k--) {
				int temp = 0x06DB + c - k;
				if (temp % 26 == 0 && temp / 26 == j) {
					result[pos] = (char)j;
					pos += 1;
					result[pos] = (char)k;
					pos += 1;

					flag = false;
				}
			}
		}
	}

	return result;
}

char* tdxapi::generate_dll(const char* dllpath, const char* account) {
	//geneate new dll path
	const char* dllpostfix = ".dll";
	int sz = strlen(dllpath) + strlen(account) + strlen(dllpostfix) + 1;
	char* newdll = new char[sz];
	memset(newdll, 0, sz);

	//set the new dll path
	memcpy(newdll, dllpath, strlen(dllpath));
	memcpy(newdll + strlen(newdll), account, strlen(account));
	memcpy(newdll + strlen(newdll), dllpostfix, strlen(dllpostfix));

	//check if new dll is exists
	if (_access(newdll, 0) == 0) {
		return newdll;
	}

	//key for account
	char* key = generate_key(account);

	//load dll to memory
	int fsz = 0;
	char *content = read_file(dllpath, fsz);
	
	//target string to be replaced
	const char* targetstr = "CCHOGIBI";

	//replace target string with key
	char *pos = find(content, fsz, targetstr, strlen(targetstr));
	memcpy(pos, key, strlen(key));
	
	//write to new dll
	write_file(newdll, content, fsz);

	delete []content;

	return newdll;
}

//load data from file
char* tdxapi::read_file(const char* path, int &sz) {
	FILE* fp = NULL;
	fopen_s(&fp, path, "rb");
	sz = _filelength(_fileno(fp));

	char* content = new char[sz];

	fread(content, sizeof(char), sz, fp);

	fclose(fp);
	return content;

}

//write data to file
int tdxapi::write_file(const char* path, const char* content, int sz) {
	FILE* fp = NULL;
	fopen_s(&fp, path, "wb");

	fwrite(content, sizeof(char), sz, fp);

	fclose(fp);

	return 0;
}

char *tdxapi::find(char* src, int sz, const char* sub, int subsz) {
	for (int i = 0; i < sz; i++) {
		if (memcmp(src + i, sub, subsz) == 0) {
			return src + i;
		}
	}

	return 0;
}