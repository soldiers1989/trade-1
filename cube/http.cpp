#include "http.h"
#include "fd.h"
#include "str.h"
#include <ctime>
#include <stdarg.h>
#include <algorithm>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE
//////////////////////////////////////////charset class/////////////////////////////////////////
std::string charset::utf8("utf-8");
std::string charset::default("");

//////////////////////////////////////////mime class/////////////////////////////////////////
std::string mime::json::default("application/json");
std::string mime::octet::default("application/octet-stream");
std::string mime::form::default("application/x-www-form-urlencoded");

std::string mime::json::utf8("application/json;charset=utf-8");
std::string mime::octet::utf8("application/octet-stream;charset=utf-8");
std::string mime::form::utf8("application/x-www-form-urlencoded;charset=utf-8");

std::string mime::json::gb2312("application/json;charset=gb2312");
std::string mime::octet::gb2312("application/octet-stream;charset=gb2312");
std::string mime::form::gb2312("application/x-www-form-urlencoded;charset=gb2312");

std::string mime::unknown("");

std::map<std::string, std::string> mime::_types;

mime::setter mime_json("json", "application/json");
mime::setter mime_octet("octet", "application/octet-stream");
mime::setter mime_form("form", "application/x-www-form-urlencoded");

std::string mime::get(const std::string &ext, const std::string &charset) {
	std::string res("");

	//get relate mime type
	std::map<std::string, std::string>::const_iterator citer = _types.find(ext);
	if (citer != _types.end()) {
		res.append(citer->second);
	}

	//append content charset
	if (!charset.empty()) {
		if(!res.empty())
			res.append(";charset=" + charset);
		else
			res.append("charset=" + charset);
	}

	return res;
}

void mime::set(const std::string &ext, const std::string &ctype) {
	_types[ext] = ctype;
}

//////////////////////////////////////////address class/////////////////////////////////////////
std::string address::get() const {
	int sz = 0;
	char data[BUFSZ] = { 0 };
	if (_port == 80)
		sz = snprintf(data, BUFSZ, "%s", _host.c_str());
	else
		sz = snprintf(data, BUFSZ, "%s:%d", _host.c_str(), _port);

	return std::string(data, sz);
}

int address::set(const char *data, int sz, std::string *err) {
	//find seperator of host and port
	const char *start = data, *end = data + sz, *pos = data;
	while (*pos != ':' && pos < end)
		pos++;

	//parse host and port
	std::string host(""), port("80");
	if (*pos == ':') {
		host = cube::str::strip(start, pos - start);
		port = cube::str::strip(pos + 1, end - pos - 1);
	} else {
		//only host found
		host = cube::str::strip(data, sz);
	}

	//check host and port
	if (host.empty()) {
		cube::safe_assign<std::string>(err, "address: empty host");
		return -1;
	}

	if (!cube::str::isdigit(port.c_str())) {
		cube::safe_assign<std::string>(err, str::format("address: %s, invalid port", port.c_str()));
		return -1;
	}

	//set host and port
	_host = host;
	_port = (ushort)::atoi(port.c_str());

	return sz;
}

//////////////////////////////////////////params class/////////////////////////////////////////
std::string params::get() const {
	//data buffer
	char data[BUFSZ] = { 0 };

	//output data
	int dsz = 0;
	bool first = true;
	std::map<std::string, std::vector<std::string>>::const_iterator iter = _params.begin(), iterend = _params.end();
	while (iter != iterend) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			if (first) {
				dsz += snprintf(data + dsz, BUFSZ - dsz, "%s=%s", str::escape(iter->first).c_str(), str::escape(iter->second[i]).c_str());
				first = false;
			} else {
				dsz += snprintf(data + dsz, BUFSZ - dsz, "&%s=%s", str::escape(iter->first).c_str(), str::escape(iter->second[i]).c_str());
			}
		}
	}

	return std::string(data, dsz);
}

int params::set(const char *data, int sz, std::string *err) {
	//split data by param seperator
	std::vector<std::string> items;
	str::strtok(data, sz, "&", items);

	//parse key and value of each param
	for (std::size_t i = 0; i < items.size(); i++) {
		std::size_t sep = items[i].find('=');
		if (sep != std::string::npos) {
			std::string key = str::unescape(items[i].substr(0, sep));
			std::string val = str::unescape(items[i].substr(sep + 1));
			_params[key].push_back(val);
		} else {
			cube::safe_assign<std::string>(err, str::format("params: %s, invalid param", items[i].c_str()));
			return -1;
		}
	}

	return 0;
}

