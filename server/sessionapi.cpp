#include "sessionapi.h"
#include <iostream>

BEGIN_SERVER_NAMESPACE

sessionapi::sessionapi() {

}

sessionapi::~sessionapi() {
}

int sessionapi::on_open(void *arg) {
	std::cout << "on open" << std::endl;
	recv(1024);
	return 0;
}

int sessionapi::on_send(int transfered) {
	std::cout << "on send" << std::endl;
	return 0;
}

int sessionapi::on_recv(char *data, int transfered) {
	std::cout << "on recv" << std::endl;
	std::cout << data << std::endl;
	return 0;
}

int sessionapi::on_close() {
	std::cout << "on close" << std::endl;
	return 0;
}
END_SERVER_NAMESPACE
