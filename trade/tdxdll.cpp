#include <io.h>
#include <stdio.h>
#include <Windows.h>

#include "error.h"
#include "tdxdll.h"
#include "cube\os.h"
#include "cube\mm.h"
#include "cube\file.h"

BEGIN_TRADE_NAMESPACE
int tdxdll::load(std::string account, std::string *error/* = 0*/) {
	//create new dll directory
	if (!cube::file::exist(TDX_NEWDLL_PATH)) {
		if (cube::file::mkdirs(TDX_NEWDLL_PATH) != 0) {
			if(error != 0)
				*error = ERR_TDX_INIT_TDXDLL;
			return -1;
		}
	}
	if (!cube::file::isdir(TDX_NEWDLL_PATH)) {
		if (error != 0)
			*error = ERR_TDX_INIT_TDXDLL;
		return -1;
	}

	//generate the new dll path
	std::string newdllpath = TDX_NEWDLL_PATH + cube::file::filename(TDX_RAWDLL_PATH) + "." + account + ".dll";
	int err = create_newdll(account, TDX_RAWDLL_PATH, newdllpath);
	if (err != 0) {
		if (error != 0)
			*error = ERR_TDX_INIT_TDXDLL;
		return -1;
	}

	//load dll module
	_hmodule = LoadLibrary(newdllpath.c_str());
	if (_hmodule == NULL) {
		if (error != 0)
			*error = cube::os::last_error();
		return -1;
	}

	//load export api
	OpenTdx = (OpenTdxDelegate)GetProcAddress((HMODULE)_hmodule, "OpenTdx");
	CloseTdx = (CloseTdxDelegate)GetProcAddress((HMODULE)_hmodule, "CloseTdx");
	Logon = (LogonDelegate)GetProcAddress((HMODULE)_hmodule, "Logon");
	Logoff = (LogoffDelegate)GetProcAddress((HMODULE)_hmodule, "Logoff");
	QueryData = (QueryDataDelegate)GetProcAddress((HMODULE)_hmodule, "QueryData");
	SendOrder = (SendOrderDelegate)GetProcAddress((HMODULE)_hmodule, "SendOrder");
	CancelOrder = (CancelOrderDelegate)GetProcAddress((HMODULE)_hmodule, "CancelOrder");
	GetQuote = (GetQuoteDelegate)GetProcAddress((HMODULE)_hmodule, "GetQuote");
	Repay = (RepayDelegate)GetProcAddress((HMODULE)_hmodule, "Repay");

	QueryDatas = (QueryDatasDelegate)GetProcAddress((HMODULE)_hmodule, "QueryDatas");
	QueryHistoryData = (QueryHistoryDataDelegate)GetProcAddress((HMODULE)_hmodule, "QueryHistoryData");
	SendOrders = (SendOrdersDelegate)GetProcAddress((HMODULE)_hmodule, "SendOrders");
	CancelOrders = (CancelOrdersDelegate)GetProcAddress((HMODULE)_hmodule, "CancelOrders");
	GetQuotes = (GetQuotesDelegate)GetProcAddress((HMODULE)_hmodule, "GetQuotes");


	return 0;
}

int tdxdll::free() {
	if (_hmodule != 0) {
		FreeModule((HMODULE)_hmodule);
		_hmodule = 0;
	}
	return 0;
}

int tdxdll::create_newdll(const std::string& account, const std::string& rawdll, const std::string& newdll) {
	//check if new dll is exist
	if (cube::file::exist(newdll)){
		if (cube::file::isfile(newdll))
			return 0;
		else
			return -1;
	}

	//check if raw dll is exist
	if (!cube::file::exist(rawdll) || !cube::file::isfile(rawdll)) {
		return -1;
	}

	//read dll content
	int filesz = 0;
	char* content = cube::file::read(rawdll, filesz);
	if (content == 0) {
		return -1;
	}

	//target key for raw account which will be replaced
	std::string rawkey = "CCHOGIBI";
	//encrypted key for account
	std::string newkey = encrypt_account(account.c_str());

	//repleace content
	cube::mm::overwrite(content, filesz, rawkey.c_str(), rawkey.length(), newkey.c_str(), newkey.length());

	//write to new dll
	int err = cube::file::write(newdll, content, filesz);
	if (err != 0) {
		delete[]content;
		return -1;
	}
	
	//free content
	delete[]content;

	return 0;
}

std::string tdxdll::encrypt_account(const std::string& account) {
	std::string encrypted("");

	//get the account string length
	int acount_len = (int)account.length();

	//encrypt every char in odd position of account string
	unsigned short salt = 0x055E;
	for (int i = 0; i < (int)account.length(); i += 2) {
		int c = (int)account[i] ^ (salt >> 8);
		salt = (unsigned short)(0x207F * (salt + c) - 0x523D);

		bool flag = true;
		for (int j = (int)'A'; j <= (int)'Z'&&flag; j++) {
			for (int k = (int)'Z'; k >= (int)'A'&&flag; k--) {
				int temp = 0x06DB + c - k;
				if (temp % 26 == 0 && temp / 26 == j) {
					encrypted.push_back((char)j);
					encrypted.push_back((char)k);

					flag = false;
				}
			}
		}
	}

	return encrypted;
}

END_TRADE_NAMESPACE