std::vector<std::string> params::get(const std::string &key) const {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end())
		return std::vector<std::string>();

	return citer->second;
}

std::string params::get(const std::string &key, const char *default) const {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end() || citer->second.empty())
		return default;

	return citer->second[0];
}

//////////////////////////////////////////uri class/////////////////////////////////////////
std::string uri::get() const {
	//data buffer
	int sz = BUFSZ;
	char data[BUFSZ] = { 0 };

	//data pos
	int pos = 0;

	//add scheme
	if (!_scheme.empty()) {
		pos += snprintf(data + pos, sz - pos, "%s:", _scheme.c_str());
	}

	//add auth string
	if (!_auth.empty()) {
		pos += snprintf(data + pos, sz - pos, "//%s", _auth.c_str());
	}

	//add path string
	if (!_path.empty()) {
		pos += snprintf(data + pos, sz - pos, "/%s", _path.c_str());
	}

	//add query string
	if (!_query.empty()) {
		pos += snprintf(data + pos, sz - pos, "?%s", _query.c_str());
	}

	//add fragment string
	if (!_fragment.empty()) {
		pos += snprintf(data + pos, sz - pos, "#%s", _fragment.c_str());
	}

	return std::string(data, pos);
}

int uri::set(const char *data, int sz, std::string *err) {
	//skip space characters
	const char *start = data, *end = data + sz;
	while (::isspace(*start))
		start++;

	while (::isspace(*end))
		end--;

	if (start > end) {
		cube::safe_assign<std::string>(err, "uri: empty uri data.");
		return -1;
	}

	const char *pos = start;
	////parse scheme////
	//find scheme end flag
	while (*pos != ':' && pos < end)
		pos++;

	//save scheme if flag found
	if (*pos == ':') {
		_scheme = std::string(start, pos - start);
		start = ++pos;
	} else {
		pos = start;
	}

	////parse authority & address////
	//find authority start flag
	int slashnum = 0;
	while (slashnum != 2 && pos < end) {
		//skip space character
		if (::isspace(*pos)) {
			pos++;
			continue;
		}

		if (*pos == '/') {
			slashnum++;
			pos++;
		} else {
			//authority flag not found
			break;
		}
	}

	if (slashnum == 2) {
		//set authority start pos
		start = pos;

		//find authority end flag
		while (*pos != '/' && *pos != '?' && *pos != '#' && pos < end)
			pos++;

		//uri authority
		std::string auth = std::string(start, pos - start);

		//parse address
		if(_addr.set(auth.c_str(), auth.length(), err) != 0)
			return -1;

		//set authority
		_auth = auth;

		//reset start pos
		start = pos;
	} else {
		//authority flag not found, reset pos
		pos = start;
	}

	////parse path////
	if (*pos == '/' && pos < end) {
		//skip path start flag
		start = pos++;

		//find path end flag(query or fragment start flag)
		while (*pos != '?' && *pos != '#' && pos < end)
			pos++;

		//save path
		_path = std::string(start, pos - start);
	}

	////parse query & params////
	if (*pos == '?' && pos < end) {
		//skip query start flag
		start = ++pos;

		while (*pos != '#' && pos < end)
			pos++;

		//query string
		std::string query = std::string(start, pos - start);

		//parse params
		if(_params.set(query.c_str(), query.length(), err) != 0)
			return -1;

		//save query string
		_query = query;
	}

	////parse fragment////
	if (*pos == '#' && pos < end) {
		//skip fragment start flag
		start = ++pos;

		//save fragment
		_fragment = std::string(start, end - start);
	}

	return 0;
}

//////////////////////////////////////////http version class/////////////////////////////////////////
std::string version::get() const {
	//data buffer
	int sz = BUFSZ;
	char data[BUFSZ] = { 0 };

	//pack version
	sz = snprintf(data, sz, "%s/%s", _name.c_str(), _code.c_str());
	return std::string(data, sz);
}

