#include "cube\log\log.h"
#include "cube\str\part.h"
#include "cube\str\escape.h"
#include "cube\http\param.h"
BEGIN_CUBE_HTTP_NS
std::string param::pack() const {
	std::string res("");
	res.append(cube::str::escape(name()));
	res.append("=");
	res.append(cube::str::escape(value()));
	return res;
}

int param::parse(const std::string &str) {
	std::size_t sep = str.find('=');
	if (sep == std::string::npos) {
		log::error("params: %s, invalid param", str.c_str());
		return -1;
	}

	name(cube::str::unescape(str.substr(0, sep)));
	value(cube::str::unescape(str.substr(sep + 1)));

	return 0;
}

std::string params::pack() const {
	std::string res("");

	bool first = true;
	std::vector<param>::const_iterator iter = _params.begin(), iterend = _params.end();
	while (iter != iterend) {
		if (first) {
			res.append((*iter).pack());
			first = false;
		} else {
			res.append("&");
			res.append((*iter).pack());
		}
	}

	return res;
}

int params::parse(const std::string &str) {
	//split data by param seperator
	std::vector<std::string> items;
	cube::str::part(str.c_str(), "&", items);

	//parse key and value of each param
	for (std::size_t i = 0; i < items.size(); i++) {
		param param;
		if(param.parse(items[i]) != 0)
			return -1;
		_params.push_back(param);
	}

	return 0;
}

bool params::empty() const {
	return _params.empty();
}

bool params::has(const std::string &name) const {
	return std::find(_params.begin(), _params.end(), name) != _params.end();
}

void params::add(const std::string &name, const std::string &value) {
	_params.push_back(param(name, value));
}

std::string params::get(const std::string &name) const {
	return get(name, "");
}

std::string params::get(const std::string &name, const char *default) const {
	std::vector<param>::const_iterator citer = std::find(_params.begin(), _params.end(), name);
	if (citer != _params.end())
		return (*citer).value();
	return default;
}

void params::gets(const std::string &name, std::vector<std::string> &values) const {
	for (::size_t i = 0; i < _params.size(); i++) {
		if (_params[i].name() == name) {
			values.push_back(_params[i].value());
		}
	}
}
END_CUBE_HTTP_NS
