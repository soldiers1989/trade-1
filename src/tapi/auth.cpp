#include "auth.h"
#include "cube\str.h"
BEGIN_SEC_NAMESPACE
void auth::init(const std::string &user) {
	//set user
	_user = user;

	//set token
	_token = cube::str::random(16);
}
END_SEC_NAMESPACE
