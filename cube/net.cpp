#include "net.h"

BEGIN_CUBE_NAMESPACE
int session::on_open(void *arg) {
	return -1;
}

int session::on_send(int sz) {
	return -1;
}

int session::on_recv(char *data, int sz) {
	return -1;
}

int session::on_close() {
	return -1;
}

void session::open(socket_t s, uint ip, ushort port) {
	_socket.open(s, ip, port);
}

int session::send(char *data, int sz, std::string *error/* = 0*/) {
	//create a new context object
	io_context *context = new io_context(data, sz);

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
	io_context *context = new io_context(sz);

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
END_CUBE_NAMESPACE

