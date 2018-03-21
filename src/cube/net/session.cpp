#include "cube\net\session.h"
BEGIN_CUBE_NET_NS
///////////////////////////////////////////////////////////session class//////////////////////////////////////////////////////////////
int session::on_open(void *arg) {
	return -1;
}

int session::on_send(int transfered) {
	return -1;
}

int session::on_recv(char *data, int transfered) {
	return -1;
}

int session::on_timer(int id) {
	return -1;
}

void session::on_close() {
}

void session::open(socket s) {
	_socket = s;
}

int session::send(const char *data, int sz, std::string *error/* = 0*/) {
	//create a new context object
	ioctxt *context = new ioctxt(this, data, sz);

	//post a send data request
	int err = _socket.send(&context->buf, &context->overlapped, error);
	if (err != 0) {
		delete context;
		return -1;
	}

	//add to pending context list
	std::lock_guard<std::mutex> lock(_mutex);
	_contexts.push_back(context);

	return 0;
}

int session::recv(int sz, std::string *error/* = 0*/) {
	//create a new context object
	ioctxt *context = new ioctxt(sz, this);

	//post a receive data request
	int err = _socket.recv(&context->buf, &context->overlapped, error);
	if (err != 0) {
		delete context;
		return -1;
	}

	//add to pending context list
	std::lock_guard<std::mutex> lock(_mutex);
	_contexts.push_back(context);

	return 0;
}

void session::close() {
	_socket.close();
}

void session::free() {
	std::lock_guard<std::mutex> lock(_mutex);
	std::list<ioctxt*>::iterator iter = _contexts.begin(), iterend = _contexts.end();
	while (iter != iterend) {
		delete *iter;
		iter++;
	}
	_contexts.clear();
}

int session::on_send(ioctxt *context, int transfered) {
	//notify data has been sent event
	int err = on_send(transfered);

	//remove completed context
	std::lock_guard<std::mutex> lock(_mutex);
	_contexts.remove(context);

	//free context object
	delete context;

	//return error flag
	return err;
}

int session::on_recv(ioctxt *context, int transfered) {
	//notify data has been sent event
	int err = on_recv(context->buf.buf, transfered);

	//remove completed context
	std::lock_guard<std::mutex> lock(_mutex);
	_contexts.remove(context);

	//free context object
	delete context;

	//return error flag
	return err;
}

socket_t session::handle() {
	return _socket.handle();
}

std::string session::name() {
	return _socket.peeraddr().name();
}

const socket& session::peer() {
	return _socket;
}

END_CUBE_NET_NS
