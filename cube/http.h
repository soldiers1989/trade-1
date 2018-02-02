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

	virtual bool full() const = 0;

	virtual int size() const = 0;
};

//http file stream
class fstream : public std::fstream, public stream {
public:
	fstream(const std::string &path, std::ios::openmode mode = std::ios::in | std::ios::out) : std::fstream(path, mode) {}

	int take(char *data, int sz);
	int feed(const char *data, int sz);

	bool endg() { return eof(); }
	bool full() const { return false;}
	int size() const {return 0;}
};

//http head stream
class hstream : public std::stringstream, public stream {
public:
	hstream() : _pos(0), _completed(false), std::stringstream() {}
	hstream(const std::string &str) : _pos(0), _completed(true), std::stringstream(str) {}

	int take(char *data, int sz);
	int feed(const char *data, int sz);

	bool endg() { return eof(); }
	bool full() const { return _completed; }
	int size() const { return 0; }
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
	sstream() : _completed(false), std::stringstream() {}
	sstream(const std::string &data) : _completed(true), std::stringstream(data) {}
	~sstream() {}

	int take(char *data, int sz);
	int feed(const char *data, int sz);
	bool endg() { return eof(); }
	bool full() const { return _completed; }
	int size() const { return 0; }
private:
	//stream completed
	bool _completed;
};

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
	
	//pack/parse address with data string
	std::string pack() const;
	int parse(const char *data, int sz, std::string *err = 0);


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

	//pack/parse params with data string
	std::string pack() const;
	int parse(const char *data, int sz, std::string *err = 0);

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

	//pack/parse uri with data string
	std::string pack() const;
	int parse(const char *data, int sz, std::string *err = 0);

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

	//pack/parse version with data string
	std::string pack() const;
	int parse(const char *data, int sz, std::string *err = 0);

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

	//pack/parse query line with data string
	std::string pack() const;
	int parse(const char *data, std::string *err = 0);

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
		setter(int code, const std::string &reason);
		~setter() {}
	};
	
	//default status, <int-code, <string-code, reason>>
	static std::map<int, std::pair<std::string, std::string>> _status;

public:
	status() : _code(""), _reason("") {}
	virtual ~status() {}

	//pack/parse status line with string
	std::string pack() const;
	int parse(const char *str, std::string *err = 0);

	//set status with specified code
	int set(int code, std::string *err = 0);

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
	std::string expires() const;
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

//http body meta information
class meta {
public:
	meta() : _type(""), _lang(""), _encoding(""), _length(0), _range(""), _expires("") {}
	~meta() {}

	const std::string &type()  const { return _type; }
	void type(const std::string &type) { _type = type; }
	const std::string &lang()  const { return _lang; }
	void lang(const std::string &lang) { _lang = lang; }
	const std::string &encoding()  const { return _encoding; }
	void encoding(const std::string &encoding) { _encoding = encoding; }
	int length() const { return _length; }
	void length(int len) { _length = len; }
	const std::string &range()  const { return _range; }
	void range(const std::string &range) { _range = range; }
	const std::string &expires() const { return _expires; }
	void expires(const std::string &expires) { _expires = expires; }
private:
	int _length;
	std::string _type;
	std::string _lang;
	std::string _encoding;
	std::string _range;
	std::string _expires;
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
			setter(const std::string &key, const std::string &value) { http::header::request::set(key, value); }
			~setter() {}
		};

		static const std::map<std::string, std::string> &get() { return _header; }
		static void set(const std::string &key, const std::string &value) { _header[key] = value; }

	private:
		//default request header
		static std::map<std::string, std::string> _header;
	};

	//default response header class
	class response {
	public:
		class setter {
		public:
			setter(const std::string &key, const std::string &value) { http::header::response::set(key, value); }
			~setter() {}
		};

		static const std::map<std::string, std::string> &get() { return _header; }
		static void set(const std::string &key, const std::string &value) { _header[key] = value; }
	private:
		//default request header
		static std::map<std::string, std::string> _header;
	};
public:
	header() {}
	virtual ~header() { }

	/*
	*	pack header data
	*@return:
	*	header crlf feed
	*/
	std::string pack() const;

	/*
	*	parse header data
	*@return:
	*	0 for success, otherwise <0
	*/
	int parse(const char *str, std::string *err = 0);

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
	std::vector<std::string> get(const std::string &key) const;
	std::string get(const std::string &key, const char *default) const;

