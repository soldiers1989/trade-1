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
	if (_stream.completed()) {
		return 0;
	}

	//feed data to stream
	int szeat = _stream.write(data, sz);

	//parse query if completed
	if (_stream.completed()) {
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

//////////////////////////////////////////header class/////////////////////////////////////////
void header::make() {

}

int header::read(char *data, int sz) {
	return _stream.read(data, sz);
}

int header::write(const char *data, int sz) {
	//header has completed, can not take more
	if (_stream.completed()) {
		return 0;
	}

	//feed data to streamer
	int wsz= _stream.write(data, sz);

	//parse header if completed
	if (_stream.completed()) {
		int err = parse(_stream.data().c_str(), _stream.data().length());
		if (err != 0) {
			throw error("invalid header: %s, parse failed", _stream.data().c_str());
		}
	}

	//return data feeded
	return wsz;
}

int header::parse(const std::string &str) {
	return parse(str.c_str(), str.length());
}

int header::parse(const char *str, int sz) {
	const char *SEP = "\r\n";
	std::vector<std::string> items = cube::str::split(str, sz, SEP);
	for (std::size_t i = 0; i < items.size(); i++) {
		std::size_t sep = items[i].find(':');
		if (sep != std::string::npos) {
			std::string key = cube::str::lower(cube::str::strip(items[i].substr(0, sep)));
			std::string val = cube::str::strip(items[i].substr(sep + 1));
			if (!key.empty()) {
				if (_items.find(key) == _items.end()) {
					_items.insert(std::pair<std::string, std::vector<std::string>>(key, std::vector<std::string>()));
				}

				_items[key].push_back(val);
			}
		}
	}

	return 0;
}

bool header::has(const std::string &item) {
	std::map<std::string, std::vector<std::string>>::const_iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end() && iter->second.size() > 0) {
		return true;
	}

	return false;
}

header& header::set(const std::string &item, bool replace, const char *format, ...) {
	std::map<std::string, std::vector<std::string>>::iterator iter = _items.find(item);

	return *this;
}

std::string header::get(const std::string &item, const char *default) {
	std::map<std::string, std::vector<std::string>>::iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end() && iter->second.size() > 0) {
		return iter->second[0];
	} else {
		return default;
	}
}

std::vector<std::string> header::gets(const std::string &item) {
	std::map<std::string, std::vector<std::string>>::iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end())
		return iter->second;
	else
		return std::vector<std::string>();
}

//////////////////////////////////////////content class/////////////////////////////////////////
int content::write(const char *data, int sz) {
	return _stream.write(data, sz);
}

//////////////////////////////////////////request class/////////////////////////////////////////
int request::write(const char *data, int sz) {
	int wsz = 0;
	//first: feed query if it is not completed
	if (!_query.full()) {
		wsz += _query.feed(data, sz);
	}

	//second: feed header if it is not completed
	if (sz - wsz > 0 && !_header.completed()) {
		wsz += _header.write(data + wsz, sz - wsz);

		//try to get content length from header
		_content.size(::atoi(_header.get("content-length", "0").c_str()));
	}

	//third: feed content if it is not completed
	if (sz - wsz > 0 && !_content.completed()) {
		wsz += _content.write(data + wsz, sz - wsz);
	}

	return wsz;
}

/////////////////////////////////////////status class/////////////////////////////////////////////
void status::make() {

}

int status::read(char *data, int sz) {
	return 0;
}

int status::write(const char *data, int sz) {
	//feed data if status line not completed
	if (!_stream.completed()) {
		//feed more data
		int szfeed = _stream.write(data, sz);

		//parse status line if it is completed
		if (_stream.completed()) {
			//split status line
			std::vector<std::string> items = cube::str::strtok(_stream.data().c_str(), " ");
			if (items.size() != 3) {
				throw error("response: %s, invalid status line", _stream.data().c_str());
			}

			//parse http version

			//parse status code

			//parse status phrase reason
		}

		return szfeed;
	}

	//status has completed, can not take more data
	return 0;
}

/////////////////////////////////////////status specification class////////////////////////////////
const status &statuss::get(const std::string &code) {
	std::map<std::string, status>::iterator iter = statuss::_statuss.find(code);
	if (iter == statuss::_statuss.end()) {
		throw error("status spec: %s, is not support.", code.c_str());
	}

	return iter->second;
}

std::map<std::string, status> statuss::_statuss;

void statuss::set(const std::string &code, const status &status) {
	statuss::_statuss.insert(std::pair<std::string, http::status>(code, status));
}

/////////////////////////////////////////response class///////////////////////////////////////////
int response::write(const char *data, int sz) {
	return 0;
}

int response::read(char *data, int sz) {
	const char *resp = "HTTP/1.1 200 OK";
	memcpy(data, resp, strlen(resp));
	return 0;
}

/////////////////////////////////////////http global variable initialize///////////////////////////
statuss::setter set_status_200("1.1", "200", "OK");
statuss::setter set_status_400("1.1", "400", "Bad Request");

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
