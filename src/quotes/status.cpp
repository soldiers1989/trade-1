#include "status.h"
BEGIN_QUOTES_NAMESPACE
int status::SUCCESS = 0;
int status::ERROR = -1;
int status::ERROR_NOT_AUTHORIZED = -100;
int status::ERROR_NOT_CONNECTED = -200;
int status::ERROR_INVALID_PARAM = -300;
END_QUOTES_NAMESPACE
