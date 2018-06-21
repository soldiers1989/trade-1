#include "status.h"
BEGIN_TRADES_NAMESPACE
int status::SUCCESS = 0;
int status::ERROR = -1;
int status::ERROR_NOT_AUTHORIZED = -100;
int status::ERROR_ACCOUNT_NOT_EXIST = -200;
int status::ERROR_INVALID_PARAM = -300;
END_TRADES_NAMESPACE
