#include <algorithm>
#include "cube\log\log.h"
#include "cube\str\case.h"
#include "cube\str\part.h"
#include "cube\str\strip.h"
#include "cube\str\format.h"
#include "cube\http\header.h"
BEGIN_CUBE_HTTP_NS
//////////////////////////////////////////element class///////////////////////////////////////
std::string element::pack() const {
	return "";
}

int element::parse(const std::string &str) {
	return -1;
}

//////////////////////////////////////////field class///////////////////////////////////////
std::string header::pack() const {
	std::string res("");
	res.append(name());
	res.append(": ");
	res.append(value());
	res.append("\r\n");
	return res;
}

int header::parse(const std::string &str) {
	std::size_t sep = str.find(":");
	if (sep == std::string::npos) {
		log::error("header: %s invalid header", str.c_str());
		return -1;
	}

	name(str::strip(str.substr(0, sep)));
	value(str::strip(str.substr(sep + 1)));

	return 0;
}

bool header::operator==(const header &header) const {
	return str::lower(name()) == str::lower(header.name());
}

bool header::operator==(const std::string &name) const {
	return str::lower(header::name()) == str::lower(name);
}

//////////////////////////////////////////header class/////////////////////////////////////////
std::string headers::pack() const {
	std::string res("");
	for (::size_t i = 0; i < _headers.size(); i++) {
		res.append(_headers[i].pack());
	}
	return res;
}

int headers::parse(const std::string &str) {
	::size_t spos = 0, epos = str.find("\r\n");
	while (epos != std::string::npos) {
		//current header line
		std::string line = str.substr(spos, epos-spos);
		if (line.empty())
			break;

		//parse header
		header header;
		if(header.parse(line) != 0)
			return -1;

		//add header
		_headers.push_back(header);

		//next line
		spos = epos + 2;
		epos = str.find("\r\n", spos);
	}
	return 0;
}

std::string headers::get(const std::string &name) const {
	for (::size_t i = 0; i < _headers.size(); i++) {
		if (_headers[i] == name) {
			return _headers[i].value();
		}
	}

	return "";
}

std::string headers::get(const std::string &name, const char *default) const {
	for (::size_t i = 0; i < _headers.size(); i++) {
		if (_headers[i] == name) {
			return _headers[i].value();
		}
	}

	return std::string(default);
}

std::vector<std::string> headers::gets(const std::string &name) const {
	std::vector<std::string> res;
	for (::size_t i = 0; i < _headers.size(); i++) {
		if (_headers[i] == name) {
			res.push_back(_headers[i].value());
		}
	}
	return res;
}

void headers::add(const std::string &name, const std::string &value) {
	_headers.push_back(header(name, value));
}

void headers::set(const std::string &name, const std::string &value) {
	std::vector<header>::iterator iter = std::find(_headers.begin(), _headers.end(), name);
	if (iter != _headers.end()) {
		(*iter).value(value);
	} else {
		_headers.push_back(header(name, value));
	}
}
END_CUBE_HTTP_NS
