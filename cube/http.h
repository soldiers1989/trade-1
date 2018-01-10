/*
*	http - http protocol parser module
*/
#pragma once
#include "cube.h"
#include <map>
#include <vector>
#include <string>
#include <memory>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//network address class
class addr {
public:
	addr() : _host(""), _port(0){}
	addr(const std::string &host, ushort port) : _host(host), _port(port) {}
	virtual ~addr() {}

	/*
	*	parse network address from string
	*@param str: in, address string
	*@param sz: in, size of string
	*@return:
	*	0 for parse success, otherwise <0
	*/
	int parse(const std::string &str);
	int parse(const char* str, int sz);

	/*
	*	get address information
	*/
	const std::string& host() { return _host; }
	ushort port() { return _port; }

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
	virtual ~params(){}

	/*
	*	parse parameters from string
	*@param str: in, parameters string
	*@param sz: in, size of string
	*@return:
	*	0 for parse success, otherwise <0
	*/
	int parse(const std::string &str);
	int parse(const char* str, int sz);


	/*
	*	get parameter value by specfied key
	*@param key: in, parameter key
	*@return:
	*	value of parameter
	*/
	std::string get(const std::string &key) const;
	std::vector<std::string> gets(const std::string &key) const;

private:
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
	const std::string& protocol() const { return _scheme; }
	const std::string& scheme() const { return _scheme; }
	const std::string& auth() const { return _auth; }
	const std::string& path() const { return _path; }
	const std::string& query() const { return _query; }
	const std::string& fragment() const { return _fragment; }
	const params& params() const { return _params; }

	/*
	*	get description of uri
	*@return:
	*	description of uri
	*/
	std::string description();

public:
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

//streamer class
class tagstreamer {
public:
	tagstreamer(const std::string &endtag) : _data(""), _endtag(endtag), _completed(false), _mtpos(0) {}
	virtual ~tagstreamer() {}

	/*
	*	feed data to query
	*@param data: in, data feed to query
	*@param sz: in, data size want to feed
	*@return:
	*	data size took by query object
	*/
	int feed(const char *data, int sz);

	/*
	*	check if streamer is full feed(end tag in the last)
	*@return:
	*	true for full, false if not
	*/
	bool completed() { return _completed; }

	/*
	*	get stream data
	*/
	std::string &data() { return _data; }
	const std::string &cdata() const{ return _data; }

private:
	//data has taken
	std::string _data;
	//end tag for feeding
	std::string _endtag;

	//stream completed flag
	bool _completed;
	//current match pos in end tag
	int _mtpos;
};

//data streamer
class datastreamer {
public:
	datastreamer() : _szwant(INT_MAX) {}
	datastreamer(int sz) : _szwant(sz) {}
	virtual ~datastreamer() {}

	/*
	*	set stream want data size
	*/
	void want(int szwant) { _szwant = szwant; }

	/*
	*	feed data to query
	*@param data: in, data feed to query
	*@param sz: in, data size want to feed
	*@return:
	*	data size took by query object
	*/
	int feed(const char *data, int sz);

	/*
	*	check if streamer is full feed(end tag in the last)
	*@return:
	*	true for full, false if not
	*/
	bool completed() { return _data.length() == _szwant; }

	/*
	*	get stream data
	*/
	std::string &data() { return _data; }
	const std::string &cdata() const { return _data; }

private:
	//data has taken
	std::string _data;

	//stream want size
	int _szwant;
};

//method class
class method {
public:
	method() {}
	virtual ~method() {}

	static bool support(const std::string &mtd);
};

//query class
//data: GET /path?param HTTP/1.1\r\n
class query {
	//error query data exception
	typedef cexception edata;
public:
	query() : _method(""), _path(""), _fragment(""), _version(""), _streamer("\r\n") {}
	virtual ~query() {}

	/*
	*	feed data to query
	*@param data: in, data feed to query
	*@param sz: in, data size want to feed
	*@return:
	*	data size took by query object
	*/
	int feed(const char *data, int sz);

	/*
	*	check if query is completed
	*@return:
	*	true for completed, false if not
	*/
	bool completed() { return _streamer.completed(); }

	/*
	*	get query items parsed from data
	*/
	const std::string &method() { return _method; }
	const std::string &path() { return _path; }
	const params &params() { return _params; }
	const std::string &fragment() { return _fragment; }

	/*
	*	get original query data
	*/
	std::string &data() { return _streamer.data(); }
	const std::string &cdata() const { return _streamer.cdata(); }
	
private:
	//request method
	std::string _method;
	//request path
	std::string _path;
	//request params
	http::params _params;
	//request fragment
	std::string _fragment;
	//request http version
	std::string _version;
	
	//streamer for holding feeded data
	tagstreamer _streamer;
};

//header class
//request header
class header {
	//bad header execption
	typedef cexception error;
public:
	header() : _streamer("\r\n\r\n") {}
	virtual ~header() {}

	/*
	*	feed data to header
	*@param data: in, data to feed
	*@param sz: in, data size want to feed
	*@return:
	*	data size took by header object
	*/
	int feed(const char *data, int sz);

	/*
	*	check if header is completed
	*@return:
	*	true for completed, false if not
	*/
	bool completed() { return _streamer.completed(); }

	/*
	*	parse header items from string
	*@param str: in, header string
	*@param sz: in, size of string
	*@param error: out, error message when failed
	*@return:
	*	0 for success, otherwise <0
	*/
	int parse(const std::string &str);
	int parse(const char *str, int sz);

	/*
	*	check if item exist and get item value
	*/
	bool has(const std::string &item);

	/*
	*	get int value of specified item
	*@param item: in, item key
	*@param default: in, default value if item not exist
	*@return:
	*	item int value or default value
	*/
	int geti(const std::string &item, int default = 0);

	/*
	*	get string value of specified item
	*@param item: in, item key
	*@param default: in, default value if item not exist
	*@return:
	*	item string value or default value
	*/
	std::string gets(const std::string &item, const char *default = "");

	/*
	*	get string values of specified item
	*@param item: in, item key
	*@return:
	*	values in vector of specfied item
	*/
	std::vector<std::string> gets(const std::string &item);

private:
	//header items
	std::map<std::string, std::vector<std::string>> _items;

	//streamer for holding feeded data
	tagstreamer _streamer;
};

//content class
//post content
class content {
public:
	content() : _streamer(){}
	virtual ~content() {}

	/*
	*	feed data to header
	*@param data: in, data to feed
	*@param sz: in, data size want to feed
	*@return:
	*	data size took by header object
	*/
	int feed(const char *data, int sz);

	/*
	*	check if header is completed
	*@return:
	*	true for completed, false if not
	*/
	bool completed() { return _streamer.completed(); }

private:
	//streamer to hold content
	datastreamer _streamer;
};

/*data type to save http request parse results*/
class request {
	//bad request execption
	typedef cexception error;

public:
	request() {}
	virtual ~request() {}

	/*
	*	feed data to request, and try to parse request in the same time
	*@param data: in, new data
	*@param sz: in, data size
	*@return:
	*	true if request data completed and parsed, otherwise return false
	*/
	int feed(const char *data, int sz);
	
	/*
	*	check if request has completed
	*@return:
	*	true if completed, otherwise return false
	*/
	bool completed() { return _query.completed() && _header.completed() && _content.completed(); }
	
	/*
	*	get request query/header/content
	*/
	query &query() { return _query; }
	header &header() { return _header; }
	content &content() { return _content; }

private:
	//request query
	http::query _query;
	//request header
	http::header _header;
	//request content
	http::content _content;
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
