#include "sessionapi.h"
#include <iostream>

BEGIN_SERVER_NAMESPACE

sessionapi::sessionapi() {

}

sessionapi::~sessionapi() {
}

int sessionapi::on_open(void *arg) {
	std::cout << "on open: " <<peer().ip() <<":" <<peer().port() << std::endl;
	recv(1024);
	return 0;
}

int sessionapi::on_send(int transfered) {
	std::cout << "on send: " << transfered << ", " << peer().ip() << ":" << peer().port() << std::endl;
	return -1;
}

int sessionapi::on_recv(char *data, int transfered) {
	std::cout << "on recv: "<<transfered << ", " <<peer().ip() << ":" << peer().port() << std::endl;
	if (transfered == 0) {
		return -1;
	}

	*(data + transfered) = 0;
	std::cout << data << std::endl;

	char * hello = "hello!";
	send(hello, strlen(hello));
	return 0;
}

int sessionapi::on_close() {
	std::cout << "on close: " << peer().ip() << ":" << peer().port() << std::endl;
	return 0;
}
END_SERVER_NAMESPACE
