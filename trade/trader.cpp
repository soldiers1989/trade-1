#include "trader.h"


trader::trader(const char* account, const char* password): _account(account), _password(password), _error("")
{
}


trader::~trader()
{
}

const std::string& trader::account() {
	return _account;
}

const std::string& trader::password() {
	return _password;
}

void trader::set_last_error(const std::string& error) {
	_error = error;
}

const std::string& trader::get_last_error() {
	return _error;
}
