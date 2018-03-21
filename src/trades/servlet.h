#pragma once
#include "cube\http\servlet.h"
class login : public cube::http::servlet {
public:
	virtual int handle(const cube::http::request &req, cube::http::response &resp);
};