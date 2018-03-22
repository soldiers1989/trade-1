#include "cube\log\log.h"
#include "trades\config.h"
#include "trades\servlet.h"
#include "trades\service.h"

BEGIN_TRADES_NAMESPACE
cube::http::applet service::applet;
cube::svc::http_server service::server;

int service::start() {
	std::string emsg("");
	cube::log::info("start trade service...");

	//load configure file
	const char *config_file = "trade.ini";
	int err = config::load(config_file);
	if (err != 0) {
		cube::log::error("load config file: %s failed.", config_file);
		return -1;
	}
	cube::log::info("load config file: %s, loaded.", config_file);

	
	//start http server
	err = server.start(config::port, 1, &applet);
	if (err != 0) {
		cube::log::error("start manage service on port %d failed.", config::port);
		return -1;
	}

	cube::log::info("manage service started.");

	return 0;
}

void service::wait() {
	while (1)
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));
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
service::mount_servlet s_login("GET", "/trade/login", new login());
service::mount_servlet s_quote("GET", "/trade/quote", new quote());
service::mount_servlet s_order("GET", "/trade/order", new order());
service::mount_servlet s_cancel("GET", "/trade/cancel", new cancel());
service::mount_servlet s_query("GET", "/trade/query/current", new querycurrent());
service::mount_servlet s_history("GET", "/trade/query/history", new queryhistory());
service::mount_servlet s_logout("GET", "/trade/logout", new logout());

END_TRADES_NAMESPACE
