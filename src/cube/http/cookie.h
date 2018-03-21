#pragma once
#include <map>
#include <string>
#include <time.h>
#include "cube\ns.h"
BEGIN_CUBE_HTTP_NS
//http cookie class
class cookie {
public:
	cookie() : _name(""), _value(""), _domain(""), _path(""), _expires(0), _maxage(0) {}

	cookie(const std::string &name, const std::string &value)
		: _name(name), _value(value), _domain(""), _path(""), _expires(0), _maxage(0) { }
	
	cookie(const std::string &name, const std::string &value, const std::string &domain, const std::string &path, int maxage) 
		: _name(name), _value(value), _domain(domain), _path(path), _maxage(maxage), _expires(time(0) + _maxage) { }

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
END_CUBE_HTTP_NS
