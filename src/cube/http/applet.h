#pragma once
#include <map>
#include "cube\http\servlet.h"
BEGIN_CUBE_HTTP_NS
//http applet class
class applet {
public:
	applet() {}
	virtual ~applet() {}

	/*
	*	handle request, set response with process result
	*@param req: in, request object
	*@param resp: in/out, response object
	*@return:
	*	0 for success, otherwise for error
	*/
	int handle(const cube::http::request &req, cube::http::response &resp);

	/*
	*	mount path with relate servlet
	*@param path: in, servlet relate path
	*@param servlet: in, servlet for path
	*@return:
	*	void
	*/
	void mount(const std::string &method, const std::string &path, servlet *servlet);

private:
	//registered servlets, <method, <path, servlet>>
	std::map<std::string, std::map<std::string, std::shared_ptr<servlet>>> _servlets;
};
END_CUBE_HTTP_NS
