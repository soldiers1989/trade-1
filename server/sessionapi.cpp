#include "sessionapi.h"
#include <iostream>

BEGIN_SERVER_NAMESPACE

sessionapi::sessionapi(SOCKET s, cube::uint ip, cube::uint port) : session(s, ip, port) {

}

sessionapi::~sessionapi() {
}

int sessionapi::on_open(void *arg) {
	std::cout << "on open" << std::endl;
	return 0;
}

int sessionapi::on_send(cube::io_context *context, cube::uint transfered) {
	std::cout << "on send" << std::endl;
	return 0;
}

int sessionapi::on_recv(cube::io_context *context, cube::uint transfered) {
	std::cout << "on recv" << std::endl;
	return 0;
}

int sessionapi::on_close() {
	std::cout << "on close" << std::endl;
	return 0;
}
END_SERVER_NAMESPACE
