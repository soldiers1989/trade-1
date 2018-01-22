#include "http.h"
#include "str.h"
#include <stdarg.h>
#include <algorithm>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE
//////////////////////////////////////////parser class/////////////////////////////////////////
std::string parser::data() {
	char buf[BUFSZ] = { 0 };
	int sz = pack(buf, BUFSZ);
	return std::string(buf, sz);
}

//////////////////////////////////////////address class/////////////////////////////////////////
int address::pack(char *data, int sz) {
	if (_port == 80)
		return snprintf(data, sz, "%s", _host.c_str());
	else
		return snprintf(data, sz, "%s:%d", _host.c_str(), _port);
}

int address::parse(const char *data, int sz) {
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
		throw error("address: empty host");
	}

	if (!cube::str::isdigit(port.c_str())) {
		throw error("address: %s, invalid port", port.c_str());
	}

	//set host and port
	_host = host;
	_port = (ushort)::atoi(port.c_str());

	return sz;
}

//////////////////////////////////////////parameters class/////////////////////////////////////////
int params::pack(char *data, int sz) {
	//data pos
	int pos = 0;
	
	//output data
	bool first = true;
	std::map<std::string, std::vector<std::string>>::iterator iter = _params.begin(), iterend = _params.end();
	while (iter != iterend) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			if (first) {
				pos += snprintf(data + pos, sz - pos, "%s=%s", str::escape(iter->first).c_str(), str::escape(iter->second[i]).c_str());
				first = false;
			} else {
				pos += snprintf(data + pos, sz - pos, "&%s=%s", str::escape(iter->first).c_str(), str::escape(iter->second[i]).c_str());
			}
		}
	}

	return pos;
}

int params::parse(const char *data, int sz) {
	//split data by param seperator
	std::vector<std::string> items;
	str::strtok(data, sz, "&", items);

	//parse key and value of each param
	for (std::size_t i = 0; i < items.size(); i++) {
		std::size_t sep = items[i].find('=');
		if (sep != std::string::npos) {
			std::string key = str::unescape(items[i].substr(0, sep));
			std::string val = str::unescape(items[i].substr(sep + 1));
			if (_params.find(key) == _params.end()) {
				_params.insert(std::pair<std::string, std::vector<std::string>>(key, std::vector<std::string>()));
			}
			_params[key].push_back(val);
		}
	}

	return sz;
}

std::vector<std::string> params::get(const std::string &key) {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end())
		return std::vector<std::string>();

	return citer->second;
}

std::string params::get(const std::string &key, const char *default) {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end() || citer->second.empty())
		return default;

	return citer->second[0];
}

//////////////////////////////////////////uri class/////////////////////////////////////////
int uri::pack(char *data, int sz) {
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

	return pos;
}

int uri::parse(const char *data, int sz) {
	//skip space characters
	const char *start = data, *end = data + sz;
	while (::isspace(*start))
		start++;

	while (::isspace(*end))
		end--;

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
		_addr.parse(auth.c_str(), auth.length());

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
		_params.parse(query.c_str(), query.length());

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

	return sz;
}

//////////////////////////////////////////http version class/////////////////////////////////////////
//default http version
version version::DEFAULT("HTTP/1.1");

int version::pack(char *data, int sz) {
	return snprintf(data, sz, "%s/%s", _name.c_str(), _code.c_str());
}

int version::parse(const char *data, int sz) {
	std::vector<std::string> items;
	str::strtok(data, sz, "/", items);
	if (items.size() != 2) {
		throw error("http version: %s, invalid http version", std::string(data,sz).c_str());
	}

	//check protocol
	if (str::lower(items[0]) != "http") {
		throw error("http version: %s, protocol not supported", items[0].c_str());
	}

	//set name & code
	_name = items[0];
	_code = items[1];

	return sz;
}
//////////////////////////////////////////query class///////////////////////////////////////////
void query::init(const std::string &data) {
	parse(data.c_str(), data.length());
}

int query::pack(char *data, int sz) {
	return snprintf(data, sz, "%s %s %s\r\n", _method.c_str(), _uri.data().c_str(), _version.data().c_str());
}

int query::parse(const char *data, int sz) {
	std::vector<std::string> items;
	cube::str::strtok(data, sz, " ", items, 3);
	if (items.size() != 3) {
		throw error("query line: %s, invalid request", std::string(data, sz).c_str());
	}

	//parse method
	_method = items[0];

	//parse query
	_uri.parse(items[1].c_str(), items[1].length());

	//parse protocol & version
	_version.parse(items[2].c_str(), items[2].length());

	return sz;
}

void query::make() {
	//pack query line
	char buf[BUFSZ] = { 0 };
	int sz = pack(buf, BUFSZ);

	//assign stream data
	_stream.assign(std::string(buf, sz));
}

int query::take(char *data, int sz) {
	return _stream.get(data, sz);
}

int query::feed(const char *data, int sz) {
	return _stream.put(data, sz);
}

const std::string &query::data() {
	return _stream.cdata();
}

