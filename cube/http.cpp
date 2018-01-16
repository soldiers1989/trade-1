#include "http.h"
#include "str.h"
#include <stdarg.h>
#include <algorithm>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//////////////////////////////////////////address class/////////////////////////////////////////
void addr::parse() {
	const char *start = _data.c_str(), *end = _data.c_str() + _data.length();
	
	//find seperator of host and port
	const char *pos = start;
	while (*pos != ':' && pos < end)
		pos++;

	//parse host and port
	std::string host(""), port("80");
	if (*pos == ':') {
		host = cube::str::strip(start, pos - start);
		port = cube::str::strip(pos + 1, end - pos - 1);
	} else {
		//only host found
		host = cube::str::strip(_data);
	}

	//check host and port
	if (host.empty()) {
		throw error("address: empty host");
	}

	if (!cube::str::isdigit(port.c_str())) {
		throw error("address: %s, invalid port", port.c_str());
	}

	//set host and port
	_host = host;
	_port = (ushort)::atoi(port.c_str());
}

void addr::parse(const std::string &str) {
	//set data
	_data = str;

	//parse data
	parse();
}

void addr::pack() {
	//ignore default port
	if (_port == 80) {
		_data = _host;
	}

	//pack host & port
	cube::str::format(_data, "%s:%d", _host.c_str(), _port);
}

//////////////////////////////////////////parameters class/////////////////////////////////////////
void params::parse() {
	const char *SEP = "&";
	//split params
	std::vector<std::string> items;
	cube::str::strtok(_data.c_str(), _data.length(), SEP, items);

	//parse each param
	for (std::size_t i = 0; i < items.size(); i++) {
		std::size_t sep = items[i].find('=');
		if (sep != std::string::npos) {
			std::string key = cube::str::strip(items[i].substr(0, sep));
			std::string val = cube::str::strip(items[i].substr(sep + 1));
			if (!key.empty()) {
				//unescape key
				key = cube::str::unescape(key);
				if (_params.find(key) == _params.end()) {
					_params.insert(std::pair<std::string, std::vector<std::string>>(key, std::vector<std::string>()));
				}

				//unescape value
				val = cube::str::unescape(val);
				_params[key].push_back(val);
			}
		}
	}
}

void params::parse(const std::string &str) {
	//clear old params
	_params.clear();

	//set params data
	_data = str;

	//parse data
	parse();
}

void params::pack() {
	bool first = true;
	std::map<std::string, std::vector<std::string>>::iterator iter = _params.begin(), iterend = _params.end();
	while (iter != iterend) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			if (first) {
				_data.append(iter->first + "=" + iter->second[i]);
				first = false;
			} else {
				_data.append("&"+iter->first + "=" + iter->second[i]);
			}
		}
	}
}

void params::get(const std::string &key, std::string &val) {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer != _params.end() && !citer->second.empty())
		val = citer->second[0];
}

std::string params::get(const std::string &key, const char *default) {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end() || citer->second.empty())
		return default;

	return citer->second[0];
}

std::vector<std::string> params::gets(const std::string &key) {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end())
		return std::vector<std::string>();

	return citer->second;
}

void params::gets(const std::string &key, std::vector<std::string> &vals) {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer != _params.end())
		vals = citer->second;
}

