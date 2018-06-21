#pragma once
#include "stdtrds.h"
BEGIN_TRADES_NAMESPACE
class status {
public:
	static int SUCCESS;
	static int ERROR;
	static int ERROR_NOT_AUTHORIZED;
	static int ERROR_ACCOUNT_NOT_EXIST;
	static int ERROR_INVALID_PARAM;
};
END_TRADES_NAMESPACE
