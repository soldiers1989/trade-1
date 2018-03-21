#pragma once
#include "cube\http\request.h"
#include "cube\http\response.h"
BEGIN_CUBE_HTTP_NS
//http servlet class
class servlet {
public:
	/*
	*	handle http request
	*@param req: in, client request
	*@param resp: in/out, service response
	*@return:
	*	0 for success, otherwise for error
	*/
	virtual int handle(const cube::http::request &req, cube::http::response &resp) = 0;
};
END_CUBE_HTTP_NS

