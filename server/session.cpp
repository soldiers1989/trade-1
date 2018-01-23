#include "session.h"
#include <iostream>
BEGIN_SERVICE_NAMESPACE
//////////////////////////////session quote class///////////////////////////////////
int ssquote::on_open(void *arg) {
	std::cout << "on open: " << peer().ip() << ":" << peer().port() << std::endl;
	recv(1024);
	return 0;
}

int ssquote::on_send(int transfered) {
	std::cout << "on send: " << transfered << ", " << peer().ip() << ":" << peer().port() << std::endl;
	return -1;
}

int ssquote::on_recv(char *data, int transfered) {
	std::cout << "on recv: " << transfered << ", " << peer().ip() << ":" << peer().port() << std::endl;
	if (transfered == 0) {
		return -1;
	}

	*(data + transfered) = 0;
	std::cout << data << std::endl;

	char * hello = "hello!";
	send(hello, strlen(hello));
	return 0;
}

void ssquote::on_close() {
	std::cout << "on close: " << peer().ip() << ":" << peer().port() << std::endl;
}

//////////////////////////////session trade class///////////////////////////////////
int sstrade::on_open(void *arg) {
	std::cout << "on open: " << peer().ip() << ":" << peer().port() << std::endl;
	recv(1024);
	return 0;
}

int sstrade::on_send(int transfered) {
	std::cout << "on send: " << transfered << ", " << peer().ip() << ":" << peer().port() << std::endl;
	return -1;
}

int sstrade::on_recv(char *data, int transfered) {
	std::cout << "on recv: " << transfered << ", " << peer().ip() << ":" << peer().port() << std::endl;
	if (transfered == 0) {
		return -1;
	}

	*(data + transfered) = 0;
	std::cout << data << std::endl;

	char * hello = "hello!";
	send(hello, strlen(hello));
	return 0;
}

void sstrade::on_close() {
	std::cout << "on close: " << peer().ip() << ":" << peer().port() << std::endl;
}

//////////////////////////////session manage class///////////////////////////////////
int ssmanage::on_open(void *arg) {
	std::cout << "on open: " << peer().ip() << ":" << peer().port() << std::endl;
	recv(1024);
	return 0;
}

int ssmanage::on_send(int transfered) {
	std::cout << "on send: " << transfered << ", " << peer().ip() << ":" << peer().port() << std::endl;
	return -1;
}

int ssmanage::on_recv(char *data, int transfered) {
	std::cout << "on recv: " << transfered << ", " << peer().ip() << ":" << peer().port() << std::endl;
	if (transfered == 0) {
		return -1;
	}

	*(data + transfered) = 0;
	std::cout << data << std::endl;

	char * hello = "hello!";
	send(hello, strlen(hello));
	return 0;
}

void ssmanage::on_close() {
	std::cout << "on close: " << peer().ip() << ":" << peer().port() << std::endl;
}
END_SERVICE_NAMESPACE
