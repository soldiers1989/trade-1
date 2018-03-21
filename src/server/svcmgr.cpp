#include "svcmgr.h"
#include "config.h"
#include "cube\log.h"
#include "json\json.h"
#include "tapi\manage.h"
BEGIN_SVR_NAMESPACE
BEGIN_MGR_NAMESPACE
/////////////////////////////servlet class///////////////////////////////////
void login::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string user = req.query().params().get("user", "");
	std::string pwd = req.query().params().get("pwd", "");
	
	sec::auth auth;
	std::string emsg("");

	int err = sec::manage::inst.login(user, pwd, auth, &emsg);
	if (err != 0) {
		resp.json(emsg.c_str(), emsg.length());
		return;
	}
	
	Json::Value root;
	root["user"] = user;
	root["token"] = auth.token();

	Json::FastWriter fw;
	std::string str = fw.write(root);

	resp.json(str.c_str(), str.length());
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
cube::http::applet service::applet;

int service::start() {
	std::string emsg("");
	cube::log::info("start manage service...");

	//load configure file
	const char *config_file = "etc/manage.ini";
	int err = cfg::load(config_file); 
	if (err != 0){
		cube::log::error("load manage config file: %s failed.", config_file);
		return -1;
	}
	cube::log::info("load manage config file: %s, loaded.", config_file);

	//initialize manage module
	err = sec::manage::inst.init(sec::db(cfg::db.host, cfg::db.user, cfg::db.pwd, cfg::db.name, cfg::db.port), &emsg);
	if (err != 0) {
		cube::log::error("initialize manage service: %s, failed.", emsg.c_str());
		return -1;
	}
	cube::log::info("init manage service.");

	//start http server
	err = server.start(cfg::http.port, 1, &applet);
	if (err != 0) {
		cube::log::error("start manage service on port %d failed.", cfg::http.port);
		return -1;
	}

	cube::log::info("manage service started.");

	return 0;
}

void service::stop() {
	cube::log::info("stop manage service...");
	
	server.stop();

	cube::log::info("manage service stopped.");
}

void service::mount(const std::string &method, const std::string &path, cube::http::servlet *servlet) {
	applet.mount(method, path, servlet);
}

/////////////////////////////mount servlet///////////////////////////////////
service::servlet s_login("GET", "/manage/login", new login());

service::servlet s_add_account("GET", "/manage/account/add", new add_account());
service::servlet s_get_account("GET", "/manage/account/get", new get_account());
service::servlet s_del_account("GET", "/manage/account/del", new del_account());
service::servlet s_mod_account("GET", "/manage/account/mod", new mod_account());

END_MGR_NAMESPACE
END_SVR_NAMESPACE
