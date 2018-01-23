#include "svcmgr.h"
BEGIN_SERVICE_NAMESPACE
/////////////////////////////servlet class///////////////////////////////////
void servlet_login::handle(const cube::http::request &req, cube::http::response &resp) {
	resp.redirect("http://www.baidu.com/");
}

/////////////////////////////service manager class///////////////////////////////////
service_manager *service_manager::_instance = 0;

service_manager *service_manager::instance() {
	if (_instance == 0) {
		_instance = new service_manager();
	}

	return _instance;
}

int service_manager::start(ushort port) {
	//register servlets
	_servlets.mount("GET", "/login", new servlet_login());

	//start http server
	return _server.start(port, &_servlets);
}

void service_manager::stop() {
	_server.stop();
}
END_SERVICE_NAMESPACE