int version::set(const char *data, int sz, std::string *err) {
	std::vector<std::string> items;
	str::strtok(data, sz, "/", items);
	if (items.size() != 2) {
		cube::safe_assign<std::string>(err, str::format("http version: %s, invalid http version", std::string(data,sz).c_str()));
		return -1;
	}

	//check protocol
	if (str::lower(items[0]) != "http") {
		cube::safe_assign<std::string>(err, str::format("http version: %s, protocol not supported", items[0].c_str()));
		return -1;
	}

	//set name & code
	_name = items[0];
	_code = items[1];

	return 0;
}
//////////////////////////////////////////query class///////////////////////////////////////////
std::string query::get() const {
	int sz = BUFSZ;
	char data[BUFSZ] = { 0 };

	sz = snprintf(data, sz, "%s %s %s\r\n", _method.c_str(), _uri.get().c_str(), _version.get().c_str());
	return std::string(data, sz);
}

int query::set(const char *data, int sz, std::string *err) {
	std::vector<std::string> items;
	cube::str::strtok(data, sz, " ", items, 3);
	if (items.size() != 3) {
		cube::safe_assign<std::string>(err, str::format("query line: %s, invalid request", std::string(data, sz).c_str()));
		return -1;
	}

	//parse method
	_method = items[0];

	//parse query
	if(_uri.set(items[1].c_str(), items[1].length(), err) != 0)
		return -1;

	//parse protocol & version
	if(_version.set(items[2].c_str(), items[2].length(), err) != 0)
		return -1;

	return 0;
}

/////////////////////////////////////////status class/////////////////////////////////////////////
std::map<int, std::pair<std::string, std::string>> status::_status;
status::setter s_ok(200, "OK");
status::setter r_moved_permanently(301, "Moved Permanently");
status::setter r_moved_temporarily(302, "Found");
status::setter cerr_bad_request(400, "Bad Request");
status::setter cerr_not_found(404, "Not Found");
status::setter cerr_method_not_allowed(405, "Method Not Allowed");
status::setter serr_interval_server_error(500, "Internal Server Error");

std::string status::get() const {
	int sz = BUFSZ;
	char data[BUFSZ] = { 0 };

	sz = snprintf(data, sz, "%s %s %s\r\n", _version.get().c_str(), _code.c_str(), _reason.c_str());
	return std::string(data, sz);
}

int status::set(int code, std::string *err) {
	std::map<int, std::pair<std::string, std::string>>::const_iterator citer = _status.find(code);
	if (citer == _status.end()) {
		cube::safe_assign<std::string>(err, str::format("status line: %d, not supported", code));
		return -1;
	}

	//set code & reason
	_code = citer->second.first;
	_reason = citer->second.second;

	return 0;
}

int status::set(const char *data, int sz, std::string *err) {
	//split status line
	std::vector<std::string> items;
	cube::str::strtok(data, sz, " ", items, 3);
	if (items.size() != 3) {
		cube::safe_assign<std::string>(err, str::format("status line: %s, invalid response", std::string(data, sz).c_str()));
		return -1;
	}

	//parse http version
	if(_version.set(items[0].c_str(), items[0].length(), err) != 0)
		return -1;

	//parse status code
	_code = items[1];

	//parse status phrase reason
	_reason = items[2];

	return 0;
}

//////////////////////////////////////////cookie class/////////////////////////////////////////
cookie::cookie(const std::string &name, const std::string &value) : _name(name), _value(value), _domain(""), _path(""), _expires(0), _maxage(0) {

}

cookie::cookie(const std::string &name, const std::string &value, const std::string &domain, const std::string &path, int maxage) : _name(name), _value(value), _domain(domain), _path(path), _maxage(maxage) {
	_expires = time(0) + _maxage; 
}

const std::string &cookie::expires() const { 
	ctime(&_expires); 
}

//////////////////////////////////////////cookies class/////////////////////////////////////////
std::string cookies::get(const std::string &name) {
	std::map<std::string, cookie>::const_iterator citer = _cookies.find(name);
	if (citer != _cookies.end()) {
		return citer->second.value;
	}
	return "";
}

void cookies::set(const std::string &name, const std::string &value, const std::string &domain, const std::string &path, int maxage) {
	_cookies[name] = cookie(name, value, domain, path, maxage);
}

//////////////////////////////////////////session class/////////////////////////////////////////
session::session(const std::string &id, int maxage) : _id(id), _maxage(maxage){
	_expires = time(0) + _maxage;
}

bool session::aged(time_t now) {
	if (now > _expires)
		return true;
	return false;
}

