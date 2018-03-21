#include "cube\str\rand.h"
#include "cube\http\csession.h"
BEGIN_CUBE_HTTP_NS
//////////////////////////////////////////session class/////////////////////////////////////////
bool session::aged(time_t now) {
	if (now > _expires)
		return true;
	return false;
}

std::string session::get(const std::string &name) {
	std::map<std::string, std::string>::const_iterator citer = _items.find(name);
	if (citer != _items.end()) {
		return citer->second;
	}
	return "";
}

void session::set(const std::string &name, const std::string &value) {
	_items[name] = value;
}

//////////////////////////////////////////sessions class/////////////////////////////////////////
//default session id length
int sessions::_length = 16;
//default session life time 1 day
int sessions::_life = 86400;
//global sessions
std::mutex sessions::_mutex;
std::map<std::string, session> sessions::_sessions;

void sessions::aging() {
	std::unique_lock<std::mutex> lck(_mutex);
	time_t now = time(0);
	std::map<std::string, session>::iterator iter = _sessions.begin(), iterend = _sessions.end();
	while (iter != iterend) {
		if (iter->second.aged(now))
			_sessions.erase(iter++);
		else
			iter++;
	}
}

void sessions::life(int secs) {
	std::unique_lock<std::mutex> lck(_mutex);
	_life = secs;
}

void sessions::length(int len) {
	std::unique_lock<std::mutex> lck(_mutex);
	_length = len;
}

session &sessions::gen(int age) {
	std::unique_lock<std::mutex> lck(_mutex);
	//generate session id
	std::string id = str::random(_length);
	while (_sessions.find(id) != _sessions.end()) {
		id = str::random(_length);
	}

	//add new session
	_sessions[id] = session(id, age);

	return _sessions[id];
}

session &sessions::get(const std::string &sid) {
	std::unique_lock<std::mutex> lck(_mutex);
	return _sessions[sid];
}
END_CUBE_HTTP_NS