//////////////////////////////////////////uri class/////////////////////////////////////////
void uri::parse() {
	const char *start = _data.c_str(), *end = _data.c_str()+_data.length();
	//skip head spaces
	while (::isspace(*start))
		start++;

	//skip end spaces
	while (::isspace(*end))
		end--;

	//input is spaces
	if (start > end) {
		throw error("uri: empty uri data.");
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

	////parse authority////
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

		//save authority
		_auth = std::string(start, pos - start);

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

	////parse query////
	if (*pos == '?' && pos < end) {
		//skip query start flag
		start = ++pos;

		while (*pos != '#' && pos < end)
			pos++;

		//save query
		_query = std::string(start, pos - start);
	}

	////parse params////
	if (!_query.empty()) {
		_params.parse(_query);
	}

	////parse fragment////
	if (*pos == '#' && pos < end) {
		//skip fragment start flag
		start = ++pos;

		//save fragment
		_fragment = std::string(start, end - start);
	}
}

void uri::parse(const std::string &str) {
	//set uri data
	_data = str;

	//parse data
	parse();
}

void uri::pack() {
	//clear data first
	_data.clear();

	//add scheme
	if (!_scheme.empty()) {
		_data.append(_scheme + ":");
	}

	//add auth string
	if (!_auth.empty()) {
		_data.append("//" + _auth);
	}

	//add path string
	if (!_path.empty()) {
		_data.append("/" + _path);
	}

	//add query string
	if (!_query.empty()) {
		_data.append("?" + _query);
	}

	//add fragment string
	if (!_fragment.empty()) {
		_data.append("#" + _fragment);
	}
}

//////////////////////////////////////////http version class/////////////////////////////////////////
//default http version
version version::DEFAULT("HTTP/1.1");

void version::parse() {
	std::vector<std::string> items = cube::str::split(_data.c_str(), _data.length(), '/');
	if (items.size() != 2) {
		throw error("http version: %s, invalid http version", _data.c_str());
	}

	//parse protocol
	std::string name = cube::str::lower(cube::str::strip(items[0]));
	if (name != "http") {
		throw error("http version: %s, protocol not supported", name.c_str());
	}

	//set protocol name & version code
	_name = name;
	_code = cube::str::strip(items[1]);
}

void version::parse(const std::string &str) {
	//set data
	_data = str;

	//parse http version
	parse();
}

void version::pack() {
	_data = _name + "/" + _code;
}

//////////////////////////////////////////method class///////////////////////////////////////////
method method::GET("GET");
method method::POST("POST");

void method::parse() {
	_name = cube::str::lower(cube::str::strip(_data));
	if (!support(_name)) {
		throw error("request: %s, method not support", _data.c_str());
	}
}

void method::parse(const std::string &str) {
	//set data
	_data = str;

	//parse method
	parse();
}

void method::pack() {
	_data = cube::str::upper(_name);
}

bool method::support(const std::string &mtd) {
	return mtd == "get" || mtd == "post";
}

//////////////////////////////////////////query class///////////////////////////////////////////
void query::make() {
	//make query data
	std::string data("");
	cube::str::format(data, "%s %s %s\r\n", _method.data().c_str(), _uri.data().c_str(), _version.data().c_str());
	
	//initialize stream
	_stream.data(data);
}

int query::read(char *data, int sz) {
	return _stream.read(data, sz);
}

int query::feed(const char *data, int sz) {
	//query data has completed, need no more data
	if (_stream.full()) {
		return 0;
	}

	//feed data to stream
	int szeat = _stream.write(data, sz);

	//parse query if completed
	if (_stream.full()) {
		parse();
	}

	//return size feeded
	return szeat;
}

void query::parse() {
	std::vector<std::string> reqs;
	cube::str::strtok(_stream.data().c_str(), _stream.data().length(), " ", 3);
	if (reqs.size() != 3) {
		throw error("request: %s, invalid request", _stream.data().c_str());
	}
	//parse method
	_method.parse((reqs[0]));
	
	//parse query
	_uri.parse(reqs[1]);
	
	//parse protocol & version
	_version.parse(reqs[2]);
}

void query::get(const char *uri_format, ...) {
	//set method
	_method = method::GET;

	//format uri string
	static const int BUFSZ = 2048;
	char buf[BUFSZ] = { 0 };
	va_list va;
	va_start(va, uri_format);
	vsnprintf(buf, BUFSZ, uri_format, va);
	va_end(va);
	
	//set uri
	_uri.parse(buf);

	//set version
	_version = version::DEFAULT;
}

void query::post(const char *uri_format, ...) {
	//set method
	_method = method::POST;
	
	//format uri string
	static const int BUFSZ = 2048;
	char buf[BUFSZ] = { 0 };
	va_list va;
	va_start(va, uri_format);
	vsnprintf(buf, BUFSZ, uri_format, va);
	va_end(va);

	//set uri
	_uri.parse(buf);

	//set version
	_version = version::DEFAULT;
}

/////////////////////////////////////////status class/////////////////////////////////////////////
status status::OK("HTTP/1.1 200 OK\r\n");
status status::MOVE("HTTP/1.1 301 Moved Permanently\r\n");
status status::REDIRECT("HTTP/1.1 302 Found\r\n");
status status::BAD("HTTP/1.1 400 Bad Request\r\n");
status status::ERR("HTTP/1.1 500 Internal Server Error\r\n");

void status::make() {

}

int status::read(char *data, int sz) {
	return _stream.read(data, sz);
}

int status::feed(const char *data, int sz) {
	//status line completed
	if (_stream.full()) {
		return 0;
	}

	//feed more data
	int szfeed = _stream.write(data, sz);

	//parse status line if it is completed
	if (_stream.full()) {
		//parse status line
		parse();
	}

	return szfeed;
}

void status::parse() {
	//check stream data
	if (!_stream.full()) {
		throw error("status: %s, incompleted status line", _stream.data().c_str());
	}

	//split status line
	std::vector<std::string> items = cube::str::strtok(_stream.data().c_str(), " ", 3);
	if (items.size() != 3) {
		throw error("response: %s, invalid status line", _stream.data().c_str());
	}

	//parse http version
	_version.parse(items[0]);

	//parse status code
	_code = cube::str::strip(items[1]);

	//parse status phrase reason
	_reason = cube::str::strip(items[2]);
}

//////////////////////////////////////////header class/////////////////////////////////////////
void header::make() {
	std::string data("");

	//process each item
	header::items::iterator iter = _items.begin(), iterend = _items.end();
	while (iter != iterend) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			data.append(iter->second[i].first + ": " + iter->second[i].second + "\r\n");
		}
	}

	//add last "\r\n"
	data.append("\r\n");

	//set stream data
	_stream.data(data);
}

int header::read(char *data, int sz) {
	return _stream.read(data, sz);
}

