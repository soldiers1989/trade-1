#pragma once
#include <vector>
#include <algorithm>
#include "cube\http\pair.h"
BEGIN_CUBE_HTTP_NS
//parameter
class param : public pair {
public:
	param() {}
	param(const std::string &name, const std::string &value) : pair(name, value) {}
	virtual ~param() {}
	
	std::string pack() const;
	int parse(const std::string &str);

public:
	inline bool operator==(const std::string &name) const {
		return param::name() == name;
	}
};

//parameters
class params {
public:
	params() {}
	virtual ~params() {}

	std::string pack() const;
	int parse(const std::string &str);

public:
	bool empty() const;
	bool has(const std::string &name) const;
	void add(const std::string &name, const std::string &value);

	std::string get(const std::string &name) const;
	std::string get(const std::string &name, const char *default) const;
	void gets(const std::string &name, std::vector<std::string> &values) const;

private:
	std::vector<param> _params;
};

END_CUBE_HTTP_NS
