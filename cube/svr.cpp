#include "svr.h"
#include "log.h"
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE
//////////////////////////////////////http servlets class///////////////////////////////////////
void servlets::mount(const std::string &method, const std::string &path, servlet *servlet) {
	std::map<std::string, std::map<std::string, std::shared_ptr<http::servlet>>>::iterator iter = _servlets.find(method);
	if (iter == _servlets.end()) {
		_servlets.insert(std::pair<std::string, std::map<std::string, std::shared_ptr<http::servlet>>>(method, std::map<std::string, std::shared_ptr<http::servlet>>()));
	}

	_servlets[method].insert(std::pair<std::string, std::shared_ptr<cube::http::servlet>>(path, std::shared_ptr<cube::http::servlet>(servlet)));
}

void servlets::handle(const request &req, response &resp) {
	std::string method = req.query().method();
	std::map<std::string, std::map<std::string, std::shared_ptr<http::servlet>>>::iterator miter = _servlets.find(method);
	if (miter == _servlets.end()) {
		//method not supported
	}

	std::map<std::string, std::shared_ptr<servlet>>::iterator siter = _servlets[method].find(req.query().path());
	if (siter == _servlets[method].end()) {
		//request resource not exist
	}

	siter->second->handle(req, resp);
}

//////////////////////////////////////http session class///////////////////////////////////////
int session::on_open(void *arg) {
	cube::log::info("[http][%s] open session", name().c_str());
	//save servlets
	_servlets = (servlets*)arg;

	//receive data from client
	std::string errmsg("");
	int err = recv(BUFSZ, &errmsg);
	if (err != 0) {
		cube::log::error("[http][%s]%s", name().c_str(), errmsg.c_str());
		return -1;
	}

	return 0;
}

int session::on_send(int transfered) {
	cube::log::info("[http][%s] send data: %d bytes", name().c_str(), transfered);
	//send response content
	char buf[BUFSZ] = { 0 };
	int sz = _resp.take(buf, BUFSZ);
	if (sz > 0) {
		//send left response data
		return send(buf, sz);
	}

	//all response data has sent, close session
	return -1;
}

int session::on_recv(char *data, int transfered) {
	cube::log::info("[http][%s] recv data: %d bytes", name().c_str(), transfered);
	try {
		//feed data to request
		if (transfered > 0 && !_req.full()) {
			_req.feed(data, transfered);
		}

		//request data has completed
		if (_req.full()) {
			//process request
			_servlets->handle(_req.request(), _resp.response());

			//make response
			_resp.make();

			//send response content
			char buf[BUFSZ] = { 0 };
			int sz = _resp.take(buf, BUFSZ);
			if (sz > 0) {
				//send response data
				return send(buf, sz);
			}

			//no data
			return -1;
		}

		//wait for more data
		return 0;
	} catch (std::exception &e) {
		cube::log::error("[http][%s] recv data: %s", name().c_str(), e.what());
		return -1;
	}
}

void session::on_close() {
	cube::log::info("[http][%s] close session", name().c_str());
}

//////////////////////////////////////http server class///////////////////////////////////////
int server::start(ushort port, servlets *servlets) {
	return _server.start(port, servlets);
}

void server::stop() {
	_server.stop();
}
END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
