/*
*	http - http protocol parser module
*/
#pragma once
#include "cube.h"
#include <map>
#include <string>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//uri structure
//uri->[scheme:][//authority][/path][?query][#fragment]
//authority->[host:port]
class uri {
public:
	uri();
	virtual ~uri();

	/*
	*	parse uri from string
	*@param str: in, uri string
	*@param sz: in, size of string
	*@param error: out, error message when failed
	*@return:
	*	0 for success, otherwise <0
	*/
	int parse(const std::string &str, std::string *error = 0);
	int parse(const char *str, int sz, std::string *error = 0);
	
	/*
	*	encode uri to string
	*@param str: out, uri string
	*@param error: out, error message when failed
	*return:
	*	0 for success, otherwise <0
	*/
	int pack(std::string &str, std::string *error = 0);

private:
	std::string _scheme; //uri scheme string
	std::string _auth; //uri authority string
	std::string _path; //uri path string
	std::string _query; //uri query string
	std::string _fragment; //uri fragment string
};

//header class
class header {
public:
	header();
	virtual ~header();

	/*
	*	parse header items from string
	*@param str: in, header string
	*@param sz: in, size of string
	*@param error: out, error message when failed
	*@return:
	*	0 for success, otherwise <0
	*/
	int parse(const std::string &str, std::string *error = 0);
	int parse(const char *str, int sz, std::string *error = 0);

	/*
	*	pack header items to string
	*@param str: out, header string
	*@param error: out, error message when failed
	*return:
	*	0 for success, otherwise <0
	*/
	int pack(std::string &str, std::string *error = 0);

private:
	//header items
	std::multimap<std::string, std::string> _items;
};

/*data type to save http request parse results*/
class request {
public:
	request();
	virtual ~request();

	/*
	*	parse header items from string
	*@param str: in, header string
	*@param sz: in, size of string
	*@param error: out, error message when failed
	*@return:
	*	0 for success, otherwise <0
	*/
	int parse(const std::string &str, std::string *error = 0);
	int parse(const char *str, int sz, std::string *error = 0);

	/*
	*	pack header items to string
	*@param str: out, header string
	*return:
	*	0 for success, otherwise <0
	*/
	int pack(std::string &str, std::string *error = 0);

private:
	//request method
	std::string _method;
	//request uri
	uri _uri;
	//http version
	std::string _version;

	//request header
	header _header;
};

/*data type to save http response results*/
class response {
public:
	response();
	virtual ~response();

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

//seperator used for parsing and packing
class sep {
public:
	const char *AUTH = "//";
	const char *REQUEST = "\r\n";
	const char *STATUS = "\r\n";
	const char *HEADER = "\r\n\r\n";

	const char SCHEME = ':';
	const char SPACE = ' ';
	const char VERSION = '/';

	const char PATH = '/';
	const char QUERY = '?';
	const char FRAGMENT = '#';

	const char PARAM = '&';
	const char VALUE = '=';

	const char ITEM = ':';

};
END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
