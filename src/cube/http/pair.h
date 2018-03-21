#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_HTTP_NS
//name value pair
class pair {
public:
	pair() : _name(""), _value("") {}
	pair(const std::string &name, const std::string &value) : _name(name), _value(value) {}
	virtual ~pair() {}


	const std::string &name() const { return _name; }
	void name(const std::string &name) { _name = name; }

	const std::string &value() const { return _value; }
	void value(const std::string &value) { _value = value; }

private:
	std::string _name;
	std::string _value;
};
END_CUBE_HTTP_NS
