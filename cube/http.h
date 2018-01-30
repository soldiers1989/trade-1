/*
*	http - http protocol parser module
*/
#pragma once
#include "cube.h"
#include <map>
#include <mutex>
#include <vector>
#include <memory>
#include <fstream>
#include <sstream>
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
	static std::string default;
};

//mime class
class mime {
public:
	/*
	*	general mime types
	*/
	class form {
	public:
		static std::string utf8;
		static std::string gb2312;
		static std::string default;
	};
	class json {
	public:
		static std::string utf8;
		static std::string gb2312;
		static std::string default;
	};
	class octet {
	public:
		static std::string utf8;
		static std::string gb2312;
		static std::string default;
	};
	static std::string unknown;

	/*
	*	mime setter
	*/
	class setter {
	public:
		setter(const std::string &ext, const std::string &ctype) { set(ext, ctype); }
		~setter() {}
	};
public:
	/*
	*	get content type by extension name
	*/
	static std::string get(const std::string &ext, const std::string &charset);

	/*
	*	set content type by extension name & type
	*/
	static void set(const std::string &ext, const std::string &ctype);

private:
	//mime types, <extension, http content-type>
	static std::map<std::string, std::string> _types;
};

//address class
class address {
public:
	address() : _host(""), _port(0){ }
	virtual ~address() {}
	
	//get/set address with data string
	std::string get() const;
	int set(const char *data, int sz, std::string *err = 0);


	//get/set address properties
	const std::string& host() { return _host; }
	void host(const std::string &host) { _host = host; }
	ushort port() { return _port; }
	void port(ushort port) { _port = port; }
	
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

	//get/set params with data string
	std::string get() const;
	int set(const char *data, int sz, std::string *err = 0);

	/*
	*	get param value by specfied key
	*@param key: in, param key
	*@param val: in/out, value of specified key
	*@return:
	*	value of param
	*/
	std::vector<std::string> get(const std::string &key) const;
	std::string get(const std::string &key, const char *default) const;
private:
	//params
	std::map<std::string, std::vector<std::string>> _params;
};

//uri structure
//uri->[scheme:][//authority][/path][?query][#fragment]
//authority->[host:port]
class uri {
public:
	uri() : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") {}
	virtual ~uri() {}

	//get/set uri with data string
	std::string get() const;
	int set(const char *data, int sz, std::string *err = 0);

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
class version {
public:
	version() : _name("HTTP"), _code("1.1") {}
	virtual ~version() {}

	//get/set version with data string
	std::string get() const;
	int set(const char *data, int sz, std::string *err = 0);

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
class query {
public:
	query() : _method("") {}
	virtual ~query() {}

	//get/set query line with data string
	std::string get() const;
	int set(const char *data, int sz, std::string *err = 0);

	/*
	*	get query items parsed from data
	*/
	const std::string &method() const { return _method; }
	const std::string &path() const { return _uri.path(); }
	const params &params() const { return _uri.params(); }
	const std::string &fragment() const { return _uri.fragment(); }
	const std::string &version() const { return _version.code(); }

private:
	//request method
	std::string _method;
	//request uri
	http::uri _uri;
	//request http version
	http::version _version;
};

//response status line class
class status {
public:
	//status setter
	class setter {
	public:
		setter(int code, const std::string &reason) {
			status::_status[code] = std::pair<std::string, std::string>(str::tostr(code), reason);
		}
		~setter() {}
	};
	
	//default status, <int-code, <string-code, reason>>
	static std::map<int, std::pair<std::string, std::string>> _status;

public:
	status() : _code(""), _reason("") {}
	virtual ~status() {}

	//get/set query line with data string
	std::string get() const;
	int set(int code, std::string *err = 0);
	int set(const char *data, int sz, std::string *err = 0);

	//get/set status properties
	const std::string &code() { return _code; }
	void code(const std::string &code) { _code = code; }
	const std::string &version() { return _version.name(); }
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

//http cookie class
class cookie {
public:
	cookie() : _name(""), _value(""), _domain(""), _path(""), _expires(0), _maxage(0) {}
	cookie(const std::string &name, const std::string &value);
	cookie(const std::string &name, const std::string &value, const std::string &domain, const std::string &path, int maxage);
	~cookie() {}
	
	const std::string &name() const { return _name; }
	const std::string &value() const { return _value; }
	const std::string &domain() const { return _domain; }
	const std::string &path() const { return _path; }
	const std::string &expires() const;
	int maxage() const { return _maxage; }
private:
	std::string _name;
	std::string _value;

	std::string _domain;
	std::string _path;
	int _maxage;
	time_t _expires;
};

//http cookies class
class cookies {
public:
	cookies() {}
	~cookies() {}

	std::string get(const std::string &name);
	void set(const std::string &name, const std::string &value, const std::string &domain, const std::string &path, int maxage);
private:
	//cookie values
	std::map<std::string, cookie> _cookies;
};

//http session class
class session {
public:
	session() : _id(""), _maxage(0), _expires(0) {}
	session(const std::string &id, int maxage);
	~session() {}

	//test if session has aged
	bool aged(time_t now);

