#include "tdx.h"
#include <iostream>

tdx::tdx(const char* account, const char* password) : trader(account, password), _tdxapi(0), _client_id(-1) {
	_server.ip("222.247.45.187");
	_server.port(7708);
	_server.version("6.00");
	_server.deptid(1);

	//_server.ip("119.147.172.176");
	//_server.port(7708);
	//_server.version("1.12");
	//_server.deptid(2);

	//_server.ip("119.97.142.136");
	//_server.port(7708);
	//_server.version("6.00");
	//_server.deptid(1);

	//_server.ip("119.167.224.7");
	//_server.port(7708);
	//_server.version("2.03");
	//_server.deptid(0);
}

tdx::~tdx() {

}

int tdx::init() {
	/*first initialize tdx api*/
	_tdxapi = new tdxapi();
	int ret = _tdxapi->load(account().c_str(), "tdx.dll");
	if (ret != 0) {
		return -1;
	}
	_tdxapi->open();

	return 0;
}

int tdx::login() {
	char error[1024] = { 0 };
	_client_id = _tdxapi->login(_server.ip().c_str(), _server.port(), _server.version().c_str(), _server.deptid(), 
							account().c_str(), account().c_str(), password().c_str(), password().c_str(), error);
	if (_client_id < 0) {
		std::cout << error << std::endl;
		set_last_error(error);
		return -1;
	}

	return 0;
}

int tdx::query(int category) {
	char *result = new char[1024*1024], error[1024] = { 0 };
	_tdxapi->query_data(_client_id, category, result, error);//²éÑ¯×Ê½ð
	std::cout << result << std::endl;
	std::cout << error << std::endl;

	delete[]result;
	return 0;
}

int tdx::logout() {
	if(_client_id != -1){
		_tdxapi->logout(_client_id);
		return 0;
	}
	else {
		return -1;
	}
}

int tdx::destroy() {

	if (_tdxapi != 0) {
		_tdxapi->close();
		delete _tdxapi;
		_tdxapi = 0;
	}
	return 0;
}


trade_server::trade_server():_ip(""), _port(-1), _version(""), _deptid(-1) {
}

trade_server::trade_server(const std::string &ip, unsigned short port, const std::string& version, unsigned short deptid) : _ip(ip), _port(port), _version(version), _deptid(deptid){
}

trade_server::~trade_server() {
}

void trade_server::ip(const std::string& ip) {
	_ip = ip;
}

void trade_server::port(const unsigned short port) {
	_port = port;
}

void trade_server::version(const std::string& version) {
	_version = version;
}

void trade_server::deptid(const unsigned short deptid) {
	_deptid = deptid;
}

const std::string& trade_server::ip() {
	return _ip;
}

unsigned short trade_server::port() {
	return _port;
}

const std::string& trade_server::version() {
	return _version;
}

unsigned short trade_server::deptid() {
	return _deptid;
}
