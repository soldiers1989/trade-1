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
static const int BUFSZ = 4096;
//parser class
class parser {
public:
	/*
	*	take data from parser
	*@param data: data take to
	*@param sz: data size
	*@return:
	*	size taked
	*/
	virtual int take(char *data, int sz) = 0;

	/*
	*	feed data to parser
	*@param data: data to feed
	*@param sz: data size
	*@return:
	*	size feed
	*/
	virtual int feed(const char *data, int sz) = 0;

public:
	parser() {}
	virtual ~parser() {}

	std::string take();
	int take(std::string &data);
	int feed(const std::string &data);
};

//address class
class address : parser{
	//address parse error
	typedef cexception error;
public:
	address() : _host(""), _port(0){ }
	address(const std::string &host, ushort port) : _host(host), _port(port) {}
	address(const std::string &data) : _host(""), _port(0) { feed(data.c_str(), data.length()); }
	virtual ~address() {}

	/*
	*	address data parse
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	get/set address host
	*/
	const std::string& host() { return _host; }
	void host(const std::string &host) { _host = host; }

	/*
	*	get/set address port
	*/
	ushort port() { return _port; }
	void port(ushort port) { _port = port; }
	
private:
	//host address in url
	std::string _host;
	//port in url
	ushort _port;
};

//parameters structure
class params : parser{
public:
	params() {}
	params(const std::string &data) { feed(data.c_str(), data.length()); }
	virtual ~params(){}

	/*
	*	params data parse
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	get param value by specfied key
	*@param key: in, param key
	*@param val: in/out, value of specified key
	*@return:
	*	value of param
	*/
	std::vector<std::string> get(const std::string &key);
	std::string get(const std::string &key, const char *default);
private:
	//params
	std::map<std::string, std::vector<std::string>> _params;
};

//uri structure
//uri->[scheme:][//authority][/path][?query][#fragment]
//authority->[host:port]
class uri : parser {
	//uri parse error
	typedef cexception error;
public:
	uri() : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") {}
	uri(const std::string &data) : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") { feed(data.c_str(), data.length()); }
	virtual ~uri() {}

	/*
	*	uri data parse
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	get uri items
	*/
	const std::string& protocol() const { return _scheme; }
	const std::string& scheme() const { return _scheme; }
	const std::string& auth() const { return _auth; }
	const std::string& path() const { return _path; }
	const std::string& query() const { return _query; }
	const std::string& fragment() const { return _fragment; }

	const address& addr() const { return _addr; }
	const params& params() const { return _params; }
	
private:
	std::string _scheme; //uri scheme string
	std::string _auth; //uri authority string
	std::string _path; //uri path string
	std::string _query; //uri query string
	std::string _fragment; //uri fragment string
	
	http::address _addr; //uri address
	http::params _params; //parameters in query string
};

//http version class
//format: HTTP/1.1
class version : parser {
	//version parse error
	typedef cexception error;
public:
	static version DEFAULT;

public:
	version() : _name("HTTP"), _code("1.1") {}
	version(const std::string &data) : _name(""), _code("") { feed(data.c_str(), data.length()); }
	version(const std::string &name, const std::string &code) : _name(name), _code(code) { }
	virtual ~version() {}

	/*
	*	http version data parser
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	get/set version items
	*/
	const std::string& name() { return _name; }
	const std::string& code() { return _code; }
private:
	//version name, must be "http"
	std::string _name;
	//http version code
	std::string _code;
};

//request query line class
//data: GET /path?param HTTP/1.1\r\n
class query : parser {
	//error query data exception
	typedef cexception error;
public:
	query() {}
	virtual ~query() {}

	/*
	*	http query line data parser
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	request uri by get/post method
	*/
	query& get(const char *format, ...);
	query& post(const char *format, ...);

	/*
	*	get query items parsed from data
	*/
	const std::string &method() { return _method; }
	const std::string &path() { return _uri.path(); }
	const params &params() { return _uri.params(); }
	const std::string &fragment() { return _uri.fragment(); }
	const std::string &version() { return _version.code(); }
private:
	//request method
	std::string _method;
	//request uri
	http::uri _uri;
	//request http version
	http::version _version;
};

//response status line class
class status : parser{
	//status error
	typedef cexception error;
public:
	static status OK, MOVE, REDIRECT, BAD, ERR;

public:
	status() : _code(""), _reason("") {}
	status(const std::string &data) : _code(""), _reason("") { feed(data.c_str(), data.length()); }
	virtual ~status() {}

	/*
	*	http status line data parser
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	get & set status code
	*/
	const std::string &code() { return _code; }
	void code(const std::string &code) { _code = code; }

	/*
	*	get & set http version
	*/
	const std::string &version() { return _version.name(); }
	void version(const std::string &version) { _version = version; }

	/*
	*	get & set status reason phrase
	*/
	const std::string &reason() { return _reason; }
	void reason(const std::string &reason) { _reason = reason; }

private:
	//http version
	http::version _version;
	//response code
	std::string _code;
	//response description
	std::string _reason;
};

//header class
//request header
class header : parser{
	//bad header execption
	typedef cexception error;
	
	typedef std::pair<std::string, std::string> keyval;
	typedef std::vector<keyval> keyvals;
	typedef std::map<std::string, keyvals> items;

public:
	header() {}
	header(const std::string &data) {}
	virtual ~header() { }

	/*
	*	http header data parser
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	set string value of specified item
	*@param item: in, item key
	*@param replace: in, replace item value if exist
	*@param format: in, format string
	*@return:
	*	self
	*/
	header &set(const std::string &key, bool replace, const char *format, ...);
	header &set(const std::map<std::string, std::string> &items, bool replace = false);

	/*
	*	get string value of specified item
	*@param item: in, item key
	*@param default: in, default value if item not exist
	*@return:
	*	item string value or default value
	*/
	std::vector<std::string> get(const std::string &item);
	std::string get(const std::string &key, const char *default);
private:
	//header items, map<lower key, vector<<original key, value>>>
	header::items _items;
};

//request&response entity class
class entity : parser {
public:
	entity() {}
	entity(const header &header) {}
	virtual ~entity() {}

	/*
	*	http entity data parser
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);
	
private:
	//content of entity
	std::shared_ptr<stream> _stream;
};

//http request class
class request : parser {
	//bad request execption
	typedef cexception error;

public:
	request() {}
	virtual ~request() {}

	/*
	*	http request data parser
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	get request query/header/content
	*/
	query &query() { return _query; }
	header &header() { return _header; }
	entity &entity() { return _entity; }

private:
	//request query
	http::query _query;
	//request header
	http::header _header;
	//request entity
	http::entity _entity;

};

//http response class
class response {
public:
	response() {}
	virtual ~response() {}

	/*
	*	http response data parser
	*/
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	/*
	*	get/set response data
	*/
	http::status &status() { return _status; }
	void status(const http::status &status) { _status = status; }

	http::header &header() { return _header; }

	http::entity &entity() { return _entity; }

private:
	//response status
	http::status _status;
	//response header
	http::header _header;
	//response content
	http::entity _entity;
};

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
