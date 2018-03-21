#include <io.h>
#include <stdio.h>
#include <Windows.h>

#include "tdxdll.h"
#include "cube\safe.h"
#include "cube\sys\path.h"
#include "cube\sys\file.h"
#include "cube\sys\error.h"
#include "cube\str\search.h"

BEGIN_TRADE_NAMESPACE
const char* tdxdllerr::ERR_INIT_DLL = "初始化tdx动态链接库错误";

const char* tdxdllcfg::RAWDLL_DIR = "dll\\raw";
const char* tdxdllcfg::RAWDLL_NAME = "Trade.dll";
const char* tdxdllcfg::NEWDLL_DIR = "dll\\new";

int tdxdll::load(const std::string &workdir, const std::string &account, std::string *error/* = 0*/) {
	//get absolute dll file path
	std::string newdlldir = cube::sys::path::mkpath(workdir, tdxdllcfg::NEWDLL_DIR);

	//create new dll directory
	if (!cube::sys::file::exist(newdlldir)) {
		if (cube::sys::path::mkdirs(newdlldir) != 0) {
			cube::safe_assign<std::string>(error, tdxdllerr::ERR_INIT_DLL);
			return -1;
		}
	}
	if (!cube::sys::file::isdir(newdlldir)) {
		cube::safe_assign<std::string>(error, tdxdllerr::ERR_INIT_DLL);
		return -1;
	}

	//generate the new dll path
	std::string rawdllfile = cube::sys::path::mkpath(workdir, cube::sys::path::mkpath(tdxdllcfg::RAWDLL_DIR, tdxdllcfg::RAWDLL_NAME));
	std::string newdllfile =  cube::sys::path::mkpath(newdlldir, cube::sys::file::name(tdxdllcfg::RAWDLL_NAME) + "." + account + ".dll");
	int err = create_newdll(account, rawdllfile, newdllfile);
	if (err != 0) {
		cube::safe_assign<std::string>(error, tdxdllerr::ERR_INIT_DLL);
		return -1;
	}

	//load dll module
	_hmodule = LoadLibrary(newdllfile.c_str());
	if (_hmodule == NULL) {
		cube::safe_assign<std::string>(error, cube::sys::last_error());
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
	if (cube::sys::file::exist(newdll)){
		if (cube::sys::file::isfile(newdll))
			return 0;
		else
			return -1;
	}

	//check if raw dll is exist
	if (!cube::sys::file::exist(rawdll) || !cube::sys::file::isfile(rawdll)) {
		return -1;
	}

	//read dll content
	int filesz = 0;
	char* content = cube::sys::file::read(rawdll, filesz);
	if (content == 0) {
		return -1;
	}

	//target key for raw account which will be replaced
	std::string rawkey = "CCHOGIBI";
	//encrypted key for account
	std::string newkey = encrypt_account(account.c_str());

	//repleace content
	cube::str::search_replace(content, filesz, rawkey.c_str(), rawkey.length(), newkey.c_str(), newkey.length());

	//write to new dll
	int err = cube::sys::file::write(newdll, content, filesz);
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
