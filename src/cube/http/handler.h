#pragma once
#include "cube\ns.h"
BEGIN_CUBE_HTTP_NS
class request_handler {
public:
	virtual int on_request_line() = 0;
	virtual int on_request_head() = 0;
	virtual int on_request_body() = 0;
};
END_CUBE_HTTP_NS