	//get/set session value
	std::string get(const std::string &name);
	void set(const std::string &name, const std::string &value);
private:
	//session id;
	std::string _id;
	//max age in seconds
	int _maxage;
	//expire time point
	time_t _expires;
	//session values
	std::map<std::string, std::string> _items;
};

//http sessions class
class sessions {
public:
	//aging out of life time sessions
	static void aging();
	
	//set default session life time in seconds
	static void life(int secs);
	//set default session id length
	static void length(int len);

	//generate a new session
	static session &gen(int age = sessions::_life);
	//get session by id
	static session &get(const std::string &sid);

private:
	//session id length
	static int _length;
	//default life time in seconds
	static int _life;
	//global sessions
	static std::mutex _mutex;
	static std::map<std::string, session> _sessions;
};

//header class
class header{
	typedef std::pair<std::string, std::string> keyval;
	typedef std::vector<keyval> keyvals;
	typedef std::map<std::string, keyvals> items;
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
	header() {}
	virtual ~header() { }

	//get/set header data string
	std::string get() const;
	int set(const char *data, int sz, std::string *err = 0);
	int sets(const char *data, int sz, std::string *err = 0);

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
	//header items, map<lower key, vector<<original key, value>>>
	header::items _items;
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
	void file(const std::string &path, const char *charset = "");

	/*
	*	initialize entity with form data
	*/
	void form(const char *data, int sz, const char *charset = "");

	/*
	*	initialize entity with specified content type & data
	*@param type: in, content type, xml/html/json/... .etc
	*@param data: in, content data
	*@param sz: in, content size
	*@return:
	*	void
	*/
	void data(const std::string &type, const char *data, int sz, const char *charset = "");

	/*
	*	entity meta information
	*/
	std::string type() const { return header("Content-Type"); }
	void type(const std::string &type) { header("Content-Type", type); }

	void length(int len);
	int length() const { return ::atoi(header("Content-Length", "0").c_str()); }

	void md5(const std::string &md5) { header("Content-MD5", md5); }
	std::string md5() const { return header("Content-MD5"); }

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
	*	make entity data
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
	const std::string &data();

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
	void file(const char *path, const char *charset = charset::default.c_str());
	void json(const char *data, int sz, const char *charset = charset::utf8.c_str());
	void data(const char *data, int sz, const char *charset = charset::default.c_str());

	/*
	*	client error: 4xx
	*@param code: in, client error code
	*@return:
	*	void
	*/
	void cerr(int code);

	/*
	*	server error: 5xx
	*@param code: in, server error code
	*@return:
	*	void
	*/
	void serr(int code);

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

//http stream base class
class stream {
public:
	/*
	*	take data from stream
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	virtual int take(char *data, int sz) = 0;

	/*
	*	feed data to stream
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	virtual int feed(const char *data, int sz) = 0;

	/*
	*	check if end of stream for get data
	*@return:
	*	true - end of stream, false - not end of stream
	*/
	virtual bool endg() = 0;
};

//http file stream
class fstream : public std::fstream, public stream {
public:
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	bool endg() { return eof(); }
};

//http head stream
class hstream : public std::stringstream, public stream {
public:
	hstream() : _pos(0), _completed(false), std::stringstream() {}
	hstream(const std::string &str) : _pos(0), _completed(true), std::stringstream(str) {}

	int take(char *data, int sz);
	int feed(const char *data, int sz);

	bool endg() { return eof(); }
private:
	//carriage return/line feed tag
	static const std::string _crlf;
	//current pos in crlf to compare
	int _pos;
	//stream completed
	bool _completed;
};

//http string stream
class sstream : public std::stringstream, public stream {
public:
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	bool endg() { return eof(); }
};

//http parser
class parser {
	typedef cexception error;
public:
	//line buffer size
	static const int BUFSZ;
public:
	/*
	*	parse request object from head data stream
	*/
	static int parse(hstream &head, request &req, std::string *err = 0);
	
	/*
	*	parse response object from head data stream
	*/
	static int parse(hstream &head, response &resp, std::string *err = 0);
};

//http packer
class packer {
	typedef cexception error;
public:
	/*
	*	pack request object to head data stream
	*/
	static int pack(request &req, hstream &head, std::string *err = 0);

	/*
	*	pack response object to respone data stream
	*/
	static int pack(response &resp, hstream &head, std::string *err = 0);
};

//http request stream
class rqstream {
public:
	rqstream() : _head(nullptr), _body(nullptr) {}
	~rqstream() {}

	/*
	*	take data from request buffer
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

	/*
	*	feed data to request buffer
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz);
	
public:
	http::request &request() { return _request; }
	const http::request &request() const { return _request; }

private:
	//request object
	http::request _request;

	//head data stream
	std::unique_ptr<hstream> _head;
	//body data stream
	std::unique_ptr<stream> _body;
};

//http response stream
class rpstream {
public:
	rpstream() : _head(nullptr), _body(nullptr) {}
	~rpstream() {}

	/*
	*	take data from request buffer
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

	/*
	*	feed data to request buffer
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded
	*/
	int feed(const char *data, int sz);

public:
	http::response &response() { return _response; }
	const http::response &response() const { return _response; }

private:
	//response object
	http::response _response;

	//head data stream
	std::unique_ptr<hstream> _head;
	//body data stream
	std::unique_ptr<stream> _body;
};

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
