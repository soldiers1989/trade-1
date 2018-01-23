/*
*	http - http protocol parser module
*/
#pragma once
#include "ios.h"
#include <map>
#include <vector>
#include <memory>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE
static const int BUFSZ = 4096;

//charset class
class charset {
public:
	/*
	*	general charsets
	*/
	static std::string utf8;
};

//mime class
class mime {
public:
	/*
	*	general mime types
	*/
	static std::string octet;
	static std::string form;
	static std::string json;
	static std::string unknown;

public:
	/*
	*	get content type by extension name
	*/
	static const std::string &type(const std::string &ext);

	/*
	*	set content type by extension name & type
	*/
	static void type(const std::string &ext, const std::string &ctype);

private:
	//mime types, <extension, http content-type>
	static std::map<std::string, std::string> _types;
};

//parser class
class parser {
public:
	/*
	*	pack data
	*@param data: data pack to
	*@param sz: data size
	*@return:
	*	pack size
	*/
	virtual int pack(char *data, int sz) = 0;

	/*
	*	parse data
	*@param data: data to parse
	*@param sz: data size
	*@return:
	*	parse size
	*/
	virtual int parse(const char *data, int sz) = 0;

public:
	/*
	*	get packed data
	*/
	std::string data();
};

//address class
class address : public parser{
	//address parse error
	typedef cexception error;
public:
	address() : _host(""), _port(0){ }
	address(const std::string &host, ushort port) : _host(host), _port(port) {}
	address(const std::string &data) : _host(""), _port(0) { parse(data.c_str(), data.length()); }
	virtual ~address() {}

	/*
	*	address data pack & parse
	*/
	int pack(char *data, int sz);
	int parse(const char *data, int sz);

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
class params : public parser{
public:
	params() {}
	params(const std::string &data) { parse(data.c_str(), data.length()); }
	virtual ~params(){}

	/*
	*	params data parse
	*/
	int pack(char *data, int sz);
	int parse(const char *data, int sz);

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
class uri : public parser {
	//uri parse error
	typedef cexception error;
public:
	uri() : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") {}
	uri(const std::string &data) : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") { parse(data.c_str(), data.length()); }
	virtual ~uri() {}

	/*
	*	uri data parse
	*/
	int pack(char *data, int sz);
	int parse(const char *data, int sz);

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
class version : public parser {
	//version parse error
	typedef cexception error;
public:
	version() : _name("HTTP"), _code("1.1") {}
	version(const std::string &data) : _name(""), _code("") { parse(data.c_str(), data.length()); }
	version(const std::string &name, const std::string &code) : _name(name), _code(code) { }
	virtual ~version() {}

	/*
	*	http version data parser
	*/
	int pack(char *data, int sz);
	int parse(const char *data, int sz);

	/*
	*	get/set version items
	*/
	const std::string& name() const { return _name; }
	const std::string& code() const { return _code; }
private:
	//version name, must be "http"
	std::string _name;
	//http version code
	std::string _code;
};

//request query line class
//data: GET /path?param HTTP/1.1\r\n
class query : public parser {
	//error query data exception
	typedef cexception error;

	friend class request;
public:
	query() : _method(""), _stream("\r\n") {}
	query(const std::string &data) : _method(""), _stream("\r\n") { parse(data.c_str(), data.length()); }
	virtual ~query() {}

	/*
	*	initialize query by data string, format: "<METHOD> <URI> <HTTP VERSION>\r\n"
	*@param data: query line data
	*@return:
	*	void
	*/
	void init(const std::string &data);

	/*
	*	http query line data parser
	*/
	int pack(char *data, int sz);
	int parse(const char *data, int sz);

	/*
	*	get query items parsed from data
	*/
	const std::string &method() const { return _method; }
	const std::string &path() const { return _uri.path(); }
	const params &params() const { return _uri.params(); }
	const std::string &fragment() const { return _uri.fragment(); }
	const std::string &version() const { return _version.code(); }

private:
	/*
	*	make query line data
	*@return:
	*	void
	*/
	void make();