std::string session::get(const std::string &name) {
	std::map<std::string, std::string>::const_iterator citer = _items.find(name);
	if (citer != _items.end()) {
		return citer->second;
	}
	return "";
}

void session::set(const std::string &name, const std::string &value) {
	_items[name] = value;
}

//////////////////////////////////////////sessions class/////////////////////////////////////////
//default session id length
int sessions::_length = 16;
//default session life time 1 day
int sessions::_life = 86400;
//global sessions
std::mutex sessions::_mutex;
std::map<std::string, session> sessions::_sessions;

void sessions::aging() {
	std::unique_lock<std::mutex> lck(_mutex);
	time_t now = time(0);
	std::map<std::string, session>::iterator iter = _sessions.begin(), iterend = _sessions.end();
	while (iter != iterend) {
		if (iter->second.aged(now))
			_sessions.erase(iter++);
		else
			iter++;
	}
}

void sessions::life(int secs) {
	std::unique_lock<std::mutex> lck(_mutex);
	_life = secs;
}

void sessions::length(int len) {
	std::unique_lock<std::mutex> lck(_mutex);
	_length = len;
}

session &sessions::gen(int age) {
	std::unique_lock<std::mutex> lck(_mutex);
	//generate session id
	std::string id = cube::str::random(_length);
	while (_sessions.find(id) != _sessions.end()) {
		id = cube::str::random(_length);
	}

	//add new session
	_sessions[id] = session(id, age);

	return _sessions[id];
}

session &sessions::get(const std::string &sid) {
	std::unique_lock<std::mutex> lck(_mutex);
	return _sessions[sid]; 
}

//////////////////////////////////////////header class/////////////////////////////////////////
std::map<std::string, std::string> http::header::request::_header;
std::map<std::string, std::string> http::header::response::_header;

http::header::request::setter request_accept("Accept", "*/*");
http::header::request::setter request_set_user_agent("User-Agent", "cube");
http::header::request::setter request_accept_encoding("Accept-Encoding", "gzip, deflate");
http::header::response::setter response_server("Server", "Cube/1.0");

std::string header::get() const {
	//header data
	int sz = 0;
	char data[BUFSZ] = { 0 };

	//process each item
	header::items::const_iterator iter = _items.begin(), iterend = _items.end();
	while (iter != iterend) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			sz += snprintf(data + sz, BUFSZ - sz, "%s: %s\r\n", iter->second[i].first.c_str(), iter->second[i].second.c_str());
		}
		iter++;
	}

	//add last "\r\n"
	sz += snprintf(data + sz, BUFSZ - sz, "\r\n");
	return std::string(data, sz);
}

int header::set(const char *data, int sz, std::string *err) {
	//check data
	std::vector<std::string> item;
	str::strtok(data, sz, ":", item, 2);
	if (item.size() != 2) {
		cube::safe_assign<std::string>(err, str::format("header: %s invalid header", std::string(data, sz).c_str()));
		return -1;
	}

	//parse header
	std::string key = str::lower(item[0]);
	header::items::iterator iter = _items.find(key);
	if (iter == _items.end()) {
		_items.insert(std::pair<std::string, header::keyvals>(key, header::keyvals()));
	}
	_items[key].push_back(header::keyval(item[0], item[1]));

	return 0;
}

int header::sets(const char *data, int sz, std::string *err) {
	//seperate all header items
	std::vector<std::string> items;
	str::strtok(data, sz, "\r\n", items);

	//parse each header item
	for (size_t i = 0; i < items.size(); i++) {
		if(set(items[i].c_str(), items[i].length(), err) != 0)
			return -1;
	}

	return 0;
}

header &header::set(const std::string &key, const char *format, ...) {
	//format value string
	static const int BUFSZ = 2048;
	char buf[BUFSZ] = { 0 };
	va_list va;
	va_start(va, format);
	vsnprintf(buf, BUFSZ, format, va);
	va_end(va);

	//formatted value
	std::string val(buf);

	//set header value
	_items[key] = header::keyvals();
	_items[key].push_back(header::keyval(key, val));

	return *this;
}

