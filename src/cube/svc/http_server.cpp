#include "cube\log\log.h"
#include "cube\svc\http_server.h"

BEGIN_CUBE_SVC_NS
int http_config::max_idle_time = 10;

//////////////////////////////////////http session class///////////////////////////////////////
int http_session::on_open(void *arg) {
	_last_active_time = ::time(0);
	cube::log::info("[http][%s] open session", name().c_str());
	//save servlets
	_applet = (http::applet*)arg;

	//receive data from client
	std::string errmsg("");
	int err = recv(BUFSZ, &errmsg);
	if (err != 0) {
		cube::log::error("[http][%s]%s", name().c_str(), errmsg.c_str());
		return -1;
	}

	return 0;
}

int http_session::on_send(int transfered) {
	_last_active_time = ::time(0);
	cube::log::info("[http][%s] send data: %d bytes", name().c_str(), transfered);
	//add transfered data
	_transfered += transfered;

	if (_transfered < (int)_respdata.length()) {
		//send left data
		int leftsz = _respdata.length() - _transfered;
		int sendsz = leftsz > BUFSZ ? BUFSZ : leftsz;

		return send(_respdata.c_str() + _transfered, sendsz);
	}

	//all response data has sent, close session
	return -1;
}

int http_session::on_recv(char *data, int transfered) {
	_last_active_time = ::time(0);
	cube::log::info("[http][%s] recv data: %d bytes", name().c_str(), transfered);
	try {
		if (transfered == 0)
			return -1;

		//parse request
		if(_request.parse(std::string(data, transfered)) != 0)
			return -1;

		//handle request
		_request.peerip(net::sa::ipaddr(peer().peeraddr().ip));
		if (_applet->handle(_request, _response) != 0) {
			return -1;
		}

		//pack response
		_transfered = 0;
		_respdata = _response.pack();
		if (_respdata.empty())
			return -1;

		//send response data
		int sendsz = _respdata.length() > BUFSZ ? BUFSZ : _respdata.length();
		return send(_respdata.c_str(), sendsz);
	} catch (std::exception &e) {
		cube::log::error("[http][%s] recv data: %s", name().c_str(), e.what());
		return -1;
	}
}

int http_session::on_tick(::time_t now) {
	if (now - _last_active_time > _max_idle_interval) {
		cube::log::info("[http][%s] tick time out", name().c_str());
		return -1;
	}
		
	return 0;
}

void http_session::on_close() {
	cube::log::info("[http][%s] close session", name().c_str());
}

//////////////////////////////////////http server class///////////////////////////////////////
int http_server::start(ushort port, int workers, http::applet *applet) {
	return _server.start(port, workers, applet);
}

void http_server::stop() {
	_server.stop();
}
END_CUBE_SVC_NS
