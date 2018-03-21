#pragma once
#include <map>
#include <mutex>
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_HTTP_NS
//http session class
class session {
public:
	session() : _id(""), _maxage(0), _expires(0) {}
	session(const std::string &id, int maxage) : _id(id), _maxage(maxage), _expires(time(0) + _maxage) { }
	~session() {}

	//test if session has aged
	bool aged(time_t now);

	//get/set session value
	std::string get(const std::string &name);
	void set(const std::string &name, const std::string &value);
private:
	//session id;
	std::string _id;
	//max age in seconds
	int _maxage;
	//expire time point
	time_t _expires;
	//session values
	std::map<std::string, std::string> _items;
};

//http sessions class
class sessions {
public:
	//aging out of life time sessions
	static void aging();

	//set default session life time in seconds
	static void life(int secs);
	//set default session id length
	static void length(int len);

	//generate a new session
	static session &gen(int age = sessions::_life);
	//get session by id
	static session &get(const std::string &sid);

private:
	//session id length
	static int _length;
	//default life time in seconds
	static int _life;
	//global sessions
	static std::mutex _mutex;
	static std::map<std::string, session> _sessions;
};

END_CUBE_HTTP_NS