header& header::set(const std::string &key, bool replace, const char *format, ...) {
	//format value string
	static const int BUFSZ = 2048;
	char buf[BUFSZ] = { 0 };
	va_list va;
	va_start(va, format);
	vsnprintf(buf, BUFSZ, format, va);
	va_end(va);

	//formatted value
	std::string val(buf);

	//set header value
	header::items::iterator iter = _items.find(key);
	if (iter != _items.end()) {
		if (replace) {
			iter->second.clear();
		}
		iter->second.push_back(header::keyval(key, val));
	} else {
		_items[key] = header::keyvals();
		_items[key].push_back(header::keyval(key, val));
	}

	return *this;
}

header &header::set(const std::map<std::string, std::string> &items, bool replace) {
	std::map<std::string, std::string>::const_iterator citer = items.begin(), citerend = items.end();
	while (citer != citerend) {
		std::string key = cube::str::lower(citer->first);
		header::items::iterator iter = _items.find(key);
		if (iter != _items.end()) {
			if (replace) {
				iter->second.clear();
			}
			iter->second.push_back(header::keyval(citer->first, citer->second));
		} else {
			header::keyvals kvs;
			kvs.push_back(header::keyval(citer->first, citer->second));
			_items.insert(std::pair<std::string, header::keyvals>(citer->first, kvs));
		}

		citer++;
	}

	return *this;
}

std::vector<std::string> header::get(const std::string &item) const {
	std::vector<std::string> result;
	header::items::const_iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end()) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			result.push_back(iter->second[i].second);
		}
	}

	return result;
}

std::string header::get(const std::string &item, const char *default) const {
	header::items::const_iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end() && iter->second.size() > 0) {
		return iter->second[0].second;
	} else {
		return default;
	}
}

//////////////////////////////////////////entity class/////////////////////////////////////////
void entity::init(const http::header &header) {
	//initialize entity header
	entity::header("Allow", header.get("Allow", ""));
	entity::header("Expires", header.get("Expires", ""));
	entity::header("Content-MD5", header.get("Content-MD5", ""));
	entity::header("Content-Type", header.get("Content-Type", ""));
	entity::header("Last-Modified", header.get("Last-Modified", ""));
	entity::header("Content-Range", header.get("Content-Range", ""));
	entity::header("Content-Length", header.get("Content-Length", "0"));
	entity::header("Content-Location", header.get("Content-Location", ""));
	entity::header("Content-Encoding", header.get("Content-Encoding", ""));
	entity::header("Content-Language", header.get("Content-Language", ""));

	//create output stream
	int len = length();
	if (len > 0) {
		_stream = std::unique_ptr<stream>(new sizedstream(len));
	}
}

void entity::file(const std::string &path, const char* charset) {
	//set stream data
	_stream = std::unique_ptr<stream>(new filestream(path, std::ios::in | std::ios::binary));

	//get file extension
	std::string ext = fd::ext(path);

	//set content type
	entity::type(mime::get(ext, charset));

	//set content length
	entity::length(_stream->size());
}

void entity::form(const char *data, int sz, const char* charset) {
	//set content type
	entity::type(mime::get("form", charset));

	//set content length
	entity::length(sz);

	//set stream data
	_stream = std::unique_ptr<stream>(new stringstream());
	_stream->assign(std::string(data, sz));
}

void entity::data(const std::string &type, const char *data, int sz, const char* charset) {
	//set content type
	entity::type(mime::get(type, charset));

	//set content length
	entity::length(sz);

	//set stream data
	_stream = std::unique_ptr<stream>(new stringstream());
	_stream->assign(std::string(data, sz));
}

void entity::make() {

}

int entity::take(char *data, int sz) {
	if (_stream == nullptr) {
		return 0;
	}

	return _stream->get(data, sz);
}

int entity::feed(const char *data, int sz) {
	if (_stream == nullptr) {
		return 0;
	}
	return _stream->put(data, sz);
}

bool entity::full() const {
	if (_stream == nullptr) {
		return true;
	}
	return _stream->endp();
}

const std::string &entity::data() {
	if (_stream == nullptr) {
		return _empty;
	}

	return _stream->data();
}

void entity::length(int len) {
	header("Content-Length", str::tostr(len));
}

std::map<std::string, std::string> entity::header() const {
	std::map<std::string, std::string> items;
	std::map<std::string, std::pair<std::string, std::string>>::const_iterator citer = _header.begin(), citerend = _header.end();
	while (citer != citerend) {
		items.insert(citer->second);
		citer++;
	}
	return items;
}

