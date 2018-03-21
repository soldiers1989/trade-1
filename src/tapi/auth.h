/*
*	auth - authority management
*/
#pragma once
#include "stdapi.h"
#include <string>
BEGIN_SEC_NAMESPACE
class auth {
public:
	auth() : _user(""), _token("") { }
	auth(const std::string &user, const std::string &token) : _user(user), _token(token) { }
	~auth() {}

	void init(const std::string &user);

	const std::string &user() const { return _user; }
	const std::string &token() const { return _token; }

private:
	std::string _user;
	std::string _token;
};
END_SEC_NAMESPACE
