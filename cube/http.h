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
	addr() : _data(""), _host(""), _port(0){ }
	addr(const std::string &str) : _data(str), _host(""), _port(80) { parse(); }
	addr(const std::string &host, ushort port) : _host(host), _port(port) { pack(); }
	virtual ~addr() {}

	/*
	*	parse network address from data string
	*@return:
	*	void
	*/
	void parse();
	void parse(const std::string &str);

	/*
	*	pack network address to data string
	*/
	void pack();

	/*
	*	get address information
	*/
	const std::string& host() { return _host; }
	ushort port() { return _port; }

	const std::string& data() { return _data; }

private:
	//host address in url
	std::string _host;
	//port in url
	ushort _port;

	//original data
	std::string _data;
};

//parameters structure
class params {
public:
	params() : _data("") {}
	params(const std::string &str) : _data(str) { parse(); }
	virtual ~params(){}

	/*
	*	parse params from data string
	*@return:
	*	void
	*/
	void parse();
	void parse(const std::string &str);

	/*
	*	pack params to data string
	*/
	void pack();

	/*
	*	get param value by specfied key
	*@param key: in, param key
	*@param val: in/out, value of specified key
	*@return:
	*	value of param
	*/
	void get(const std::string &key, std::string &val);
	std::string get(const std::string &key, const char *default = "");

	/*
	*	get param values by specified key
	*@param key: in, param key
	*@param vals: in/out, values of specified key
	*@return:
	*	values of param
	*/
	std::vector<std::string> gets(const std::string &key);
	void gets(const std::string &key, std::vector<std::string> &vals);
	

	const std::string& data() { return _data; }

private:
	//params
	std::map<std::string, std::vector<std::string>> _params;

	//params data
	std::string _data;
};

//uri structure
//uri->[scheme:][//authority][/path][?query][#fragment]
//authority->[host:port]
class uri {
	//uri parse error
	typedef cexception error;
public:
	uri() : _scheme(""), _auth(""), _path(""), _query(""), _fragment(""), _data("") {}
	uri(const std::string &str) : _scheme(""), _auth(""), _path(""), _query(""), _fragment(""), _data(str) { parse(); }
	virtual ~uri() {}

	/*
	*	parse uri from data string
	*@return:
	*	void
	*/
	void parse();
	void parse(const std::string &str);

	/*
	*	pack uri to data string
	*@return:
	*	void
	*/
	void pack();

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

	const std::string &data() { return _data; }

private:
	std::string _scheme; //uri scheme string
	std::string _auth; //uri authority string
	std::string _path; //uri path string
	std::string _query; //uri query string
	std::string _fragment; //uri fragment string

	std::string _data; //original uri data string
	
	cube::http::params _params; //parameters in query string
};

//http version class
//format: HTTP/1.1
class version {
	//version parse error
	typedef cexception error;
public:
	static version DEFAULT;

public:
	version() : _name("HTTP"), _code("1.1"), _data("HTTP/1.1") {}
	version(const std::string &str) : _name(""), _code(""), _data(str) { parse(); }
	version(const std::string &name, const std::string &code) : _name(name), _code(code), _data("") { pack(); }
	virtual ~version() {}

	/*
	*	parse version from data string
	*@return:
	*	void
	*/
	void parse();
	void parse(const std::string &str);

	/*
	*	pack version to data string
	*@return:
	*	void
	*/
	void pack();

	const std::string& name() { return _name; }
	const std::string& code() { return _code; }
	const std::string& data() { return _data; }

private:
	//version name, must be "http"
	std::string _name;
	//http version code
	std::string _code;

	//original version data
	std::string _data;
};

//method class
class method {
	//error request method
	typedef cexception error;
public:
	//support http method
	static method GET;
	static method POST;

public:
	method() {}
	method(const std::string &str) : _data(str) { parse(); }
	virtual ~method() {}

	/*
	*	parse method from data string
	*@return:
	*	void
	*/
	void parse();
	void parse(const std::string &str);

	/*
	*	pack method to data string
	*@return:
	*	void
	*/
	void pack();

