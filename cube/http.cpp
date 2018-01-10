#include "http.h"
#include "str.h"
#include <algorithm>
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

//////////////////////////////////////////address class/////////////////////////////////////////
int addr::parse(const std::string &str) {
	return parse(str.c_str(), (int)str.length());
}

int addr::parse(const char *str, int sz) {
	const char *start = str, *end = str + sz;
	
	//find seperator of host and port
	const char *pos = start;
	while (*pos != ':' && pos < end)
		pos++;

	if (*pos == ':') {
		_host = cube::str::strip(start, pos - start);
		std::string port = cube::str::strip(pos + 1, end - pos - 1);
		if (cube::str::isdigit(port.c_str())) {
			_port = (ushort)::atoi(port.c_str());
		}
	} else {
		//only host found
		_host = cube::str::strip(str);
	}

	return 0;
}

//////////////////////////////////////////parameters class/////////////////////////////////////////
int params::parse(const std::string &str) {
	return parse(str.c_str(), str.length());
}

int params::parse(const char *str, int sz) {
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

	return 0;
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
uri::uri(const std::string &str) : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") {
	_parse(str);
}

uri::uri(const char *str, int sz) : _scheme(""), _auth(""), _path(""), _query(""), _fragment("") {
	_parse(str, sz);
}

uri* uri::parse(const std::string &str) {
	return new uri(str);
}

uri* uri::parse(const char *str, int sz) {
	return new uri(str, sz);
}

void uri::_parse(const std::string &str) {
	return _parse(str.c_str(), (int)str.length());
}

void uri::_parse(const char *str, int sz) {
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

//////////////////////////////////////////streamer class////////////////////////////////////////
int tagstreamer::feed(const char *data, int sz) {
	//streamer is full
	if (_completed) {
		return 0;
	 }

	//last tag match result
	const char *tag = _endtag.c_str(), *ptag = tag + _mtpos;
	int sztag = _endtag.length();

	//continue check the end tag
	const char *pdata = data, *stag = data;
	while (pdata - data < sz && ptag - tag < sztag) {
		if (*ptag != *pdata) {
			//reset tag pos
			ptag = tag;

			//move data pos to next start pos and reset tag start pos in data
			stag = ++pdata;
		} else {
			ptag++;
			pdata++;
		}
	}

	//full tag found for stream
	if (ptag - tag == sztag) {
		_completed = true;
		int szfeed = pdata - data;
		_data.append(data, szfeed);
		return szfeed;
	}

	//part tag found for stream, reset match tag pos
	_mtpos = ptag - tag;
	_data.append(data, sz);

	//all data feeded
	return sz;
}

//////////////////////////////////////////data stream class//////////////////////////////////////
int datastreamer::feed(const char *data, int sz) {
	//get want size
	int szwant = _szwant - _data.length();
	szwant = sz > szwant ? szwant : sz;

	//stream has completed
	if (szwant > 0) {
		_data.append(data, szwant);
	}
	
	return szwant;
}

//////////////////////////////////////////method class///////////////////////////////////////////
bool method::support(const std::string &mtd) {
	return mtd == "get" || mtd == "post";
}

//////////////////////////////////////////query class///////////////////////////////////////////
int query::feed(const char *data, int sz) {
	//feed data to streamer
	int szeat = _streamer.feed(data, sz);

	//query data feed completed
	if (szeat < sz && _streamer.completed()) {
		std::vector<std::string> reqs = cube::str::splits(_streamer.data().c_str(), _streamer.data().length(), " ");
		if (reqs.size() != 3) {
			throw edata("invalid query: %s", _streamer.data().c_str());
		}
		//parse method
		std::string method = cube::str::lower(cube::str::strip(reqs[0]));
		if (!http::method::support(method)) {
			throw edata("invalid query: %s, method not support", _streamer.data().c_str());
		}
		
		//parse query
		uri tmpuri;
		if (tmpuri.parse(cube::str::strip(reqs[1])) != 0) {
			throw edata("invalid query: %s, invalid query path", _streamer.data().c_str());
		}

		//parse protocol & version
		std::string strpv = cube::str::strip(reqs[2]);
		std::vector<std::string> pv = cube::str::splits(strpv.c_str(), strpv.length(), "/");
		if (pv.size() != 2) {
			throw edata("invalid query: %s, invalid protocol/version", _streamer.data().c_str());
		}
		std::string protocol = cube::str::lower(cube::str::strip(pv[0]));
		std::string version = cube::str::strip(pv[1]);

		if (protocol != "http") {
			throw edata("invalid query: %s, invalid protocol", _streamer.data().c_str());
		}

		//parse query success, save query items
		_method = method;
		_path = tmpuri.path();
		_params = tmpuri.params();
		_fragment = tmpuri.fragment();
		_version = version;
	}

	//return size feeded
	return szeat;
}


//////////////////////////////////////////header class/////////////////////////////////////////
int header::feed(const char *data, int sz) {
	//feed data to streamer
	int szeat = _streamer.feed(data, sz);

	//query data feed completed
	if (szeat < sz && _streamer.completed()) {
		int err = parse(_streamer.data().c_str(), _streamer.data().size());
		if (err != 0) {
			throw error("invalid header: %s, parse failed", _streamer.data().c_str());
		}
	}

	//return size feeded
	return szeat;
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
int content::feed(const char *data, int sz) {
	return _streamer.feed(data, sz);
}

//////////////////////////////////////////request class/////////////////////////////////////////
int request::feed(const char *data, int sz) {
	int szfeed = 0;
	//first: feed query if it is not completed
	if (!_query.completed()) {
		szfeed += _query.feed(data, sz);
	}

	//second: feed header if it is not completed
	if (sz - szfeed > 0 && !_header.completed()) {
		szfeed += _header.feed(data + szfeed, sz - szfeed);
	}

	//third: feed content if it is not completed
	if (sz - szfeed > 0 && !_content.completed()) {
		szfeed += _content.feed(data + szfeed, sz - szfeed);
	}

	return szfeed;
}
END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