	/*
	*	take data from query line stream
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

	/*
	*	feed data to query line stream
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz);

	/*
	*	check if query line is full(completed)
	*@return:
	*	true - query line is full(completed), false - not full(completed)
	*/
	bool full() const;

	/*
	*	get query line data
	*@return:
	*	query line data
	*/
	const std::string &data() const;

private:
	//request method
	std::string _method;
	//request uri
	http::uri _uri;
	//request http version
	http::version _version;

	//query line data stream data
	delimitedstream _stream;
};

//response status line class
class status : public parser{
	//status error
	typedef cexception error;
	friend class response;
public:
	//status code
	static const int ok = 200, moved_permanently = 301, moved_temporarily = 302, bad_request = 400, interval_server_error = 500;
	//status setter
	class setter {
	public:
		setter(int code, const std::string &reason);
		~setter() {}
	};

public:
	status() : _code(""), _reason(""), _stream("\r\n") {}
	status(const std::string &data) : _code(""), _reason(""), _stream("\r\n") { parse(data.c_str(), data.length()); }
	virtual ~status() {}

	/*
	*	initialize status by code
	*@param code: in, response status code
	*@return:
	*	void
	*/
	void init(int code);

	/*
	*	http status line data parser
	*/
	int pack(char *data, int sz);
	int parse(const char *data, int sz);

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
	/*
	*	make status line data
	*@return:
	*	void
	*/
	void make();

	/*
	*	take data from status line stream
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

	/*
	*	feed data to status line stream
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz);

	/*
	*	check if status line is full(completed)
	*@return:
	*	true - status line is full(completed), false - not full(completed)
	*/
	bool full() const;

	/*
	*	get status line data
	*@return:
	*	status line data
	*/
	const std::string &data() const;

private:
	//http version
	http::version _version;
	//response code
	std::string _code;
	//response description
	std::string _reason;

	//status line data stream data
	delimitedstream _stream;

	//default status, <int-code, <string-code, reason>>
	static std::map<int, std::pair<std::string, std::string>> _status;
};

//header class
//request header
class header : public parser{
	//bad header execption
	typedef cexception error;
	
	typedef std::pair<std::string, std::string> keyval;
	typedef std::vector<keyval> keyvals;
	typedef std::map<std::string, keyvals> items;

	friend class http::request;
	friend class http::response;

public:
	//default request header class
	class request {
	public:
		class setter {
		public:
			setter(const std::string &key, const std::string &value) { http::header::request::default(key, value); }
			~setter() {}
		};

		/*
		*	get/set default request headers
		*/
		static const std::map<std::string, std::string> &default() { return _header; }
		static void default(const std::string &key, const std::string &value) { _header[key] = value; }

	private:
		//default request header
		static std::map<std::string, std::string> _header;
	};

	//default response header class
	class response {
	public:
		class setter {
		public:
			setter(const std::string &key, const std::string &value) { http::header::response::default(key, value); }
			~setter() {}
		};

		/*
		*	get/set default response headers
		*/
		static const std::map<std::string, std::string> &default() { return _header; }
		static void default(const std::string &key, const std::string &value) { _header[key] = value; }
	private:
		//default request header
		static std::map<std::string, std::string> _header;
	};
public:
	header() : _stream("\r\n\r\n") {}
	header(const std::string &data) : _stream("\r\n\r\n") {}
	virtual ~header() { }

	/*
	*	initialize header by data string, format: "<KEY1>: <VALUE1>\r\n<KEY2>: <VALUE2>\r\n"...
	*@param data: in, header data
	*@return:
	*	void
	*/
	void init(const std::string &data);

	/*
	*	http header data parser
	*/
	int pack(char *data, int sz);
	int parse(const char *data, int sz);

