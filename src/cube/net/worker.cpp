#include "cube\net\worker.h"
#include "cube\net\service.h"
BEGIN_CUBE_NET_NS
void workers::start(int num, service *service) {
	_service = service;

	_loopers.start(this, num);
}

void workers::stop() {
	_loopers.stop();
}

void workers::run() {
	_service->ioloop();
}
END_CUBE_NET_NS
