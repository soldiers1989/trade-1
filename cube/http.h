/*
*	http - http protocol parser module
*/
#pragma once
#include "cube.h"
#include <map>
#include <vector>
#include <string>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//network address class
class addr {
public:
	addr() : _host(""), _port(0){}
	addr(const std::string &str);
	addr(const char *str, int sz);
	virtual ~addr() {}

	/*
	*	parse network address from string
	*@param str: in, address string
	*@param sz: in, size of string
	*@return:
	*	addr parsed
	*/
	static addr* parse(const std::string &str);
	static addr* parse(const char* str, int sz);

	/*
	*	get address information
	*/
	const std::string& host() { return _host; }
	ushort port() { return _port; }

private:
	/*
	*	parse network address from string
	*@param str: in, address string
	*@param sz: in, size of string
	*@return:
	*	void
	*/
	void _parse(const std::string &str);
	void _parse(const char* str, int sz);

private:
	//host address in url
	std::string _host;
	//port in url
	ushort _port;
};

//parameters structure
class params {
public:
	params() {}
	params(const std::string &str);
	params(const char *str, int sz);
	virtual ~params(){}

	/*
	*	parse parameters from string
	*@param str: in, parameters string
	*@param sz: in, size of string
	*@return:
	*	parameters parsed
	*/
	static params* parse(const std::string &str);
	static params* parse(const char* str, int sz);

	/*
	*	get parameter value by specfied key
	*@param key: in, parameter key
	*@return:
	*	value of parameter
	*/
	std::string get(const std::string &key);
	std::vector<std::string> gets(const std::string &key);

private:
	/*
	*	parse parameters from string
	*@param str: in, parameters string
	*@param sz: in, size of string
	*@return:
	*	void
	*/
	void _parse(const std::string &str);
	void _parse(const char* str, int sz);

	//parameters
	std::map<std::string, std::vector<std::string>> _params;
};

//uri structure
//uri->[scheme:][//authority][/path][?query][#fragment]
//authority->[host:port]
class uri {
public:
	uri() : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") {}
	uri(const std::string &str);
	uri(const char *str, int sz);
	virtual ~uri() {}

	/*
	*	parse uri from string
	*@param str: in, uri string
	*@param sz: in, size of string
	*@return:
	*	uri object parsed
	*/
	static uri* parse(const std::string &str);
	static uri* parse(const char *str, int sz);

	/*
	*	get uri items
	*/
	const std::string& protocol() { return _scheme; }
	const std::string& scheme() { return _scheme; }
	const std::string& auth() { return _auth; }
	const std::string& path() { return _path; }
	const std::string& query() { return _query; }
	const std::string& fragment() { return _fragment; }
	const params& params() { return _params; }

	/*
	*	get description of uri
	*@return:
	*	description of uri
	*/
	std::string description();
private:
	/*
	*	parse uri from string
	*@param str: in, uri string
	*@param sz: in, size of string
	*@return:
	*	uri object or 0(null) means parse failed
	*/
	void _parse(const std::string &str);
	void _parse(const char *str, int sz);

private:
	std::string _scheme; //uri scheme string
	std::string _auth; //uri authority string
	std::string _path; //uri path string
	std::string _query; //uri query string
	std::string _fragment; //uri fragment string

	cube::http::params _params; //parameters in query string
};

//header class
class header {
public:
	header() {}
	header(const std::string &str);
	header(const char *str, int sz);
	virtual ~header() {}

	/*
	*	parse header items from string
	*@param str: in, header string
	*@param sz: in, size of string
	*@param error: out, error message when failed
	*@return:
	*	header object
	*/
	static header* parse(const std::string &str);
	static header* parse(const char *str, int sz);

public:
	/*
	*	parse header items from string
	*@param str: in, header string
	*@param sz: in, size of string
	*@param error: out, error message when failed
	*@return:
	*	header object
	*/
	void _parse(const std::string &str);
	void _parse(const char *str, int sz);

private:
	//header items
	std::map<std::string, std::vector<std::string>> _items;
};

/*data type to save http request parse results*/
class request {
public:
	request() {}
	virtual ~request() {}


	
private:
	//request method
	std::string _method;

	//request path string
	std::string _path;
	//request query string
	std::string _query;
	//request fragment string
	std::string _fragment;

	//request http version
	std::string _version;

	//request header
	header _header;
	
	//request content
	std::string _content;
};

/*data type to save http response results*/
class response {
public:
	response() {}
	virtual ~response() {}

	/*
	*	parse response items from string
	*@param str: in, header string
	*@param sz: in, size of string
	*@param error: out, error message when failed
	*@return:
	*	0 for success, otherwise <0
	*/
	int parse(const std::string &str, std::string *error = 0);
	int parse(const char *str, int sz, std::string *error = 0);

	/*
	*	pack reasponse items to string
	*@param str: out, header string
	*@param error: out, error message when failed
	*return:
	*	0 for success, otherwise <0
	*/
	int pack(std::string &str, std::string *error = 0);

private:
	//scheme->http
	std::string _scheme;
	//http version
	std::string _version;
	//response code
	std::string _code;
	//response description
	std::string _reason;
	
	//response header
	header _header;
};

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