	/*
	*	get method name
	*/
	const std::string &name() { return _name; }
	const std::string &data() { return _data; }

private:
	bool support(const std::string &mtd);
private:
	//method name
	std::string _name;

	//original data
	std::string _data;
};

//query class
//data: GET /path?param HTTP/1.1\r\n
class query {
	//error query data exception
	typedef cexception error;
public:
	query() : _stream("\r\n") {}
	virtual ~query() {}

	/*
	* make query data
	*@return
	*	void
	*/
	void make();

	/*
	*	read query data
	*@param data: in/out, data output
	*@param sz: in, input data buffer size
	*@return:
	*	size read
	*/
	int read(char *data, int sz);

	/*
	*	feed data to query
	*@param data: in, write feed to query
	*@param sz: in, data size want to write
	*@return:
	*	data size written
	*/
	int feed(const char *data, int sz);

	/*
	*	check if query is completed
	*@return:
	*	true for completed, false if not
	*/
	bool full() { return _stream.completed(); }

	/*
	*	
	*/
	void get(const char *uri_format, ...);
	void post(const char *uri_format, ...);

	/*
	*	get query items parsed from data
	*/
	const std::string &method() { return _method.name(); }
	const std::string &version() { return _version.code(); }

	/*
	*	request uri data
	*/
	const std::string &path() { return _uri.path(); }
	const params &params() { return _uri.params(); }
	const std::string &fragment() { return _uri.fragment(); }

	/*
	*	get original query data
	*/
	std::string &data() { return _stream.data(); }
private:
	/*
	*	parse query from stream data
	*@return:
	*	void
	*/
	void parse();

private:
	//request method
	http::method _method;
	//request uri
	http::uri _uri;
	//request http version
	http::version _version;

	//query stream
	delimitedstream _stream;
};

//header class
//request header
class header {
	//bad header execption
	typedef cexception error;
	
	typedef std::pair<std::string, std::string> keyval;
	typedef std::vector<keyval> keyvals;
	typedef std::map<std::string, keyvals> items;

public:
	header() : _stream("\r\n\r\n") {}
	virtual ~header() {}

	/*
	* make header data
	*@return
	*	void
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
	*	check if item exist and get item value
	*/
	bool has(const std::string &key);

	/*
	*	set string value of specified item
	*@param item: in, item key
	*@param replace: in, replace item value if exist
	*@param format: in, format string
	*@return:
	*	self
	*/
	header &set(const std::string &key, bool replace, const char *format, ...);

	/*
	*	get string value of specified item
	*@param item: in, item key
	*@param default: in, default value if item not exist
	*@return:
	*	item string value or default value
	*/
	std::string get(const std::string &key, const char *default = "");

	/*
	*	get string values of specified item
	*@param item: in, item key
	*@return:
	*	values in vector of specfied item
	*/
	std::vector<std::string> gets(const std::string &item);

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

private:
	//header items, map<lower key, vector<<original key, value>>>
	header::items _items;

	//empty value for not exist header item
	std::string _empty;

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
	bool completed() { return _query.full() && _header.completed() && _content.completed(); }
	
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

	/*
	*	get & set status code
	*/
	const std::string &code() { return _code; }
	void code(const std::string &code) { _code = code; }

	/*
	*	get & set http version
	*/
	const std::string &version() { return _version; }
	void version(const std::string &version) { _version = version; }

	/*
	*	get & set status reason phrase
	*/
	const std::string &reason() { return _reason; }
	void reason(const std::string &reason) { _reason = reason; }

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
	*	get / set status code
	*/
	const std::string& status() { return _status.code(); }
	void status(const std::string &code) {}
	
	/*
	*	get / set response header
	*/
	std::string header(const std::string &key, const char *default = "");
	void header(const std::string &key, bool replace, const char *format, ...);
	
	/*
	*	get / set response content
	*/
	const std::string &content();
	void content(const std::string &type, char *data, int sz);

	/*
	*	make response stream data after set response values
	*/
	void make();

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
	http::status _status;
	//response header
	http::header _header;
	//response content
	http::content _content;
};

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
