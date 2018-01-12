#include "http.h"
#include "str.h"
#include <algorithm>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//////////////////////////////////////////address class/////////////////////////////////////////
void addr::parse(const std::string &str, const char *default_port) {
	parse(str.c_str(), (int)str.length());
}

void addr::parse(const char *str, int sz, const char *default_port) {
	const char *start = str, *end = str + sz;
	
	//find seperator of host and port
	const char *pos = start;
	while (*pos != ':' && pos < end)
		pos++;

	//parse host and port
	std::string host(""), port(default_port);
	if (*pos == ':') {
		host = cube::str::strip(start, pos - start);
		port = cube::str::strip(pos + 1, end - pos - 1);
	} else {
		//only host found
		host = cube::str::strip(str);
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

//////////////////////////////////////////parameters class/////////////////////////////////////////
void params::parse(const std::string &str) {
	parse(str.c_str(), str.length());
}

void params::parse(const char *str, int sz) {
	const char *SEP = "&";
	std::vector<std::string> items = cube::str::splits(str, sz, SEP);
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

std::string params::get(const std::string &key) const {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end() || citer->second.empty())
		return "";

	return citer->second[0];
}

std::vector<std::string> params::gets(const std::string &key) const {
	std::map<std::string, std::vector<std::string>>::const_iterator citer = _params.find(key);
	if (citer == _params.end())
		return std::vector<std::string>();

	return citer->second;
}

//////////////////////////////////////////uri class/////////////////////////////////////////
void uri::parse(const std::string &str) {
	parse(str.c_str(), (int)str.length());
}

void uri::parse(const char *str, int sz) {
	const char *start = str, *end = str+sz;

	//skip head spaces
	while (::isspace(*start))
		start++;

	//skip end spaces
	while (::isspace(*end))
		end--;

	//input is spaces
	if (start > end) {
		return;
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

std::string uri::description() {
	return cube::str::format("scheme:%s\nauthority:%s\npath:%s\nquery:%s\nfragment:%s\n", _scheme.c_str(), _auth.c_str(), _path.c_str(), _query.c_str(), _fragment.c_str());
}

//////////////////////////////////////////version class/////////////////////////////////////////
std::string version::pack() {
	return _protocol + "/" + _version;
}

void version::parse(const std::string &str) {
	parse(str.c_str(), str.length());
}

void version::parse(const char *str, int sz) {
	std::vector<std::string> items = cube::str::split(str, sz, '/');
	if (items.size() != 2) {
		throw error("http version: %s, invalid http version", std::string(str, sz).c_str());
	}

	//parse protocol
	std::string protocol = cube::str::lower(cube::str::strip(items[0]));
	if (protocol != "http") {
		throw error("http version: %s, protocol not supported", protocol.c_str());
	}

	//set protocol & version
	_protocol = protocol;
	_version = cube::str::strip(items[1]);
}

//////////////////////////////////////////method class///////////////////////////////////////////
bool method::support(const std::string &mtd) {
	return mtd == "get" || mtd == "post";
}

//////////////////////////////////////////query class///////////////////////////////////////////
int query::write(const char *data, int sz) {
	//query data has completed, need no more data
	if (_stream.completed()) {
		return 0;
	}

	//feed data to stream
	int szeat = _stream.write(data, sz);

	//parse query if it is completed
	if (_stream.completed()) {
		std::vector<std::string> reqs = cube::str::splits(_stream.str().c_str(), _stream.str().length(), " ");
		if (reqs.size() != 3) {
			throw edata("request: %s, invalid request line", _stream.str().c_str());
		}
		//parse method
		std::string method = cube::str::lower(cube::str::strip(reqs[0]));
		if (!http::method::support(method)) {
			throw edata("request: %s, method not support", _stream.str().c_str());
		}

		//parse query
		std::string struri = cube::str::strip(reqs[1]);
		uri tmpuri;
		tmpuri.parse(struri);

		//parse protocol & version
		std::string strpv = cube::str::strip(reqs[2]);
		std::vector<std::string> pv = cube::str::splits(strpv.c_str(), strpv.length(), "/");
		if (pv.size() != 2) {
			throw edata("request: %s, invalid protocol/version", _stream.str().c_str());
		}
		std::string protocol = cube::str::lower(cube::str::strip(pv[0]));
		std::string version = cube::str::strip(pv[1]);

		if (protocol != "http") {
			throw edata("request: %s, invalid protocol", _stream.str().c_str());
		}

		//parse query success, save query items
		_method = method;
		_uri = struri;
		_version = version;

		//uri parse result
		_path = tmpuri.path();
		_params = tmpuri.params();
		_fragment = tmpuri.fragment();
	}

	//return size feeded
	return szeat;
}


//////////////////////////////////////////header class/////////////////////////////////////////
int header::write(const char *data, int sz) {
	//header has completed, can not take more
	if (_stream.completed()) {
		return 0;
	}

	//feed data to streamer
	int wsz= _stream.write(data, sz);

	//parse header if completed
	if (_stream.completed()) {
		int err = parse(_stream.str().c_str(), _stream.str().length());
		if (err != 0) {
			throw error("invalid header: %s, parse failed", _stream.str().c_str());
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

int header::geti(const std::string &item, int default) {
	std::map<std::string, std::vector<std::string>>::iterator iter = _items.find(cube::str::lower(item));
	if (iter != _items.end() && iter->second.size() > 0) {
		return ::atoi(iter->second[0].c_str());
	} else {
		return default;
	}
}

std::string header::gets(const std::string &item, const char *default) {
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
	if (!_query.completed()) {
		wsz += _query.write(data, sz);
	}

	//second: feed header if it is not completed
	if (sz - wsz > 0 && !_header.completed()) {
		wsz += _header.write(data + wsz, sz - wsz);

		//try to get content length from header
		_content.size(_header.geti("content-length", 0));
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

}

int status::write(const char *data, int sz) {
	//feed data if status line not completed
	if (!_stream.completed()) {
		//feed more data
		int szfeed = _stream.write(data, sz);

		//parse status line if it is completed
		if (_stream.completed()) {
			//split status line
			std::vector<std::string> items = cube::str::splits(_stream.str().c_str(), " ");
			if (items.size() != 3) {
				throw error("response: %s, invalid status line", _stream.str().c_str());
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
