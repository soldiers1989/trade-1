#include "cube\http\applet.h"
BEGIN_CUBE_HTTP_NS
void applet::mount(const std::string &method, const std::string &path, servlet *svlt) {
	std::map<std::string, std::map<std::string, std::shared_ptr<servlet>>>::iterator iter = _servlets.find(method);
	if (iter == _servlets.end()) {
		_servlets.insert(std::pair<std::string, std::map<std::string, std::shared_ptr<servlet>>>(method, std::map<std::string, std::shared_ptr<servlet>>()));
	}

	_servlets[method].insert(std::pair<std::string, std::shared_ptr<servlet>>(path, std::shared_ptr<servlet>(svlt)));
}

int applet::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string method = req.query().method();
	std::map<std::string, std::map<std::string, std::shared_ptr<servlet>>>::iterator miter = _servlets.find(method);
	if (miter == _servlets.end()) {
		//method not allowed
		resp.set_status(http::status_405_method_not_allowed);
	}

	std::map<std::string, std::shared_ptr<servlet>>::iterator siter = _servlets[method].find(req.query().path());
	if (siter != _servlets[method].end()) {
		return siter->second->handle(req, resp);
	} else {
		//request resource not found
		resp.set_status(http::status_404_not_found);
	}

	return 0;
}
END_CUBE_HTTP_NS
