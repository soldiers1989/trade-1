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
service::mount_servlet s_query_security_count("GET", "/query/security/count", new query_security_count());
service::mount_servlet s_query_security_list("GET", "/query/security/list", new query_security_list());
service::mount_servlet s_query_security_kline("GET", "/query/security/kline", new query_security_kline());
service::mount_servlet s_query_index_kline("GET", "/query/index/kline", new query_index_kline());
service::mount_servlet s_query_current_time_data("GET", "/query/current/time/data", new query_current_time_data());
service::mount_servlet s_query_current_deal_data("GET", "/query/current/deal/data", new query_current_deal_data());
service::mount_servlet s_query_current_quote_data("GET", "/query/current/quote/data", new query_current_quote_data());
service::mount_servlet s_disconnect("GET", "/disconnect", new disconnect());
service::mount_servlet s_echo("GET", "/echo", new echo());
END_QUOTES_NAMESPACE