	/*
	*	set string value of specified item
	*@param item: in, item key
	*@param replace: in, replace item value if exist
	*@param format: in, format string
	*@return:
	*	self
	*/
	header &set(const std::string &key, const char *format, ...);
	header &set(const std::string &key, bool replace, const char *format, ...);
	header &set(const std::map<std::string, std::string> &items, bool replace = false);

	/*
	*	get string value of specified item
	*@param item: in, item key
	*@param default: in, default value if item not exist
	*@return:
	*	item string value or default value
	*/
	std::vector<std::string> get(const std::string &item) const;
	std::string get(const std::string &key, const char *default) const;

private:
	/*
	*	make header data
	*@return:
	*	void
	*/
	void make();

	/*
	*	take data from header stream
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

	/*
	*	feed data to header stream
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz);

	/*
	*	check if header is full(completed)
	*@return:
	*	true - header is full(completed), false - not full(completed)
	*/
	bool full() const;

	/*
	*	get header data
	*@return:
	*	request data
	*/
	const std::string &data() const;

private:
	//header items, map<lower key, vector<<original key, value>>>
	header::items _items;

	//header data stream data
	delimitedstream _stream;
};

//request&response entity class
class entity {
	//bad request execption
	typedef cexception error;

	friend class request;
	friend class response;
public:
	entity() : _empty(""), _stream(nullptr) {}
	virtual ~entity() {}

	/*
	*	initialize entity with header
	*@param header: in, request/response header
	*@return:
	*	void
	*/
	void init(const http::header &header);

	/*
	*	initialize entity with local file
	*/
	void file(const std::string &path);

	/*
	*	initialize entity with form data
	*/
	void form(const char *data, int sz);

	/*
	*	initialize entity with specified content type & data
	*@param type: in, content type, xml/html/json/... .etc
	*@param data: in, content data
	*@param sz: in, content size
	*@return:
	*	void
	*/
	void data(const std::string &type, const char *data, int sz);

	/*
	*	entity meta information
	*/
	void length(int len);
	int length() const { return ::atoi(header("Content-Length", "0").c_str()); }
	
	void md5(const std::string &md5) { header("Content-MD5", md5); }
	std::string md5() const { return header("Content-MD5"); }

	void type(const std::string &type) { header("Content-Type", type); }
	std::string type() const { return header("Content-Type"); }

	void range(const std::string &range) { header("Content-Range", range); }
	std::string range() const { return header("Content-Range"); }

	void allow(const std::string &allow) { header("Allow", allow); }
	std::string allow() const { return header("Allow"); }

	void expires(const std::string &expires) { header("Expires", expires); }
	std::string expires() const { return header("Expires"); }

	void encoding(const std::string &encoding) { header("Content-Encoding", encoding); }
	std::string encoding() const { return header("Content-Encoding"); }

	void language(const std::string &language) { header("Content-Language", language); }
	std::string language() const { return header("Content-Language"); }

	void location(const std::string &location) { header("Content-Location", location); }
	std::string location() const { return header("Content-Location"); }

	void lastmodified(const std::string &lastmodified) { header("Last-Modified", lastmodified); }
	std::string lastmodified() const { return header("Last-Modified"); }

private:
	/*
	*	make query line data
	*@return:
	*	void
	*/
	void make();

	/*
	*	take data from entity stream
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

	/*
	*	feed data to entity stream
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz);

	/*
	*	check if entity is full(completed)
	*@return:
	*	true - entity is full(completed), false - not full(completed)
	*/
	bool full() const;

	/*
	*	get entity data
	*@return:
	*	entity data
	*/
	const std::string &data() const;

	/*
	*	get/set entity meta information by specified key
	*/
	std::map<std::string, std::string> header() const;
	void header(const std::string &key, const std::string &val);
	std::string header(const std::string &key, const char *default = "") const;

	/*
	*	get post params
	*/
	const http::params &params() const { return _params; }

private:
	//empty data
	std::string _empty;
	
	//request params by post method
	http::params _params;

	//content of entity
	std::unique_ptr<stream> _stream;

