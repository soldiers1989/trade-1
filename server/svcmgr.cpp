#include "svcmgr.h"
BEGIN_SVR_NAMESPACE
BEGIN_MGR_NAMESPACE
/////////////////////////////servlet class///////////////////////////////////
void login::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string json("{\"a\":\"0\",\"b\":\"1\"}");
	resp.json(json.c_str(), json.length());
}

void logout::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string json("{\"a\":\"0\",\"b\":\"1\"}");
	resp.json(json.c_str(), json.length());
}

void add_account::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string json("{\"a\":\"0\",\"b\":\"1\"}");
	resp.json(json.c_str(), json.length());
}

void get_account::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string json("{\"a\":\"0\",\"b\":\"1\"}");
	resp.json(json.c_str(), json.length());
}

void del_account::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string json("{\"a\":\"0\",\"b\":\"1\"}");
	resp.json(json.c_str(), json.length());
}

void mod_account::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string json("{\"a\":\"0\",\"b\":\"1\"}");
	resp.json(json.c_str(), json.length());
}

/////////////////////////////service manager class///////////////////////////////////
cube::http::server service::server;
cube::http::servlets service::servlets;

int service::start(ushort port) {
	//start http server
	return server.start(port, 1, &servlets);
}

void service::stop() {
	server.stop();
}

void service::mount(const std::string &method, const std::string &path, cube::http::servlet *servlet) {
	servlets.mount(method, path, servlet);
}

/////////////////////////////mount servlet///////////////////////////////////
service::servlet s_login("GET", "/login", new login());

service::servlet s_add_account("GET", "/account/add", new add_account());
service::servlet s_get_account("GET", "/account/get", new get_account());
service::servlet s_del_account("GET", "/account/del", new del_account());
service::servlet s_mod_account("GET", "/account/mod", new mod_account());

END_MGR_NAMESPACE
END_SVR_NAMESPACE