private:
	//header items, map<lower key, vector<<original key, value>>>
	header::items _items;
};

//http body class
class body {
	friend class request;
	friend class response;
public:
	body() : _stream(nullptr) {}
	virtual ~body() {}

	void init(const meta &meta);

	void file(const std::string &path, const char *charset = "");
	void form(const char *data, int sz, const char *charset = "");
	void data(const std::string &type, const char *data, int sz, const char *charset = "");

public:
	http::meta& meta() { return _meta; }
	const http::meta& meta() const { return _meta; }

private:
	int take(char *data, int sz);
	int feed(const char *data, int sz);

	bool done() const;
	
private:
	//body meta information
	http::meta _meta;
	
	//body data stream
	std::unique_ptr<stream> _stream;
};

//http request class
class request {
	friend class rqstream;

	//response head
	class head {
		friend class request;
	public:
		head() : _stream(nullptr) {}
		~head() {}

		http::query &query() { return _query; }
		const http::query &query() const { return _query; }

		http::header &header() { return _header; }
		const http::header &header() const { return _header; }

	private:
		int take(char *data, int sz, std::string *err = 0);
		int feed(const char *data, int sz, std::string *err = 0);

		bool done() const;

	private:
		//request line
		http::query _query;
		//request header
		http::header _header;

		//head data stream
		std::unique_ptr<hstream> _stream;
	};
public:
	request() {}
	virtual ~request() {}

	http::query &query() { return _head.query(); }
	const http::query &query() const { return _head.query(); }

	http::header &header() { return _head.header(); }
	const http::header &header() const { return _head.header(); }

private:
	int take(char *data, int sz);
	int feed(const char *data, int sz);
	bool done() const { return _head.done() && _body.done(); }

private:
	//request head
	head _head;
	//request body
	body _body;
};


//http response class
class response {
	friend class rpstream;

public:
	//response head
	class head {
		friend class response;
	public:
		head() : _stream(nullptr) {}
		~head() {}

		http::status &status() { return _status; }
		const http::status &status() const { return _status; }

		http::header &header() { return _header; }
		const http::header &header() const { return _header; }

	private:
		int take(char *data, int sz, std::string *err = 0);
		int feed(const char *data, int sz, std::string *err = 0);

		bool done() const;
	private:
		//response status
		http::status _status;
		//response header
		http::header _header;

		//head data stream
		std::unique_ptr<hstream> _stream;
	};

public:
	response() {}
	virtual ~response() {}

	/*
	*	informational: 1xx
	*/
	void info(int code);

	/*
	*	success: 2xx
	*/
	void succ(int code);

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
	*	jump to new location, code: 3xx
	*@param code: in, redirect code
	*@param url: in, new location
	*/
	void jump(const char *url, bool permanent = true);

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

public:
	http::status &status() { return _head.status(); }
	const http::status &status() const { return _head.status(); }

	http::header &header() { return _head.header(); }
	const http::header &header() const { return _head.header(); }

private:
	/*
	*	take data from request buffer
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked, <0 when error
	*/
	int take(char *data, int sz);

	/*
	*	feed data to request buffer
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded, <0 when error
	*/
	int feed(const char *data, int sz);

	/*
	*	check if request transfering has done
	*@return:
	*	true - request has done, false - not done
	*/
	bool done() const { return _head.done() && _body.done(); }

private:
	//response head
	head _head;
	//response body
	body _body;
};

//http request stream
class rqstream {
public:
	rqstream(){}
	~rqstream() {}

	/*
	*	take data from request buffer
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked, <0 when error
	*/
	int take(char *data, int sz) { return _request.take(data, sz); }

	/*
	*	feed data to request buffer
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded, <0 when error
	*/
	int feed(const char *data, int sz) { return _request.feed(data, sz); }
	
	/*
	*	check if request transfering has done
	*@return:
	*	true - request has done, false - not done
	*/
	bool done() const { return _request.done(); }

public:
	http::request &request() { return _request; }
	const http::request &request() const { return _request; }

private:
	//request object
	http::request _request;
};

//http response stream
class rpstream {
public:
	rpstream(){}
	~rpstream() {}

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
	*	check if response transfering has done
	*@return:
	*	true - response has done, false - not done
	*/
	bool done() const { return _response.done(); }
public:
	http::response &response() { return _response; }
	const http::response &response() const { return _response; }

private:
	//response object
	http::response _response;
};

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