/////////////////////////////////////////status class/////////////////////////////////////////////
status status::OK("HTTP/1.1 200 OK\r\n");
status status::MOVE("HTTP/1.1 301 Moved Permanently\r\n");
status status::REDIRECT("HTTP/1.1 302 Found\r\n");
status status::BAD("HTTP/1.1 400 Bad Request\r\n");
status status::ERR("HTTP/1.1 500 Internal Server Error\r\n");

void status::init(const std::string &data) {
	parse(data.c_str(), data.length());
}

int status::pack(char *data, int sz) {
	return snprintf(data, sz, "%s %s %s\r\n", _version.data().c_str(), _code.c_str(), _reason.c_str());
}

int status::parse(const char *data, int sz) {
	//split status line
	std::vector<std::string> items;
	cube::str::strtok(data, sz, " ", items, 3);
	if (items.size() != 3) {
		throw error("status line: %s, invalid response", std::string(data, sz).c_str());
	}

	//parse http version
	_version.parse(items[0].c_str(), items[0].length());

	//parse status code
	_code = items[1];

	//parse status phrase reason
	_reason = items[2];

	return sz;
}

void status::make() {
	//pack status line
	char buf[BUFSZ] = { 0 };
	int sz = pack(buf, BUFSZ);

	//assign stream data
	_stream.assign(std::string(buf, sz));
}

int status::take(char *data, int sz) {
	return _stream.get(data, sz);
}

int status::feed(const char *data, int sz) {
	return _stream.put(data, sz);
}

const std::string &status::data() {
	return _stream.cdata();
}

//////////////////////////////////////////header class/////////////////////////////////////////
void header::init(const std::string &data) {
	_items.clear();
	parse(data.c_str(), data.length());
}

int header::pack(char *data, int sz) {
	int pos = 0;
	//process each item
	header::items::iterator iter = _items.begin(), iterend = _items.end();
	while (iter != iterend) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			pos = snprintf(data + pos, sz - pos, "%s: %s\r\n", iter->second[i].first.c_str(), iter->second[i].second.c_str());
		}
	}

	//add last "\r\n"
	pos = snprintf(data + pos, sz - pos, "\r\n");
	return pos;
}

int header::parse(const char *data, int sz) {
	//seperate all header items
	std::vector<std::string> items;
	str::strtok(data, sz, "\r\n", items);

	//parse each header item
	for (size_t i = 0; i < items.size(); i++) {
		//check data
		std::vector<std::string> item;
		str::strtok(items[i].c_str(), items[i].size(), ":", item, 2);
		if (item.size() != 2) {
			throw error("header: %s invalid header", items[i].c_str());
		}

		//parse header
		std::string key = str::lower(item[0]);
		header::items::iterator iter = _items.find(key);
		if (iter == _items.end()) {
			_items.insert(std::pair<std::string, header::keyvals>(key, header::keyvals()));
		}
		_items[key].push_back(header::keyval(item[0], item[1]));
	}

	return sz;
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

std::vector<std::string> header::get(const std::string &item) {
	std::vector<std::string> result;
	header::items::iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end()) {
		for (size_t i = 0; i < iter->second.size(); i++) {
			result.push_back(iter->second[i].second);
		}
	}

	return result;
}

std::string header::get(const std::string &item, const char *default) {
	header::items::iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end() && iter->second.size() > 0) {
		return iter->second[0].second;
	} else {
		return default;
	}
}

void header::make() {
	//pack header
	char buf[BUFSZ] = { 0 };
	int sz = pack(buf, BUFSZ);

	//assign stream data
	_stream.assign(std::string(buf, sz));
}

int header::take(char *data, int sz) {
	return _stream.get(data, sz);
}

int header::feed(const char *data, int sz) {
	return _stream.put(data, sz);
}

const std::string &header::data() {
	return _stream.cdata();
}

//////////////////////////////////////////entity class/////////////////////////////////////////
int entity::pack(char *data, int sz) {
	return 0;
}

int entity::parse(const char *data, int sz) {
	return 0;
}

//////////////////////////////////////////request class/////////////////////////////////////////
std::string request::default::_header = "User-Agent: \r\n"\
										"Accept: *.*\r\n"\
										"Accept-Encoding: gzip, deflate\r\n";

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

	//initialize header
	_header.init(default::header());

	//initialize entity

}

void request::post(const char *url, const char *file) {

}

void request::post(const char *url, const char *data, int sz) {
	//initialize query
	char query[BUFSZ] = { 0 };
	snprintf(query, BUFSZ, "POST %s HTTP/1.1\r\n", url);
	_query.init(query);

	//initialize header
	_header.init(default::header());

	//initialize entity
}

void request::make() {
	_query.make();
}

int request::take(char *data, int sz) {
	return 0;
}

int request::feed(const char *data, int sz) {
	return 0;
}

const std::string &request::data() const{
	return "";
}

/////////////////////////////////////////response class///////////////////////////////////////////
void response::file(const char *path) {

}
void response::json(const char *data, int sz) {

}
void response::data(const char *data, int sz) {

}

void response::cerr(int code) {

}

void response::serr(int code) {

}

void response::redirect(int code, const char *url) {

}


void response::make() {

}

int response::take(char *data, int sz) {
	return 0;
}

int response::feed(const char *data, int sz) {
	return 0;
}

bool response::full() const {
	return false;
}

const std::string &response::data() const {
	return "";
}

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
