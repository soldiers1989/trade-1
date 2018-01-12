/*
*	http - http protocol parser module
*/
#pragma once
#include "cube.h"
#include "stream.h"
#include <map>
#include <vector>
#include <memory>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//network address class
class addr {
	//address parse error
	typedef cexception error;
public:
	addr() : _host(""), _port(0){}
	addr(const std::string &host, ushort port) : _host(host), _port(port) {}
	virtual ~addr() {}

	/*
	*	parse network address from string
	*@param str: in, address string
	*@param sz: in, size of string
	*@return:
	*	void
	*/
	void parse(const std::string &str, const char *default_port = "80");
	void parse(const char* str, int sz, const char *default_port = "80");

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
	*	void
	*/
	void parse(const std::string &str);
	void parse(const char* str, int sz);

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
	virtual ~uri() {}

	/*
	*	parse uri from string
	*@param str: in, uri string
	*@param sz: in, size of string
	*@return:
	*	void
	*/
	void parse(const std::string &str);
	void parse(const char *str, int sz);

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

private:
	std::string _scheme; //uri scheme string
	std::string _auth; //uri authority string
	std::string _path; //uri path string
	std::string _query; //uri query string
	std::string _fragment; //uri fragment string

	cube::http::params _params; //parameters in query string
};

//http version class
//format: HTTP/xxx
class version {
	//version parse error
	typedef cexception error;
public:
	version() {}
	version(const std::string &protocol, const std::string &version) : _protocol(protocol), _version(version) {}
	virtual ~version() {}

	/*
	*	pack version data
	*/
	std::string pack();

	/*
	*	parse version from string
	*@param str: in, version string
	*@param sz: in, size of string
	*@return:
	*	0 for success, otherwise <0
	*/
	void parse(const std::string &str);
	void parse(const char *str, int sz);

private:
	//protocol, must be "http"
	std::string _protocol;
	//http version
	std::string _version;
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
	query() : _method(""), _path(""), _fragment(""), _version(""), _stream("\r\n") {}
	virtual ~query() {}

	/*
	*	write data to query
	*@param data: in, write feed to query
	*@param sz: in, data size want to write
	*@return:
	*	data size written
	*/
	int write(const char *data, int sz);

	/*
	*	check if query is completed
	*@return:
	*	true for completed, false if not
	*/
	bool completed() { return _stream.completed(); }

	/*
	*	get query items parsed from data
	*/
	const std::string &method() { return _method; }
	const std::string &version() { return _version; }

	/*
	*	request uri data
	*/
	const std::string &path() { return _path; }
	const params &params() { return _params; }
	const std::string &fragment() { return _fragment; }

	/*
	*	get original query data
	*/
	std::string str() { return _stream.str(); }

private:
	//request method
	std::string _method;
	//request uri
	std::string _uri;
	//request http version
	std::string _version;

	//request path
	std::string _path;
	//get params
	http::params _params;
	//request fragment
	std::string _fragment;

	//query stream
	delimitedstream _stream;
};

//header class
//request header
class header {
	//bad header execption
	typedef cexception error;
public:
	header() : _stream("\r\n\r\n") {}
	virtual ~header() {}

	/*
	*	feed data to header
	*@param data: in, data to feed
	*@param sz: in, data size want to feed
	*@return:
	*	data size took by header object
	*/
	int write(const char *data, int sz);

	/*
	*	check if header is completed
	*@return:
	*	true for completed, false if not
	*/
	bool completed() { return _stream.completed(); }

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
	delimitedstream _stream;
};

//content class
//post content
class content {
public:
	content() : _stream(0){}
	virtual ~content() {}

	/*
	*	set content size
	*/
	void size(int sz) { _stream.size(sz); }

	/*
	*	write data to header
	*@param data: in, data to write
	*@param sz: in, data size want to write
	*@return:
	*	data size written
	*/
	int write(const char *data, int sz);

	/*
	*	check if header is completed
	*@return:
	*	true for completed, false if not
	*/
	bool completed() { return _stream.completed(); }

private:
	//post params
	http::params _params;

	//stream to hold content
	sizedstream _stream;
};

/*data type to save http request parse results*/
class request {
	//bad request execption
	typedef cexception error;

public:
	request() {}
	virtual ~request() {}

	/*
	*	write data to request, and try to parse request in the same time
	*@param data: in, new data
	*@param sz: in, data size
	*@return:
	*	data size written
	*/
	int write(const char *data, int sz);

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

//response status class
class status {
	//status error
	typedef cexception error;
public:
	status() : _stream("\r\n") {}
	status(const std::string &version, const std::string &code, const std::string &reason) : _version(version), _code(code), _reason(reason), _stream("\r\n"){}
	virtual ~status() {}

	/*
	*	make status stream data
	*/
	void make();

	/*
	*	read status to data
	*@param data: in/out, data output
	*@param sz: in, input data buffer size
	*@return:
	*	size read
	*/
	int read(char *data, int sz);

	/*
	*	feed data to response status
	*@param data: in, data to feed
	*@param sz: in, data size to feed
	*@return:
	*	data size taked
	*/
	int write(const char *data, int sz);

	/*
	*	check if query is completed
	*@return:
	*	true for completed, false if not
	*/
	bool completed() { return _stream.completed(); }
private:
	//http version
	std::string _version;
	//response code
	std::string _code;
	//response description
	std::string _reason;

	//stream status data
	delimitedstream _stream;
};

//response status specification
class statuss {
	//status error
	typedef cexception error;
public:
	//register status
	class setter {
	public:
		setter(const std::string &version, const std::string &code, const std::string &reason) {
			statuss::set(code, status(version, code, reason));
		}
		virtual ~setter() {}
	};

public:
	/*
	*	get & set status specification
	*/
	static const status &get(const std::string &code);
	static void set(const std::string &code, const status &status);

private:
	static std::map<std::string, status> _statuss;
};

/*data type to save http response results*/
class response {
public:
	response() {}
	virtual ~response() {}

	/*
	*	read data from response
	*@param data: in/out, data read to
	*@param sz: in, data size wang to read
	*@return:
	*	data read
	*/
	int read(char *data, int sz);

	/*
	*	feed data to response
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int write(const char *data, int sz);

private:
	//response status
	status _status;
	//response header
	header _header;
	//response content
	content _content;
};

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