	//entity header items, <lower-key, <key, value>>
	std::map<std::string, std::pair<std::string, std::string>> _header;
};

//http request class
class request {
	//bad request execption
	typedef cexception error;

	friend class requestbuffer;
public:
	request() {}
	virtual ~request() {}

	/*
	*	make http request by get method
	*/
	void get(const char *urlformat, ...);

	/*
	*	make http request by post method
	*/
	void post(const char *url, const char *file);
	void post(const char *url, const char *data, int sz);

	/*
	*	get request query/header/content
	*/
	const query &query() const { return _query; }
	const header &header() const { return _header; }
	const entity &entity() const { return _entity; }

private:
	/*
	*	make header data
	*@return:
	*	void
	*/
	void make();

	/*
	*	take data from header stream
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

	/*
	*	feed data to header stream
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz);

	/*
	*	check if request is full(completed)
	*@return:
	*	true - request if full(completed), false - not full(completed)
	*/
	bool full() const;

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
	//bad request execption
	typedef cexception error;

	friend class responsebuffer;
public:
	response() {}
	virtual ~response() {}

	/*
	*	success response with file/json/data, code: 200 OK
	*@param path: in, local file path
	*@param data: in, data to response
	*@param sz: in, data size
	*@return:
	*	void
	*/
	void file(const char *path);
	void json(const char *data, int sz);
	void data(const char *data, int sz);

	/*
	*	client error: 4xx
	*@param code: in, client error code
	*@return:
	*	void
	*/
	void cerr(int code = status::bad_request);

	/*
	*	server error: 5xx
	*@param code: in, server error code
	*@return:
	*	void
	*/
	void serr(int code = status::interval_server_error);

	/*
	*	move to new location, code: 3xx
	*@param code: in, redirect code
	*@param url: in, new location
	*/
	void moveto(const char *url);

	/*
	*	redirect to new location, code: 3xx
	*@param code: in, redirect code
	*@param url: in, new location
	*/
	void redirect(const char *url);

	/*
	*	get/set response data
	*/
	const http::status &status() const { return _status; }
	const http::header &header() const { return _header; }
	const http::entity &entity() const { return _entity; }

private:
	/*
	*	make header data
	*@return:
	*	void
	*/
	void make();

	/*
	*	take data from header stream
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

	/*
	*	feed data to header stream
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz);

	/*
	*	check if response is full(completed)
	*@return:
	*	true - response if full(completed), false - not full(completed)
	*/
	bool full() const;
private:
	//response status
	http::status _status;
	//response header
	http::header _header;
	//response content
	http::entity _entity;
};

//request data buffer
class requestbuffer {
public:
	requestbuffer() {}
	virtual ~requestbuffer() {}

	/*
	*	make request data
	*@param req: in, request object
	*@return:
	*	void
	*/
	void make() { _request.make(); }

	/*
	*	take data from request buffer
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz) { return _request.take(data, sz); }

	/*
	*	feed data to request buffer
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz) { return _request.feed(data, sz); }

	/*
	*	check if request is full(completed)
	*@return:
	*	true - request if full(completed), false - not full(completed)
	*/
	bool full() const { return _request.full(); }

	/*
	*	get request object
	*/
	http::request &request() { return _request; }
	const http::request &request() const { return _request; }

private:
	//request object
	http::request _request;
};

class responsebuffer {
public:
	responsebuffer() {}
	virtual ~responsebuffer() {}

	/*
	*	make response data
	*@param req: in, response object
	*@return:
	*	void
	*/
	void make() { _response.make(); }

	/*
	*	take data from response buffer
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz) { return _response.take(data, sz); }

	/*
	*	feed data to response buffer
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz) { return _response.feed(data, sz); }

	/*
	*	check if response is full(completed)
	*@return:
	*	true - response if full(completed), false - not full(completed)
	*/
	bool full() const { return _response.full(); }

	/*
	*	get response object
	*/
	response &response() { return _response; }
	const http::response &response() const{ return _response; }
private:
	//response object
	http::response _response;
};

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
