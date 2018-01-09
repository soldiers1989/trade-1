#include "svcmgr.h"
BEGIN_SERVICE_NAMESPACE
/////////////////////////////servlet class///////////////////////////////////
int servlet_login::handle_get(const cube::http::request &req, cube::http::response &resp) {
	return -1;
}

int servlet_login::handle_post(const cube::http::request &req, cube::http::response &resp) {
	return -1;
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
	_servlets.mount("/login", new servlet_login());

	//start http server
	return _server.start(port, &_servlets);
}

void service_manager::stop() {
	_server.stop();
}
END_SERVICE_NAMESPACE