void entity::header(const std::string &key, const std::string &val) {
	if (!val.empty()) {
		_header[str::lower(key)] = std::pair<std::string, std::string>(key, val);
	}
}

std::string entity::header(const std::string &key, const char *default) const {
	std::map<std::string, std::pair<std::string, std::string>>::const_iterator citer = _header.find(str::lower(key));
	if (citer != _header.end()) {
		return citer->second.second;
	}

	return std::string(default);
}
//////////////////////////////////////////request class/////////////////////////////////////////
void request::get(const char *urlformat, ...) {
	//format url string
	char url[BUFSZ] = { 0 };
	va_list va;
	va_start(va, urlformat);
	int sz = vsnprintf(url, BUFSZ, urlformat, va);
	va_end(va);

	//initialize query
	char query[BUFSZ] = { 0 };
	snprintf(query, BUFSZ, "GET %s HTTP/1.1\r\n", url);
	_query.init(query);

	//set general header
	_header.set(http::header::request::default());
}

void request::post(const char *url, const char *file) {
	//initialize query
	char query[BUFSZ] = { 0 };
	snprintf(query, BUFSZ, "POST %s HTTP/1.1\r\n", url);
	_query.init(query);
	
	//set general header
	_header.set(http::header::request::default());

	//set post entity
	_entity.file(file);
}

void request::post(const char *url, const char *data, int sz) {
	//initialize query
	char query[BUFSZ] = { 0 };
	snprintf(query, BUFSZ, "POST %s HTTP/1.1\r\n", url);
	_query.init(query);

	//set general header
	_header.set(http::header::request::default());

	//set entity data
	_entity.data(mime::octet::default, data, sz);
}

void request::make() {
	//make query line
	_query.make();

	//make query entity
	_entity.make();

	//set entity header
	_header.set(_entity.header());

	//make request header
	_header.make();
}

int request::take(char *data, int sz) {
	//taked size
	int rsz = 0;

	//take query line
	if (rsz < sz) {
		rsz += _query.take(data + rsz, sz - rsz);
	}

	//take header data
	if (rsz < sz) {
		rsz += _header.take(data + rsz, sz - rsz);
	}

	//take entity data
	if (rsz < sz) {
		rsz += _entity.take(data + rsz, sz - rsz);
	}

	return rsz;
}

int request::feed(const char *data, int sz) {
	//feed size
	int wsz = 0;

	//feed query line
	if (wsz < sz) {
		wsz += _query.feed(data + wsz, sz - wsz);
	}

	//feed header data
	if (wsz < sz) {
		wsz += _header.feed(data + wsz, sz - wsz);

		//initialize entity
		if (_header.full()) {
			_entity.init(_header);
		}
	}

	//feed entity data
	if (wsz < sz) {
		wsz += _entity.feed(data + wsz, sz - wsz);
	}

	return wsz;
}

bool request::full() const {
	return _query.full() && _header.full() && _entity.full();
}

/////////////////////////////////////////response class///////////////////////////////////////////
void response::file(const char *path, const char* charset) {
	//set status line
	_status.init(200);

	//set general header
	_header.set(http::header::response::default());

	//set entity data
	_entity.file(path, charset);
}

void response::json(const char *data, int sz, const char* charset) {
	//set status line
	_status.init(200);

	//set general header
	_header.set(http::header::response::default());

	//set entity data
	_entity.data("json", data, sz, charset);
}

void response::data(const char *data, int sz, const char* charset) {
	//set status line
	_status.init(200);

	//set general header
	_header.set(http::header::response::default());

	//set entity data
	_entity.data("octet", data, sz, charset);
}

void response::cerr(int code) {
	//set status line
	_status.init(code);

	//set general header
	_header.set(http::header::response::default());
}

void response::serr(int code) {
	//set status line
	_status.init(code);

	//set general header
	_header.set(http::header::response::default());
}

void response::moveto(const char *url) {
	//set status line
	_status.init(301);

	//set general header
	_header.set(http::header::response::default());

	//set redirect location
	_header.set("Location", url);
}

void response::redirect(const char *url) {
	//set status line
	_status.init(302);
	
	//set general header
	_header.set(http::header::response::default());

	//set redirect location
	_header.set("Location", url);
}


void response::make() {
	//make status line
	_status.make();

	//make entity
	_entity.make();

	//set entity header
	_header.set(_entity.header());

	//make headers
	_header.make();
}

