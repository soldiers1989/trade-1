#pragma once
#include <string>

class tdxdll
{
public:
	tdxdll() {}
	~tdxdll() {}

	/*
	*	create a new dll for account by raw dll
	*@param account: account of stock exchange
	*@param rawdll: raw dll path of tdx
	*@param newdll: new dll path of tdx for input account
	*@return:
	*	0--success, otherwise for failure
	*/
	static int create(const std::string& account, const std::string& rawdll, const std::string& newdll);

private:
	static int encrypt(const std::string& account, std::string *encrypted);
};

