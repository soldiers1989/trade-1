#include "http.h"
#include "str.h"
#include <stdarg.h>
#include <algorithm>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//////////////////////////////////////////parser class/////////////////////////////////////////
std::string parser::take() {
	std::string data;
	take(data);
	return data;
}

int parser::take(std::string &data) {
	char buf[BUFSZ] = { 0 };
	int sz = take(buf, BUFSZ);
	data = std::string(buf, sz);
	return sz;
}

int parser::feed(const std::string &data) {
	return feed(data.c_str(), data.length());
}

//////////////////////////////////////////address class/////////////////////////////////////////
int address::take(char *data, int sz) {
	if (_port == 80)
		return snprintf(data, sz, "%s", _host.c_str());
	else
		return snprintf(data, sz, "%s:%d", _host.c_str(), _port);
}

int address::feed(const char *data, int sz) {
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
int params::take(char *data, int sz) {
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

int params::feed(const char *data, int sz) {
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
int uri::take(char *data, int sz) {
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

int uri::feed(const char *data, int sz) {
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
		_addr.feed(auth.c_str(), auth.length());

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
		_params.feed(query.c_str(), query.length());

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

int version::take(char *data, int sz) {
	return snprintf(data, sz, "%s/%s", _name.c_str(), _code.c_str());
}

int version::feed(const char *data, int sz) {
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
int query::take(char *data, int sz) {
	return snprintf(data, sz, "%s %s %s\r\n", _method.c_str(), ((parser*)&_uri)->take().c_str(), ((parser*)&_version)->take().c_str());
}

int query::feed(const char *data, int sz) {
	std::vector<std::string> items;
	cube::str::strtok(data, sz, " ", items, 3);
	if (items.size() != 3) {
		throw error("query line: %s, invalid request", std::string(data, sz).c_str());
	}

	//parse method
	_method = items[0];

	//parse query
	((parser*)&_uri)->feed(items[1]);

	//parse protocol & version
	((parser*)&_version)->feed(items[2]);

	return sz;
}

query& query::get(const char *format, ...) {
	//set method
	_method = "GET";

	//format uri string
	char buf[BUFSZ] = { 0 };
	va_list va;
	va_start(va, format);
	int sz = vsnprintf(buf, BUFSZ, format, va);
	va_end(va);
	
	//set uri
	_uri.feed(buf, sz);

	//set version
	_version = version::DEFAULT;

	return *this;
}

query& query::post(const char *format, ...) {
	//set method
	_method = "POST";
	
	//format uri string
	char buf[BUFSZ] = { 0 };
	va_list va;
	va_start(va, format);
	int sz = vsnprintf(buf, BUFSZ, format, va);
	va_end(va);

	//set uri
	_uri.feed(buf, sz);

	//set version
	_version = version::DEFAULT;

	return *this;

}

/////////////////////////////////////////status class/////////////////////////////////////////////
status status::OK("HTTP/1.1 200 OK\r\n");
status status::MOVE("HTTP/1.1 301 Moved Permanently\r\n");
status status::REDIRECT("HTTP/1.1 302 Found\r\n");
status status::BAD("HTTP/1.1 400 Bad Request\r\n");
status status::ERR("HTTP/1.1 500 Internal Server Error\r\n");

int status::take(char *data, int sz) {
	return 0;
}

int status::feed(const char *data, int sz) {
	//split status line
	std::vector<std::string> items;
	cube::str::strtok(data, sz, " ", items, 3);
	if (items.size() != 3) {
		throw error("status line: %s, invalid response", std::string(data, sz).c_str());
	}

	//parse http version
	_version.feed(items[0].c_str(), items[0].length());

	//parse status code
	_code = items[1];

	//parse status phrase reason
	_reason = items[2];

	return sz;
}

//////////////////////////////////////////header class/////////////////////////////////////////
int header::take(char *data, int sz) {
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

int header::feed(const char *data, int sz) {
	//check data
	std::vector<std::string> items;
	str::strtok(data, sz, ":", items, 2);
	if (items.size() != 2) {
		throw error("header: %s invalid header", std::string(data, sz).c_str());
	}

	//parse header
	std::string key = str::lower(items[0]);
	header::items::iterator iter = _items.find(key);
	if (iter == _items.end()) {
		_items.insert(std::pair<std::string, header::keyvals>(key, header::keyvals()));
	}
	_items[key].push_back(header::keyval(items[0], items[1]));

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

//////////////////////////////////////////entity class/////////////////////////////////////////
int entity::take(char *data, int sz) {
	return 0;
}

int entity::feed(const char *data, int sz) {
	return 0;
}

//////////////////////////////////////////request class/////////////////////////////////////////
int request::take(char *data, int sz) {
	return 0;
}

int request::feed(const char *data, int sz) {

	return 0;
}


/////////////////////////////////////////response class///////////////////////////////////////////
int response::take(char *data, int sz) {
	return 0;
}

int response::feed(const char *data, int sz) {

	return 0;
}
END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
