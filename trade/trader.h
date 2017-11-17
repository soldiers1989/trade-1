#pragma once
#include <string>

class trader
{
public:
	trader(const char* account, const char*password);
	virtual ~trader();

	virtual int init() = 0;

	virtual int login() = 0;

	virtual int query_money() = 0;

	virtual int logout() = 0;

	virtual int destroy() = 0;

protected:
	const std::string& account();
	const std::string& password();

	void set_last_error(const std::string& error);
	const std::string& get_last_error();

private:
	//current account
	std::string _account;
	//current account password
	std::string _password;

	//last error message
	std::string _error;
};

