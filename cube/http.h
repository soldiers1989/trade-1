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
	*@return:
	*	0 for success, otherwise <0
	*/
	int parse(const std::string &str, std::string *error = 0);
	int parse(const char *str, int sz, std::string *error = 0);
	
	/*
	*	encode uri to string
	*@param str: out, uri string
	*return:
	*	0 for success, otherwise <0
	*/
	int pack(std::string &str);

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

private:
};

/*data type to save http request parse results*/
class request {
public:
	request();
	virtual ~request();


private:
	//request method
	std::string _method;
	//request uri
	uri _uri;
	//http version
	std::string _version;

	//request headers
	std::multimap<std::string, std::string> _headers;
	//request cookies, !!current not used!!
	std::multimap<std::string, std::string> _cookies;
};

/*data type to save http response results*/
class response {
public:
	response();
	virtual ~response();

private:
	//http version
	std::string _version;
	//response code
	std::string _code;
	//response code info
	std::string _code_info;
	//response header parameters
	std::multimap<std::string, std::string> _map_headers;
	//response content
	std::string _content;
};

//response encode types
typedef enum encode_type {
	NONE = 0,
	GZIP = 1,
	DEFLATE = 2
}encode_type;

#define SEP_LINE				"\r\n"
#define HEADER_END				"\r\n\r\n"
#define SEP_GET					' '
#define SEP_URL					' '
#define SEP_SPACE				' '
#define SEP_QM					'?'
#define SEP_EQ					'='
#define SEP_AND					'&'
#define SEP_VERSION				'/'
#define SEP_HEADER				':'
#define MIN_HTTP_LEN				18 //"GET / HTTP/1.1\r\n\r\n"

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