int header::feed(const char *data, int sz) {
	//header has completed, can not take more
	if (_stream.full()) {
		return 0;
	}

	//feed data to streamer
	int wsz= _stream.write(data, sz);

	//parse header if completed
	if (_stream.full()) {
		parse();
	}

	//return data feeded
	return wsz;
}

void header::parse() {
	//check if stream data is completed
	if (_stream.full()) {
		throw error("header: %s incompleted header", _stream.data().c_str());
	}

	//parse header items
	std::vector<std::string> items = cube::str::strtok(_stream.data().c_str(), _stream.data().length(), "\r\n");
	for (std::size_t i = 0; i < items.size(); i++) {
		std::size_t sep = items[i].find(':');
		if (sep != std::string::npos) {
			std::string key = cube::str::lower(cube::str::strip(items[i].substr(0, sep)));
			std::string val = cube::str::strip(items[i].substr(sep + 1));
			
			header::items::iterator iter = _items.find(key);
			if (iter != _items.end()) {
				iter->second.push_back(header::keyval(key, val));
			} else {
				header::keyvals kvs;
				kvs.push_back(header::keyval(key, val));
				_items.insert(std::pair<std::string, header::keyvals>(key, kvs));
			}
		}
	}
}

bool header::has(const std::string &key) {
	header::items::const_iterator iter = _items.find(cube::str::lower(key));
	if (iter != _items.end() && iter->second.size() > 0) {
		return true;
	}

	return false;
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
	}

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
		header::keyvals kvs;
		kvs.push_back(header::keyval(key, val));
		_items.insert(std::pair<std::string, header::keyvals>(key, kvs));
	}

	return *this;
}

std::string header::get(const std::string &item, const char *default) {
	header::items::iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end() && iter->second.size() > 0) {
		return iter->second[0].second;
	} else {
		return default;
	}
}

std::vector<std::string> header::gets(const std::string &item) {
	std::vector<std::string> result;
	header::items::iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end()) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			result.push_back(iter->second[i].second);
		}
	}
	
	return result;
}

//////////////////////////////////////////body class/////////////////////////////////////////
void body::make() {

}

int body::read(char *data, int sz) {
	return _stream.read(data, sz);
}

int body::feed(const char *data, int sz) {
	if (_stream.full())
		return 0;
	return _stream.write(data, sz);
}

//////////////////////////////////////////entity class/////////////////////////////////////////
void entity::make() {

}

int entity::read(char *data, int sz) {
	return 0;
}

int entity::feed(const char *data, int sz) {
	return 0;
}

//////////////////////////////////////////request class/////////////////////////////////////////
void request::make() {

}

int request::read(char *data, int sz) {
	int rsz = 0;

	//first: read query data
	if (sz - rsz > 0 && !_query.ends()) {
		rsz += _query.read(data + rsz, sz - rsz);
	}

	//second: read header data
	if (sz - rsz > 0 && !_query.ends()) {
		rsz += _query.read(data + rsz, sz - rsz);
	}

	//second: read entity data
	if (sz - rsz > 0 && !_query.ends()) {
		rsz += _query.read(data + rsz, sz - rsz);
	}

	return rsz;
}

int request::feed(const char *data, int sz) {
	int wsz = 0;
	//first: feed query if it is not completed
	if (sz - wsz > 0 && !_query.full()) {
		wsz += _query.feed(data + wsz, sz - wsz);
	}

	//second: feed header if it is not completed
	if (sz - wsz > 0 && !_header.full()) {
		wsz += _header.feed(data + wsz, sz - wsz);
	}

	//third: feed content if it is not completed
	if (sz - wsz > 0 && !_entity.full()) {
		wsz += _entity.feed(data + wsz, sz - wsz);
	}

	return wsz;
}

/////////////////////////////////////////response class///////////////////////////////////////////
void response::make() {
	//make status data
	_status.make();
	
	//make entity data
	_entity.make();

	//set entity header
	_header.set(_entity.headers());

	//make header data
	_header.make();
}

int response::read(char *data, int sz) {
	int rsz = 0;

	//first: read query data
	if (sz - rsz > 0 && !_status.ends()) {
		rsz += _status.read(data + rsz, sz - rsz);
	}

	//second: read header data
	if (sz - rsz > 0 && !_header.ends()) {
		rsz += _header.read(data + rsz, sz - rsz);
	}

	//second: read entity data
	if (sz - rsz > 0 && !_entity.ends()) {
		rsz += _entity.read(data + rsz, sz - rsz);
	}

	return rsz;
}

int response::feed(const char *data, int sz) {
	int wsz = 0;

	//first: feed query if it is not completed
	if (sz - wsz > 0 && !_status.full()) {
		wsz += _status.feed(data + wsz, sz - wsz);
	}

	//second: feed header if it is not completed
	if (sz - wsz > 0 && !_header.full()) {
		wsz += _header.feed(data + wsz, sz - wsz);
	}

	//third: feed content if it is not completed
	if (sz - wsz > 0 && !_entity.full()) {
		wsz += _entity.feed(data + wsz, sz - wsz);
	}

	return wsz;
}
END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
