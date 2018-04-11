#include "quotes\lang.h"
#include "quotes\alias.h"
#include "cube\log\log.h"
#include "quotes\config.h"
#include "quotes\quoter.h"
#include "quotes\servlet.h"
#include "quotes\service.h"

BEGIN_QUOTES_NAMESPACE
cube::http::applet service::applet;
cube::svc::http_server service::server;

int service::start() {
	std::string emsg("");
	cube::log::info("start quote service...");

	//init quoter
	if (quoter::instance()->init() != 0) {
		cube::log::error("init quote module failed.");
		return -1;;
	}

	//load configure file
	const char *config_file = "quote.ini";
	int err = config::load(config_file);
	if (err != 0) {
		cube::log::error("load config file: %s failed.", config_file);
		return -1;
	}
	cube::log::info("load config file: %s, loaded.", config_file);

	//set lang codepage and charset
	lang::instance()->set(config::codepage, config::charset);
	if (lang::instance()->needconv()) {
		cube::log::info("enable charset convert to %s.", config::charset.c_str());
	}

	//load alias configure if alias enable
	if (config::alias_enable == "true") {
		if (alias::instance()->load(config::alias_config.c_str()) != 0) {
			cube::log::info("load alias configure %s failed, disable alias.", config::alias_config.c_str());
		} else {
			cube::log::info("load alias configure %s success, enable alias.", config::alias_config.c_str());
		}
	} else {
		alias::instance()->disable();
	}
	
	//set http session idle time limit
	cube::svc::http_config::max_idle_time = config::idle;

	//start http server
	err = server.start(config::port, config::workers, &applet);
	if (err != 0) {
		cube::log::error("start quote service on port %d failed.", config::port);
		return -1;
	}

	cube::log::info("quote service started on port %d.", config::port);

	return 0;
}

void service::wait() {
	while (1)
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));
}

void service::stop() {
	cube::log::info("stop quote service...");
	
	server.stop();

	quoter::instance()->destroy();

	cube::log::info("quote service stopped.");
}

void service::mount(const std::string &method, const std::string &path, cube::http::servlet *servlet) {
	applet.mount(method, path, servlet);
}

/////////////////////////////mount servlet///////////////////////////////////
service::mount_servlet s_connect("GET", "/connect", new connect());
service::mount_servlet s_query_security_count("GET", "/count", new query_security_count());
service::mount_servlet s_query_security_list("GET", "/list", new query_security_list());
service::mount_servlet s_query_current_quote_data("GET", "/quote", new query_current_quote_data());
service::mount_servlet s_disconnect("GET", "/disconnect", new disconnect());
service::mount_servlet s_echo("GET", "/echo", new echo());
END_QUOTES_NAMESPACE
