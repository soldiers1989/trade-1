#pragma once
#include "cube\http\mime.h"
#include "cube\http\config.h"
#include "cube\http\status.h"
#include "cube\http\header.h"
#include "cube\http\entity.h"
#include "cube\http\cookie.h"
#include "cube\http\charset.h"
BEGIN_CUBE_HTTP_NS
class response {
public:
	response() { }
	virtual ~response() {}
	
	std::string pack() const;
	int parse(const std::string &str);

public:
	/*
	*	set response status
	*/
	void set_status(http::status s);

	/*
	*	set response header
	*/
	void set_header(const std::string &name, const std::string &value);
	void add_header(const std::string &name, const std::string &value);

	/*
	*	set response cookie
	*/
	void set_cookie(const std::string &name, const std::string &value, int maxage);

	/*
	*	set response content
	*@param data: in, data to response
	*@param sz: in, data size
	*@param
	*@return:
	*	void
	*/
	void set_content(const char *data, int sz, const std::string &type, const std::string &charset = "");

public:
	/*
	*	redirect to new location, code: 3xx
	*@param code: in, redirect code
	*@param url: in, new location
	*/
	void redirect(const char *url, bool permanent = true);

private:
	//response status
	http::status _status;
	//response header
	http::headers _headers;
	//response content
	std::string _content;
};
END_CUBE_HTTP_NS