int response::take(char *data, int sz) {
	//taked size
	int rsz = 0;

	//take status line
	if (rsz < sz) {
		rsz += _status.take(data + rsz, sz - rsz);
	}

	//take header data
	if (rsz < sz) {
		rsz += _header.take(data + rsz, sz - rsz);
	}

	//take entity data
	if (rsz < sz) {
		rsz += _entity.take(data + rsz, sz - rsz);
	}

	return rsz;
}

int response::feed(const char *data, int sz) {
	//feed size
	int wsz = 0;

	//feed status line
	if (wsz < sz) {
		wsz += _status.feed(data + wsz, sz - wsz);
	}

	//feed header data
	if (wsz < sz) {
		wsz += _header.feed(data + wsz, sz - wsz);

		//initialize entity
		if (_header.full()) {
			_entity.init(_header);
		}
	}

	//feed entity data
	if (wsz < sz) {
		wsz += _entity.feed(data + wsz, sz - wsz);
	}

	return wsz;
}

bool response::full() const {
	return _status.full() && _header.full() && _entity.full();
}

////////////////////////http file stream/////////////////////////////

int fstream::take(char *data, int sz) {
	if (!eof()) {
		read(data, sz);
		return (int)gcount();
	}
	return 0;
}

int fstream::feed(const char *data, int sz) {
	write(data, sz);
	return sz;
}

////////////////////////http head stream/////////////////////////////
const std::string hstream::_crlf = "\r\n\r\n";

int hstream::take(char *data, int sz) {
	if (!eof()) {
		read(data, sz);
		return (int)gcount();
	}
	return 0;
}

int hstream::feed(const char *data, int sz) {
	//stream not completed, need more data
	if (!_completed) {
		//restore last crlf match result
		int szcrlf = _crlf.length();
		const char *crlf = _crlf.c_str(), *pcrlf = crlf + _pos;

		//continue check the end tag
		const char *pdata = data, *sdata = data;
		while (pdata - data < sz && pcrlf - crlf < szcrlf) {
			if (*pcrlf != *pdata) {
				//move data pos to next position
				sdata = ++pdata;
				//reset crlf pos
				pcrlf = crlf;
			} else {
				pdata++;
				pcrlf++;
			}
		}

		//crlf found in stream
		if (pcrlf - crlf == szcrlf) {
			//set completed flag
			_completed = true;
			//write data
			int wsz = pdata - data;
			write(data, wsz);
			//return write size
			return wsz;
		}

		//crlf not found, save current matched pos
		_pos = pcrlf - crlf;
		//write all data
		write(data, sz);
		//all data feeded
		return sz;
	}

	//stream has completed
	return 0;
}

////////////////////////http string stream/////////////////////////////
int sstream::take(char *data, int sz) {
	if (!eof()) {
		read(data, sz);
		return (int)gcount();
	}
	return 0;
}

int sstream::feed(const char *data, int sz) {
	write(data, sz);
	return sz;
}

////////////////////////http parser/////////////////////////////
const int parser::BUFSZ = 4*1024; //max line size 4KB

int parser::parse(hstream &head, request &req, std::string *err) {
	//string line
	char buf[BUFSZ] = { 0 };

	//parse query line
	head.getline(buf, BUFSZ);

	//parse headers
	while (!head.endg()) {

		head.getline(buf, BUFSZ);
	}

	//parse success
	return 0;
}

int parser::parse(hstream &head, response &resp, std::string *err) {

}

////////////////////////http packer/////////////////////////////
int packer::pack(request &req, hstream &head, std::string *err) {

}

int packer::pack(response &resp, hstream &head, std::string *err) {

}

////////////////////////http request stream/////////////////////////////
int rqstream::take(char *data, int sz) {
	int tsz = 0;
	if (_head != nullptr && !_head->endg()) {
		tsz = _head->take(data + tsz, sz - tsz);
	}

	if (_body != nullptr && !_body->endg()) {
		tsz = _body->take(data + tsz , sz - tsz);
	}

	return tsz;
}

int rqstream::feed(const char *data, int sz) {

	return 0;
}

////////////////////////http response stream/////////////////////////////
int rpstream::take(char *data, int sz) {
	return 0;
}

int rpstream::feed(const char *data, int sz) {
	return 0;
}
END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
